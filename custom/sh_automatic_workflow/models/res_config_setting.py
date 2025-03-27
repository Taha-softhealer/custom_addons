from odoo import fields, models, api


class res_config_setting_inherit(models.TransientModel):
    _inherit = "res.config.settings"

    enable_automatic_workflow = fields.Boolean(
        default=False,
        string="Enable Auto Workflow",
        implied_group='sh_sale_automation.sh_res_config_sale_automation_group',
        config_parameter="sh_sale_automation.enable_automatic_workflow"
    )
    automatic_workflow_id = fields.Many2one(
        "sh.automatic.workflow",
        string="Default Workflow",
        config_parameter="sh_automatic_workflow.automatic_workflow_id"
    )
    
    
    def set_values(self):
        super(res_config_setting_inherit, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("sh_automatic_workflow.enable_automatic_workflow", self.enable_automatic_workflow)
        group = self.env.ref(
            "sh_automatic_workflow.group_automatic_workflow", raise_if_not_found=False
        )
        print('\n\n\n-----group------->',group)
        print('\n\n\n--------self.ena---->',self.enable_automatic_workflow)
        print('\n\n\n--------self.automatic_workflow_id---->',self.automatic_workflow_id)
        if group:
            if self.enable_automatic_workflow:
                group.users = [(6, 0, self.env["res.users"].search([]).ids)]
            else:
                group.users = [(5, 0, 0)]
        
        