from odoo import fields, models, api


class sh_calender_attendee(models.Model):
    _inherit = "calendar.attendee"
    _description = "lesson details details"

    company_id = fields.Many2one("res.company",default=lambda self: self.env.company.id)

    @api.model_create_multi
    def create(self, values):
        result = super().create(values)
        if self.company_id.enable_meeting_timesheet:
            for rec in result:
                if rec.state == "accepted":
                    emp_id = rec.partner_id.employee_ids.ensure_one()
                    rec.event_id.create_timesheet(emp_id)
                else:
                    emp_id = rec.partner_id.employee_ids.ensure_one()
                    rec.event_id.remove_timesheet(emp_id)
        return result

    def write(self, values):
        res = super().write(values)
        if self.company_id.enable_meeting_timesheet:
            if self.state == "accepted":
                emp_id = self.partner_id.employee_ids.ensure_one()
                self.event_id.create_timesheet(emp_id)
            else:
                emp_id = self.partner_id.employee_ids.ensure_one()
                self.event_id.remove_timesheet(emp_id)
        return res

    def unlink(self):
        if self.company_id.enable_meeting_timesheet:
            for rec in self:
                emp_id = rec.partner_id.employee_ids.ensure_one()
                rec.event_id.remove_timesheet(emp_id)
        return super().unlink()
