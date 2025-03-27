from odoo import fields, models, api


class sh_sale_order_inherit(models.Model):
    _inherit = "sale.order"
    _description = "sales note details"
                    
                    
    def default_get(self, fields):
        res = super(sh_sale_order_inherit, self).default_get(fields)
        # Get context values
        res_enable=self.env['ir.config_parameter'].sudo().get_param("sh_automatic_workflow.enable_automatic_workflow")
        res_auto_id=self.env['ir.config_parameter'].sudo().get_param("sh_automatic_workflow.automatic_workflow_id")
        print('\n\n\n-----parent_record.id------->',res_auto_id)
        res['enable_automatic_workflow']=res_enable
        res['automatic_workflow_id']=res_auto_id
        # if self.env.context.get('default_product_id'):
        #     parent_record = self.env['product.template'].browse(self.env.context['default_product_id'])
        #     print('\n\n\n-----parent_record.id------->',parent_record.id)
        #     res.update({
        #         'name': parent_record.name,
        #         'product_id': parent_record.id
        #     })
        return res

                    
    enable_automatic_workflow = fields.Boolean(
        default=False,
        string="Enable Auto Workflow",
    )
    automatic_workflow_id = fields.Many2one(
        "sh.automatic.workflow",
        string="Automatic Workflow",
    )