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
    # warranty_expiry_date = fields.Date(
    #     string="warranty expiry date", compute="_compute_warranty_expiry_date"
    # )

    @api.depends("order_date", "warranty_period")
    def _compute_warranty_expiry_date(self):
        for record in self:
            print('\n\n\n-----record["warranty_period"]------->',record["warranty_period"])
            print('\n\n\n-----record["order_date"]------->',record["order_date"])
            record.warranty_expiry_date = record["order_date"] + relativedelta(months=record["warranty_period"])