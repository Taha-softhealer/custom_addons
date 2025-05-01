# -*- coding: utf-8 -*-
# Softhealer Technologies

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime
import pytz

class ShReporting(models.TransientModel):
    _name="sh.reporting"
    _description="sh reporting"
    
    start_date=fields.Date(string="Start Date",required=True)
    end_date=fields.Date(string="End Date",required=True)
    lesson_id=fields.Many2one('sh.school.lessons',string="Lesson")
    attendance=fields.Selection([("present","PRESENT"),("absent","ABSENT")])
    
    
    
    def action_send(self):
        if not self.start_date or not self.end_date:
            raise UserError('Please provide start date and end date')

      
        if self.end_date < self.start_date:
            raise UserError(_("The end date must come after the start date. Please correct the dates."))

        user_tz = self.env.user.tz or 'UTC'
        local_tz = pytz.timezone(user_tz)

        
        start_date_local = datetime.combine(self.start_date, datetime.min.time()).replace(tzinfo=local_tz)
        end_date_local = datetime.combine(self.end_date, datetime.max.time()).replace(tzinfo=local_tz)

       
        start_date_utc = start_date_local.astimezone(pytz.utc).replace(tzinfo=None)
        end_date_utc = end_date_local.astimezone(pytz.utc).replace(tzinfo=None)

        domain = [
            ('start_time', '>=', start_date_utc),
            ('end_time', '<=', end_date_utc)
        ]

        if self.lesson_id:
            domain.append(('lesson_id', '=', self.lesson_id.id))

        if self.attendance:
            domain.append(('student_attendance', '=', self.attendance))

        data = self.env['sh.school.attendance'].search(domain)

        if not data:
            raise UserError("No students attendance recrods available for specified criteria.")

        return self.env.ref('sh_music_school.action_report_sh_class').report_action(docids=data, config=False)
      