# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models,api, _
from odoo.exceptions import UserError

class ShSchoolLessons(models.Model):

    _name = 'sh.school.lessons'
    _description = 'Students'

    name = fields.Char(
        index=True, default_export_compatible=True, string='Lesson')

    start_time = fields.Datetime(
        string='Start Time',
        default=fields.Datetime.now,
    )

    end_time = fields.Datetime(
        string='End Time',
        default=fields.Datetime.now,
    )

    teacher_id = fields.Many2one(
        string='Teacher', comodel_name='hr.employee')


    student_ids = fields.Many2many(comodel_name='sh.school.student', relation='sh_student_lesson_rel',
                                   column1='student_id', column2='lesson_id', string='Students')

    service_id = fields.Many2one(
        string='Service',
        comodel_name='product.product',
        domain=[('detailed_type', '=', 'service')])

    instrument_id = fields.Many2one(
        string='Equipment', comodel_name='maintenance.equipment')

    lesson_line_count = fields.Integer(
        string='count_lesson_line', compute="_compute_lesson_line_count"
    )

    attendance_count = fields.Integer(
        string='Attendance Count', compute="_compute_attendance_count"
    )
    
    sh_available_space = fields.Integer(string='Available Spaces',default='20')
    
    sh_lasson_duration = fields.Selection(([ 
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5')]),string='Duration')
    
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

                
                
    def create(self, vals):
        record = super(ShSchoolLessons, self).create(vals)
        print("\n\n\n\n>>> create called >>>>>",record.sh_lasson_duration,record.company_id.sh_lesson_duration)
        if record.sh_lasson_duration and record.company_id.sh_lesson_duration:
            if int(record.sh_lasson_duration) > int(record.company_id.sh_lesson_duration):
                raise UserError(_('Class Duration Is Maximum {} Hours'.format(record.company_id.sh_lesson_duration)))
        return record
    
    
    def write(self, vals):
        res = super(ShSchoolLessons, self).write(vals)
        for record in self:
            if 'sh_lasson_duration' in vals and record.sh_lasson_duration and record.company_id.sh_lesson_duration:
                if int(record.sh_lasson_duration) > int(record.company_id.sh_lesson_duration):
                    raise UserError(_('Class Duration Is Maximum {} Hours'.format(record.company_id.sh_lesson_duration)))
        return res
    
    @api.constrains('sh_available_space', 'student_ids')
    def _check_available_space(self):
        for record in self:
           
            if record.sh_available_space < len(record.student_ids):
                raise UserError(_('More student then avilable Spaces'))
    
    def _compute_lesson_line_count(self):
        for lesson_line in self:
            lesson_line.lesson_line_count = self.env['sh.class.lesson.line'].search_count(
                [('lesson_id', '=', lesson_line.id)])

    def action_class_lessons(self):
        self.ensure_one()
        domain = [('lesson_id', '=', self.id)]
        return {
            'name': _("Lessons"),
            'view_mode': 'tree',
            'views': [(self.env.ref('sh_music_school.sh_class_lesson_line_view_tree').id, 'tree'), (False, 'form')],
            'res_model': 'sh.class.lesson.line',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': domain,
        }

    def _compute_attendance_count(self):

        for attendees in self:

            attendees.attendance_count = self.env['sh.school.attendance'].search_count(
                [('lesson_id', '=', self.id)])

    def action_attendance_count(self):
        self.ensure_one()
        domain = [('lesson_id', '=', self.id)]
        return {
            'name': _("Attendance"),
            'view_mode': 'tree',
            'views': [(self.env.ref('sh_music_school.sh_school_attendance_tree_view').id, 'tree'), (False, 'form')],
            'res_model': 'sh.school.attendance',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': domain,
        }

