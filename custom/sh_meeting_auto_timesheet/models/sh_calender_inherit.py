from odoo import fields, models, api, Command
from odoo.tools import html2plaintext

class sh_calender_inherit(models.Model):
    _inherit = "calendar.event"
    _description = "lesson details details"

    sh_project_id = fields.Many2one("project.project", string="Project", required=True)
    sh_task_id = fields.Many2one("project.task", string="Task", required=True)
    sh_timesheet_ids = fields.One2many("account.analytic.line", "sh_meeting_id")
    
    def write(self, values):
        if "sh_project_id" in values:
            for rec in self.sh_timesheet_ids:
                rec.project_id=values.get("sh_project_id")

        if "sh_task_id" in values:
            for rec in self.sh_timesheet_ids:
                rec.task_id=values.get("sh_task_id")
        
        if "start" in values:
            for rec in self.sh_timesheet_ids:
                rec.date=values.get("start")
                
        if "duration" in values:
            for rec in self.sh_timesheet_ids:
                rec.unit_amount=values.get("duration")
                
        if "description" in values:
            for rec in self.sh_timesheet_ids:
                rec.name=values.get("description")
            
        res = super().write(values)
        return res

    def create_timesheet(self, partner):
        vals ={
                "employee_id": partner,
                "project_id": self.sh_project_id.id,
                "task_id": self.sh_task_id.id,
                "date": self.start,
                "unit_amount":self.duration,
                "name": html2plaintext(self.description),
            }
        self.sh_timesheet_ids = [Command.create(vals)]
        
    def remove_timesheet(self,partner):
        for rec in self.sh_timesheet_ids:
                if rec.employee_id.id == partner:
                    rec.unlink()
                

class sh_timesheets(models.Model):
    _inherit = "account.analytic.line"

    sh_meeting_id = fields.Many2one(
        "calendar.event",
        string="Meeting",
    )
