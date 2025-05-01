# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models, _, api
from odoo.exceptions import UserError

class ShClassLessonLine(models.Model):

    _name = 'sh.class.lesson.line'
    _description = 'Class Lesson Line'
    _rec_name = 'lesson_id'

    class_id = fields.Many2one(
        string='class', comodel_name='sh.school.classes',copy=False)

    lesson_id = fields.Many2one(
        string='Lesson', comodel_name='sh.school.lessons')

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

    
    attendance_ids = fields.One2many('sh.school.attendance', 'class_lesson_line_id', string='Attendees')
    
    student_ids = fields.Many2many(comodel_name='sh.school.student', relation='sh_school_student_lesson_rel',
                                   column1='student_id', column2='lesson_id', string='Students')

    service_id = fields.Many2one(
        string='Service',
        comodel_name='product.product',
        domain=[('detailed_type', '=', 'service')])

    instrument_id = fields.Many2one(
        string='Instrument', comodel_name='maintenance.equipment', related='attendance_ids.instrument_id')

    state = fields.Selection(string='State', selection=[('draft', 'DRAFT'), ('started', 'STARTED'), (
        'completed', 'COMPLETED'),('fulfilled','FULFILLED'),('cancelled', 'CANCELLED')], default='draft')
    
    
    student_ids=fields.Many2many("sh.school.student")
    
    is_mass_attendance=fields.Boolean(string="Mass Attendance click",copy=False)
    
    is_present_absent_attendance = fields.Boolean(string='Has Active Lesson', compute='_compute_is_present_absent_attendance', store=True)
    
    
    def action_fulfilled(self):
        self.write({
            'state':'fulfilled'
        })
    
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
    @api.depends('attendance_ids.sh_is_button_click')
    def _compute_is_present_absent_attendance(self):
        for record in self:
            record.is_present_absent_attendance = any(attendance_line.sh_is_button_click for attendance_line in record.attendance_ids)
  
  
    def action_state_started(self):
        
        if self.class_id.state == 'draft':
                raise UserError(_('First start the class'))
            
        if self.class_id.state == 'cancelled':
                raise UserError(_('Your class is cancelled, so you cannot start or cancel the lesson.')) 
        
        date = self.start_time
        previous_dates = [line for line in self.class_id.class_lesson_line if line.start_time.date() < date.date()]  
        
        for previous_date in previous_dates:
          if previous_date.state not in ['fulfilled', 'cancelled']:
                raise UserError(_('First fulfilled the previous lessons before starting this one.'))
        
        self.state = "started"
        
    def action_state_completed(self):
       
        for attendance in self.attendance_ids:
            if attendance.student_attendance:
                self.state = "completed"
                
            else:
                raise UserError(_("First take the attendance"))
            

    def action_state_cancelled(self):
        if self.class_id.state == 'draft':
                raise UserError(_('First start the class'))
            
        if self.class_id.state == 'cancelled':
                raise UserError(_('Your class is cancelled, so you cannot start or cancel the lesson.'))
            
        date = self.start_time
        previous_dates = [line for line in self.class_id.class_lesson_line if line.start_time.date() < date.date()]  
        
        for previous_date in previous_dates:
          if previous_date.state not in ['fulfilled', 'cancelled']:
                raise UserError(_('First fulfilled or cancelled the previous lessons before starting this one.'))
            
            
        for attendace in self.attendance_ids:
          
            attendace.student_attendance=False
        self.state = "cancelled"
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_state_reset_to_draft(self):
      
        self.state = "draft"
        self.is_mass_attendance=False
        for attendace in self.attendance_ids:
            attendace.student_attendance=False
            attendace.sh_is_button_click=False

    @api.onchange('lesson_id')
    def _onchange_lesson_id(self):

        self.start_time = self.lesson_id.start_time
        self.end_time = self.lesson_id.end_time
        self.teacher_id = self.lesson_id.teacher_id
        self.service_id = self.lesson_id.service_id
        self.instrument_id = self.lesson_id.instrument_id

    def action_student_attendance_present(self):
        # self.is_mass_attendance=True
        
        for i in self.attendance_ids:
            i.student_attendance = 'present'
          
        self.write({
            'is_mass_attendance':True
        })  


    def add_attendees(self):
      
        if  self:
                for line in self:
                    line.student_btn()
                   


    def student_btn(self):
       
        self.attendance_ids=False
      
        for student_obj in self.class_id.student_ids:
            student_attendence=self.env['sh.school.attendance'].create({
                    "lesson_id":self.lesson_id.id,
                    'student_id':student_obj.id,
                    'start_time':self.start_time,
                    'end_time':self.end_time,
                    'class_lesson_line_id':self.id,
                    'teacher_id':self.lesson_id.teacher_id.id
                    
                })
           
        self.write({
            'service_id':self.class_id.service_id,
            'teacher_id':self.class_id.teacher_id,
            "student_ids":self.class_id.student_ids,
            })

    
                   
    
    def create(self, vals):
       
        res = super(ShClassLessonLine, self).create(vals)
        res.add_attendees()
            
        return res

