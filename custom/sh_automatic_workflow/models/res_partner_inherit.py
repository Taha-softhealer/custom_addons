from odoo import fields, models, api


class sh_sale_order_inherit(models.Model):
    _inherit = "res.partner"
    _description = "res partner details"
                     
    automatic_workflow_id = fields.Many2one(
        'sh.automatic.workflow',
        string='Automatic Workflow',
        )
    
    
    def write(self, values):
        if "automatic_workflow_id" in values:
            if self.is_company or values.get("is_company"):
                for id in self.child_ids or values.get("child_ids"):
                    id.automatic_workflow_id=values.get("automatic_workflow_id")
        res = super().write(values)
        return res