# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models, _, tools, api, Command


class ShSchoolStudent(models.Model):

    _name = 'sh.school.student'
    _inherit = 'avatar.mixin'
    _description = 'Students'

    partner_id = fields.Many2one(
        string='Student', comodel_name='res.partner', required=True)
    
    avatar_1920 = fields.Image(related='partner_id.avatar_1920',readonly=False,store=True)

    name = fields.Char(string="Student Name", related='partner_id.name',
                       store=True, readonly=False)

    gender = fields.Selection(string='Gender', selection=[
                              ('male', 'Male'), ('female', 'Female')])

    language = fields.Char(string='Language')

    birthday = fields.Date(
        string='Birthday', default=fields.Date.context_today)

    visa_info = fields.Char(string='Visa info')

    blood_group = fields.Selection(
        string='Blood Group',
        selection=[('a+', 'A+'), ('B+', 'B+'), ('o+', 'O+'), ('ab+', 'AB+'),
                   ('a-', 'A-'), ('B-', 'B-'), ('o-', 'O-'), ('ab-', 'AB-'),]
    )

    street = fields.Char(related='partner_id.street', readonly=False)

    street2 = fields.Char(related='partner_id.street2', readonly=False)

    zip = fields.Char(change_default=True,
                      related='partner_id.zip', readonly=False)

    city = fields.Char(related='partner_id.city', readonly=False)

    state_id = fields.Many2one("res.country.state", string='State',
                               ondelete='restrict', domain="[('country_id', '=?', country_id)]", related='partner_id.state_id', readonly=False)

    country_id = fields.Many2one(
        'res.country', string='Country', ondelete='restrict', related='partner_id.country_id', readonly=False)

    country_code = fields.Char(
        related='country_id.code', string="Country Code", readonly=False)

    email = fields.Char(related='partner_id.email', readonly=False)

    email_formatted = fields.Char(
        'Formatted Email', compute='_compute_email_formatted',
        help='Format email address "Name <email@domain>"', related='partner_id.email_formatted', readonly=False)

    phone = fields.Char(
        unaccent=False, related='partner_id.phone', readonly=False)

    mobile = fields.Char(
        unaccent=False, related='partner_id.mobile', readonly=False)

    classes_ids = fields.Many2many(
        string='Classes',
        comodel_name='sh.school.classes',
        relation='sh_student_class_rel',
        column1='student_id',
        column2='class_id',
    )

    student_classes_count = fields.Integer(
        compute='_compute_student_classes_count')
    
    student_invoice_count=fields.Integer(compute="compute_student_invoice_count")

    @api.depends('name', 'email')
    def _compute_email_formatted(self):

        self.email_formatted = False
        for partner in self:
            emails_normalized = tools.email_normalize_all(partner.email)
            if emails_normalized:
                # note: multi-email input leads to invalid email like "Name" <email1, email2>
                # but this is current behavior in Odoo 14+ and some servers allow it
                partner.email_formatted = tools.formataddr((
                    partner.name or u"False",
                    ','.join(emails_normalized)
                ))
            elif partner.email:
                partner.email_formatted = tools.formataddr((
                    partner.name or u"False",
                    partner.email
                ))

    def action_student_class(self):
        self.ensure_one()
        domain = [('student_ids.id', '=', self.id)]
        return {
            'name': _("Classes"),
            'view_mode': 'tree,form',
            'views': [(self.env.ref('sh_music_school.sh_school_classes_tree_view').id, 'tree'), (False, 'form')],
            'res_model': 'sh.school.classes',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': domain,
        }

  

    def _compute_student_classes_count(self):
        for student in self:
            student.student_classes_count = student.classes_ids.search_count(
                [('student_ids', 'in', student.id)])
            
            
        
    def compute_student_invoice_count(self):
        for rec in self:
            rec.student_invoice_count=self.env['account.move'].search_count([("partner_id","=",self.partner_id.id),("payment_state","=","paid")])
            
    
            
    def action_student_invoice(self):
      
        return {

            'type': 'ir.actions.act_window',

            'name': 'Vehicle Invoice',

            'view_mode': 'tree,form',

            'res_model': 'account.move',

            'domain':  [('partner_id', '=', self.partner_id.id),("payment_state","=","paid")],

            'context': "{'create': False}"

        }
        

    def add_student(self):

        active_model = self.env.context.get('my_active_model')
        active_id = self.env.context.get('my_active_id')

        if active_model == 'sh.school.classes' and active_id:
            student_class = self.env[active_model].browse(active_id)
            student_class.student_ids = [(4, student) for student in self.ids]

    def create_attendance(self):
    

        active_model = self.env.context.get('my_active_model')
        active_id = self.env.context.get('my_active_id')
        class_lesson = self.env[active_model].browse(active_id)

        if active_model == 'sh.school.classes' and active_id:

            for line in class_lesson.class_lesson_line:

                line.attendance_ids = [Command.create({'student_id': attendee, 'lesson_id': line.lesson_id.id, 'teacher_id': line.teacher_id.id,
                                                       'start_time': line.start_time, 'end_time': line.end_time, 'instrument_id': line.lesson_id.instrument_id.id}) for attendee in self.ids]
