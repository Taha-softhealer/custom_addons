from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = "res.company"

    sh_restric_day_num = fields.Integer(string="Restrict Timeshhet After")

class ResConfigSetting(models.TransientModel):
    _inherit = "res.config.settings"

    sh_restric_day_num = fields.Integer(related="company_id.sh_restric_day_num",readonly=False)

