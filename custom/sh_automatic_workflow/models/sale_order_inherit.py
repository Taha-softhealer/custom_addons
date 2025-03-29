from odoo import fields, models, api


class sh_sale_order_inherit(models.Model):
    _inherit = "sale.order"
    _description = "sales note details"
    
    def default_get(self, fields):
        res = super(sh_sale_order_inherit, self).default_get(fields)
        
        # Get context values
        res_enable = self.env['ir.config_parameter'].sudo().get_param("sh_automatic_workflow.enable_automatic_workflow")
        res_auto_id = self.env['ir.config_parameter'].sudo().get_param("sh_automatic_workflow.automatic_workflow_id")
        
        if res_enable:
            res['enable_automatic_workflow'] = res_enable
        else:
            res['enable_automatic_workflow'] = False
        
        if res_auto_id:
            res_auto_id = int(res_auto_id)
            res_auto_id_record = self.env["sh.automatic.workflow"].browse(res_auto_id)
            if res_auto_id_record:
                res['automatic_workflow_id'] = res_auto_id_record.id
        
        print('\n\n\n-----automatic_workflow_id------->', res.get("automatic_workflow_id"))
        return res

    enable_automatic_workflow = fields.Boolean(
        string="Enable Auto Workflow",
    )
    automatic_workflow_id = fields.Many2one(
        "sh.automatic.workflow",
        string="Automatic Workflow",
    )


    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            if self.partner_id.automatic_workflow_id:
                self.automatic_workflow_id=self.partner_id.automatic_workflow_id
            else:
                res_auto_id = self.env['ir.config_parameter'].sudo().get_param("sh_automatic_workflow.automatic_workflow_id")
                self.automatic_workflow_id=int(res_auto_id)
                
                
    def action_confirm(self):
        super().action_confirm()
        if self.automatic_workflow_id:
            if self.automatic_workflow_id.delivery_order:
                rec=self.env["stock.picking"].search([("sale_id","=",self.id)])
                print("============rec=========>",rec)
                print("============rec=========>",self.id)
                rec.button_validate()