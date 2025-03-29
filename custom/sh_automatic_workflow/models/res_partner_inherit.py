from odoo import fields, models, api


class sh_sale_order_inherit(models.Model):
    _inherit = "res.partner"
    _description = "res partner details"
                     
    automatic_workflow_id = fields.Many2one(
        'sh.automatic.workflow',
        string='Automatic Workflow',
        )