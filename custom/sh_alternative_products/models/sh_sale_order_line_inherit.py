from odoo import fields, models, api


class sh_sale_order_line_inherit(models.Model):
    _inherit = "sale.order.line"
    _description = "product details"

    def open_wizard(self):
        self.ensure_one()
        disc = {
            "name": "replace product",
            "type": "ir.actions.act_window",
            "res_model": "sh.replace.product",
            "view_mode": "form",
            "context":{
                "default_name":self.product_id.name,
                "default_alternative_products_ids":[rec.id for rec in self.product_id.alternative_products_ids]
            },
            "target":"new"
        }
        return disc
