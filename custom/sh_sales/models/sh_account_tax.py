from odoo import fields, models, api


class sh_account_tax(models.Model):
    _name = "sh.account.tax"
    _description = "account tax table"
    
    name=fields.Char(string="Name", required=True)
    tax_per=fields.Integer(string="Tax percentage", required=True)
    sale_order_line_ids=fields.Many2many("sh.sale.order.line")
    product_line_ids=fields.Many2many("sh.product.product")