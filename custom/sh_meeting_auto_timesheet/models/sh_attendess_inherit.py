from odoo import fields, models, api


class sh_calender_attendee(models.Model):
    _inherit = "calendar.attendee"
    _description = "lesson details details"
    
    
        # emp_id=self.partner_id.employee_ids.ensure_one()
        # self.event_id.create_timesheet(emp_id.id)

    @api.model_create_multi
    def create(self, values):
        result = super().create(values)
        for rec in result:
            if rec.state=="accepted":
                emp_id=rec.partner_id.employee_ids.ensure_one()
                rec.event_id.create_timesheet(emp_id.id)
            else:    
                emp_id=rec.partner_id.employee_ids.ensure_one()
                rec.event_id.remove_timesheet(emp_id.id)
        return result
    
    def write(self, values):
        res = super().write(values)
        if self.state=="accepted":
            emp_id=self.partner_id.employee_ids.ensure_one()
            self.event_id.create_timesheet(emp_id.id)
        else:    
            emp_id=self.partner_id.employee_ids.ensure_one()
            self.event_id.remove_timesheet(emp_id.id)
        return res
    
    def unlink(self):
        for rec in self:
            emp_id=rec.partner_id.employee_ids.ensure_one()
            rec.event_id.remove_timesheet(emp_id.id)
        return super().unlink()