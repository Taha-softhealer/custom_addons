from odoo import fields, models, api
from odoo.exceptions import UserError  # type: ignore
from dateutil.relativedelta import relativedelta


class sh_sale_order(models.Model):
    _inherit = "sale.order"

    warranty_applicable = fields.Boolean("warranty applicable")
    warranty_period = fields.Integer(string="warranty period in months", default="12")
    warranty_expiry_date = fields.Date(
        string="warranty expiry date", compute="_compute_warranty_expiry_date"
    )

    @api.onchange("warranty_period")
    def onchange_warranty_period(self):
        if (self.warranty_period) < 6:
            warning = {
                "warning": {
                    "title": (
                        "Warranty period is not sufficient"
                    ),
                    "message": ("warranty period is less than 6 months."),
                }
            }
            return warning
            # raise UserError("warranty period is less than 6 months")

    @api.model_create_multi
    def create(self, vals_list):
        rec = super(sh_sale_order, self).create(vals_list)
        if rec.warranty_applicable:
            temp = self.env["sh.sale.warranty"].create(
                {
                    "name": rec.name,
                    "order_date": rec.date_order,
                    "warranty_period": rec.warranty_period,
                    "sale_order_id": rec.id,
                }
            )
        return rec

    def write(self, values):
        temp = self.env["sh.sale.warranty"].search([("name", "=", self.name)])
        if values.get("warranty_applicable") == True:
            self.env["sh.sale.warranty"].create(
                {
                    "name": self.name,
                    "order_date": values.get("date_order") or self.date_order,
                    "warranty_period": values.get("warranty_period")
                    or self.warranty_period,
                    "sale_order_id": self.id,
                }
            )
        if values.get("warranty_applicable") == False:
            temp.unlink()
            print("\n\n\n-hahaha---------hahaha->")
        if values.get("date_order"):
            temp.order_date = values.get("date_order")
            temp.warranty_expiry_date = values.get("warranty_expiry_date")

        if values.get("warranty_period"):
            temp.warranty_period = values.get("warranty_period")
            temp.warranty_expiry_date = values.get("warranty_expiry_date")

        res = super().write(values)
        return res

    @api.depends("date_order", "warranty_period")
    def _compute_warranty_expiry_date(self):
        for record in self:
            print(
                '\n\n\n-----record["warranty_period"]------->',
                record["warranty_period"],
            )
            print('\n\n\n-----record["order_date"]------->', record["date_order"])
            record.warranty_expiry_date = record["date_order"] + relativedelta(
                months=record["warranty_period"]
            )

    def warranty_reader(self):
        self.ensure_one()
        record = self.env["sh.sale.warranty"].search([("name", "=", self.name)])
        print("\n\n\n-----record------->", record)
        print(
            "\n\n\n-hhh----self.name------hhh->",
        )
        disc = {
            "name": "Journal Items",
            "type": "ir.actions.act_window",
            "res_model": "sh.sale.warranty",
            "view_mode": "form",
            "res_id": record.id,
        }
        print('\n\n\n-----disc["domain"]------->', disc["res_id"])
        return disc
