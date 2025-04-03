# -*- coding: utf-8 -*-
# Part of Softhealer Technologies. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from datetime import timedelta


class sh_sale_order(models.Model):

    _inherit = "sale.order"
    _description = "Sale order "

    name = fields.Char(string="Name")
    sh_sale_order_line_ids = fields.One2many("sale.order.line", "sh_sale_order_id")

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        res_ls = []
        if self.partner_id:
            print(
                "\n\n\n-----self.partner_id.sale_order_ids------->",
                self.partner_id.sale_order_ids,
            )

            for rec in self.partner_id.sale_order_ids:
                if rec.id != self.id:
                    for i in rec.order_line:
                        res_ls.append(i.id)
            print("\n\n\n-----res_ls------->", res_ls)

            if (
                self.company_id.last_no_days
                or self.company_id.last_no_order
                or self.company_id.sale_order_states_ids
            ):
                last_days = (
                    fields.Date.today() - timedelta(days=self.company_id.last_no_days)
                ).strftime("%Y-%m-%d")
                record = self.env["sale.order.line"].browse(res_ls)
                searched = record.search(
                    [
                        ("order_date", ">=", last_days),
                        (
                            "state",
                            "in",
                            (
                                [
                                    state.value
                                    for state in self.company_id.sale_order_states_ids
                                ]
                            ),
                        ),
                    ],
                    limit=self.company_id.last_no_order,
                    order="order_date desc",
                )
                self.sh_sale_order_line_ids = [(6, 0, [i.id for i in searched])]
            else:
                self.sh_sale_order_line_ids = [(6, 0, res_ls)]

    def all_line_order(self):
        record = self.sh_sale_order_line_ids.search([("line_reorder", "=", True)])
        if record:
            for rec in record:
                rec.re_order()
                rec.line_reorder = False
        else:
            for rec in self.sh_sale_order_line_ids:
                rec.re_order()


class sh_sale_order_line(models.Model):

    _inherit = "sale.order.line"
    _description = "Sale order "

    sh_sale_order_id = fields.Many2one("sale.order")
    order_date = fields.Datetime(string="Order Date", related="order_id.date_order")
    line_reorder = fields.Boolean(readonly=False)
    enable_reorder = fields.Boolean(related="company_id.enable_reorder")

    def open_order(self):
        self.ensure_one()
        disc = {
            "name": "Sale order",
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "res_id": self.order_id.id,
            "view_mode": "form",
        }
        return disc

    def re_order(self):
        if not self.sh_sale_order_id:
            self.env["bus.bus"]._sendone(
                self.env.user.partner_id,
                "simple_notification",
                {
                    "type": "danger",
                    "title": "Save",
                    "message": "Please save your changes first",
                },
            )
        else:
            self.create(
                {
                    "product_id": self.product_id.id,
                    "product_uom_qty": self.product_uom_qty,
                    "product_uom": self.product_uom.id,
                    "price_unit": self.price_unit,
                    "order_id": self.sh_sale_order_id.id,
                    "name": self.product_id.name,
                }
            )
