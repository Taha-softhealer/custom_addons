from odoo import fields, models, api


class res_company_inherit(models.Model):
    _inherit = "res.company"

    group_sh_enable_meeting_timesheet = fields.Boolean(string="Enable auto meeting timesheet")


class res_config_setting_inherit(models.TransientModel):
    _inherit = "res.config.settings"

    group_enable_meeting_timesheet = fields.Boolean(related="company_id.group_sh_enable_meeting_timesheet",readonly=False ,implied_group="sh_meeting_auto_timesheet.group_meeting_timesheet")


    # def set_values(self):
    #     super(res_config_setting_inherit, self).set_values()
    #     group = self.env.ref(
    #         "sh_meeting_auto_timesheet.group_meeting_timesheet", raise_if_not_found=False
    #     )
    #     if group:
    #         if self.enable_meeting_timesheet:
    #             group.users = [(6, 0, self.env["res.users"].search([]).ids)]
    #         else:
    #             group.users = [(5, 0, 0)]