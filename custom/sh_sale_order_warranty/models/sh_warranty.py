from odoo import fields, models, api
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class sh_sale_warranty(models.Model):
    _name = "sh.sale.warranty"
    _description = "Tracks warranty details of products sold"

    name = fields.Char(string="warranty")
    sale_order_id = fields.Many2one("sale.order", string="sale_order")
    order_date = fields.Datetime("order date")
    warranty_period = fields.Integer(string="warranty period in months")
    warranty_expiry_date = fields.Date(
        related="sale_order_id.warranty_expiry_date"
    )
