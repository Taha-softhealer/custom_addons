from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class ResCompany(models.Model):
    _inherit = "account.analytic.line"

    @api.model_create_multi
    def create(self, values):
        result = super().create(values)
        for rec in result:
            if rec.date and rec.company_id.sh_restric_day_num:
                # print('\n\n\n-----fields.Date.today()-result.date------->',fields.Date.today()-result.date)
                if (fields.Date.today()-rec.date)>timedelta(days=rec.company_id.sh_restric_day_num) and not self.env.user.has_group("sh_backdated_timesheet.group_backdate_timesheet"):
                    raise ValidationError(f"You can not create timesheet older than {rec.company_id.sh_restric_day_num} days")
            
        return result