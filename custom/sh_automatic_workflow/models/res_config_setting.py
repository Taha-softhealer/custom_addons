from odoo import fields, models, api


class res_config_setting_inherit(models.TransientModel):
    _inherit="res.config.settings"

    enable_automatic_workflow = fields.Boolean(string='Enable Auto Workflow')
    automatic_workflow_id = fields.Many2one(
        'sh.automatic.workflow',
        string='Default Workflow',
        )