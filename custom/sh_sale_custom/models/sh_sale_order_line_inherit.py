from odoo import fields, models, api


class sh_sale_order_line_inherit(models.Model):
    _inherit = "sale.order.line"
    _description = "sales order line inherit details"
                    
    custom_note=fields.Many2one("sh.note",string="Note")
    sr_num=fields.Integer("S.R.No")

    