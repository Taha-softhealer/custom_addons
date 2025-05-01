# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models, _, api
from odoo.exceptions import UserError

class ShSchoolAttendance(models.Model):

    _name = 'sh.school.attendance'
    _rec_name = 'student_id'
    _description = 'Attendance'

    student_id = fields.Many2one('sh.school.student', string='Student')

    lesson_id = fields.Many2one(
        string='Lesson', comodel_name='sh.school.lessons')

    teacher_id = fields.Many2one(string='Teacher', comodel_name='hr.employee')

    start_time = fields.Datetime(string='Start Time')

    end_time = fields.Datetime(string='End Time')

    student_attendance = fields.Selection(string='Student Attendance', selection=[
                                          ('present', 'Present'), ('absent', 'Absent')],store=True)

    instrument_id = fields.Many2one(
        string='Instrument', comodel_name='maintenance.equipment')

    class_lesson_line_id = fields.Many2one(
        string='Class Lssson Line Id', comodel_name='sh.class.lesson.line')
    
    sh_is_button_click=fields.Boolean(string="Button Click")
    

  
    @api.depends('student_id.name')
    def _compute_display_name(self):
        for attendance in self:
            attendance.display_name = attendance.student_id.name

    @api.onchange('lesson_id')
    def _onchange_lesson_id(self):
        self.teacher_id = self.lesson_id.teacher_id
        self.instrument_id = self.lesson_id.instrument_id
    
    def present_button(self):
      
        self.write({
            "student_attendance":"present",
            'sh_is_button_click':True
        })
        
        
    def absent_button(self):
       
        self.write({
            "student_attendance":"absent",
            'sh_is_button_click':True
        })
        
    
    