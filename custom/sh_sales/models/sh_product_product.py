from odoo import fields, models, api


class sh_product_product(models.Model):
    _name = "sh.product.product"
    _description = "product table"
    
    name=fields.Char(string="Name", required=True)
    qty = fields.Integer(string="Qty")
    price = fields.Integer(string="Price")
    tax_ids = fields.Many2many("sh.account.tax", string="taxs")