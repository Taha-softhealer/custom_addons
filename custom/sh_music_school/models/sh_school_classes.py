# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from datetime import timedelta
from odoo import fields, models,  _, api, Command
from odoo.exceptions import UserError
from odoo.exceptions import UserError, ValidationError


class ShSchoolClasses(models.Model):

    _name = 'sh.school.classes'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Classes"

    name = fields.Char(string='Class')

    class_from = fields.Datetime(string='From', default=fields.Datetime.now)

    class_to = fields.Datetime(string='To', default=fields.Datetime.now)

    lasson_duration = fields.Float(string='Lesson Duration')

    location = fields.Char(string='Location')

    teacher_id = fields.Many2one('hr.employee', string='Class Teacher')

    available_space = fields.Integer(string='Available Spaces')

    student_ids = fields.Many2many(comodel_name='sh.school.student', relation='sh_school_student_classes_rel',
                                   column1='student_id',
                                   column2='class_id',
                                   string='Students',
                                   )

    lesson_id = fields.Many2one(comodel_name='sh.school.lessons', relation='sh__classes_lesson_rel',
                                  column1='lesson_id',
                                  column2='class_id',
                                  string='Lessons',
                                  )
    class_lesson_line = fields.One2many(
        'sh.class.lesson.line', 'class_id', string='Class Lesson Line',copy=False)

    state = fields.Selection(string='State', selection=[('draft', 'DRAFT'), ('running', 'RUNNING'), (
        'completed', 'COMPLETED'), ('cancelled', 'CANCELLED')], default='draft', tracking=True,)

    repeats = fields.Selection(string='Repeats', selection=[(
        'daily', 'Daily'), ('weekly', 'Weekly') ])

    service_id = fields.Many2one(
        string='Service',
        comodel_name='product.product',
        domain=[('detailed_type', '=', 'service')],


    )

    invoice_count = fields.Integer(
        "Invoice Count",
        compute='_compute_invoice_count',
    )

    sh_lesson_lines_count=fields.Integer(
        "Lessons Count",
        compute='_compute_sh_lesson_line_count',
    )

    is_invoice_generated=fields.Boolean("Invoice Generated",copy=False)

    is_all_lesson_completed = fields.Boolean(string='All Lessons Completed', compute='_compute_is_all_lesson_completed',store=True)
    
    active=fields.Boolean("Active",default=True,readonly=True,tracking=True,copy=False)

    mon = fields.Boolean()
    tue = fields.Boolean()
    wed = fields.Boolean()
    thu = fields.Boolean()
    fri = fields.Boolean()
    sat = fields.Boolean()
    sun = fields.Boolean()
    

    def action_state_started(self):
      
        self.state = "running"

    def action_state_completed(self):

        if all(lesson.state in ['fulfilled', 'cancelled'] for lesson in self.class_lesson_line):
            self.state = "completed"
        else:
            raise ValidationError("Please fulfill the lessons before completing the class.")

    def action_state_cancelled(self):
        self.active=False
        self.state = "cancelled"

    def action_state_reset_to_draft(self):

        self.state = "draft"
        self.class_lesson_line.add_attendees()
        
    @api.constrains('available_space', 'student_ids')
    def _check_available_space(self):
        for record in self:

            if record.available_space < len(record.student_ids):
                raise UserError(_('More student then avilable Spaces'))

    
    @api.onchange('lasson_duration','class_from', 'class_to','student_ids', 'lesson_id', 'repeats', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
    def _onchange_create_lasson(self):
        
        self.class_lesson_line
       
        weekly_days = []
        if self.repeats == "weekly":
            if self.mon == True:
                weekly_days.append(0)
            if self.tue == True:
                weekly_days.append(1)
            if self.wed == True:
                weekly_days.append(2)
            if self.thu == True:
                weekly_days.append(3)
            if self.fri == True:
                weekly_days.append(4)
            if self.sat == True:
                weekly_days.append(5)
            if self.sun == True:
                weekly_days.append(6)

        def _get_duration(value):
            hours, minutes = divmod(abs(value) * 60, 60)
            minutes = round(minutes)
            if minutes == 60:
                minutes = 0
                hours += 1
            return (hours, minutes)
        hours, minutes = _get_duration(self.lasson_duration)

        lesson_list = []

        start_time = lesson_start = self.class_from
        end_time = lesson_end = self.class_from + \
            timedelta(hours=hours,  minutes=minutes)
       
        while end_time <= self.class_to:
            for lesson in self.lesson_id:

                if self.repeats == "daily" or (start_time.weekday() in weekly_days and end_time.weekday() in weekly_days):
                    lesson_list.append(Command.create({
                        'lesson_id': lesson.id,
                        'teacher_id': lesson.teacher_id.id,
                        'student_ids': [(6, 0, self.student_ids.ids)],
                        'start_time': start_time,
                        'end_time': end_time,
                        'class_id': self.id,
                      
                    }))

                start_time += timedelta(hours=hours, minutes=minutes)
                end_time += timedelta(hours=hours, minutes=minutes)

            lesson_start += timedelta(days=1)
            start_time = lesson_start

            lesson_end += timedelta(days=1)
            end_time = lesson_end

        self.class_lesson_line = [Command.clear()] + lesson_list
       

    def _compute_invoice_count(self):
        for account in self:
            account.invoice_count = self.env['account.move'].search_count(
                [('sh_school_classes_id', '=', self.id)])

    def create_invoices(self):
        if self.invoice_count:
            raise UserError(_("Invoice Already Created"))

        student_invoice = []

        journal = self.env['account.journal'].search([('type', '=', 'sale'), (
            'company_id', '=', self.env.company.id), ('code', '=', 'MSINV')], limit=1)
        if not journal:
            journal = self.env['account.journal'].create(
                {'type': 'sale', 'company_id': self.env.company.id, 'code': 'MSINV', 'name': 'Music School Invoices'})

        for classes in self:

            for student in classes.student_ids:

                student_invoice.append({
                    'move_type': 'out_invoice',
                    'journal_id': journal.id,
                    'partner_id': student.partner_id.id,
                    'sh_school_classes_id':self.id,
                    'invoice_line_ids': [
                        (0, None, {
                            'product_id': classes.service_id.id,
                            'quantity': 1,
                            'price_unit': classes.service_id.lst_price*self.sh_lesson_lines_count,
                            'tax_ids': [Command.set(classes.service_id.taxes_id.ids)],
                        })
                    ]
                })
        self.env['account.move'].with_company(
            self.env.company).create(student_invoice)

        self.write({
            "is_invoice_generated":True
        })

    def action_add_student(self):

        return {
            'name': _('Add student in lessons'),
            'type': 'ir.actions.act_window',
            'res_model': 'sh.school.student',
            'view_id': self.env.ref('sh_music_school.sh_school_student_view_tree').id,
            'view_mode': 'tree',
            'context': {
                'my_active_model': 'sh.school.classes',
                'my_active_id': self.id,
            },
            'domain': [('id', 'not in', self.student_ids.ids)],
            'target': 'new',
        }


    def action_view_invoice(self):
        result = {
            "name": _("Customer Invoices"),
            'view_mode': 'tree,form',
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            'views': [(self.env.ref('account.view_out_invoice_tree').id, 'tree'), (False, 'form')],
            "domain":[('sh_school_classes_id', '=', self.id)],
        }
        return result


    def write(self,vals):
      
        res=super(ShSchoolClasses,self).write(vals)
        
        if 'student_ids' in vals:
             self.class_lesson_line.add_attendees()
        return res


    def create(self, vals):
       
        res = super(ShSchoolClasses, self).create(vals)
       
        if 'student_ids' in vals:
             self.class_lesson_line.add_attendees()
        return res



    @api.depends('lesson_id')
    def _compute_sh_lesson_line_count(self):
        for rec in self:
            rec.sh_lesson_lines_count=len(rec.class_lesson_line)


    @api.depends('class_lesson_line.state')
    def _compute_is_all_lesson_completed(self):
        for record in self:
            all_completed = all(rec.state in ['fulfilled', 'cancelled'] for rec in record.class_lesson_line)
            record.is_all_lesson_completed = all_completed



    @api.onchange('lesson_id')
    def _onchange_lesson_id(self):
        self.teacher_id=self.lesson_id.teacher_id.id
        self.student_ids=self.lesson_id.student_ids.ids
        self.service_id=self.lesson_id.service_id.id
        self.available_space=self.lesson_id.sh_available_space
        self.lasson_duration=self.lesson_id.sh_lasson_duration



