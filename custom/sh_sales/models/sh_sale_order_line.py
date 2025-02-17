from odoo import fields, models, api


class sh_sales_order_line(models.Model):
    _name = "sh.sale.order.line"
    _description = "sale order line table"

    name = fields.Char(string="Name")
    product_id = fields.Many2one("sh.product.product", string="product")
    sale_order_id = fields.Many2one("sh.sale.order", string="partner")
    qty = fields.Integer(string="Qty")
    price = fields.Integer(string="Price")
    amount = fields.Float(string="Amount", compute="_cal_amount")
    tax_amount = fields.Float(string="Tax amount", compute="_cal_tax_amount")
    tax_ids = fields.Many2many("sh.account.tax", string="taxs")

    @api.onchange("product_id")
    def _cal_qty_price(self):
        if self.product_id:
            self.qty = self.product_id.qty
            self.price = self.product_id.price
            self.tax_ids = [(6, False, [p.id for p in self.product_id.tax_ids])]
            # self.tax_ids=self.product_id.tax_ids

    @api.depends("qty", "price")
    def _cal_amount(self):
        print("\n\n\n-----self------->", self)
        for rec in self:
            print("\n\n\n-----rec------->", rec)
            rec.amount = 0
            if rec.qty and rec.price:
                rec.amount = rec.qty * rec.price
            #     print('\n\n\n-----if---rec.amount------->',rec.amount)

    @api.depends("amount")
    def _cal_tax_amount(self):
        for rec in self:
            print("\n\n\n-111---------111->")
            amt_per = 0
            rec.tax_amount = 0
            for t_ids in rec.tax_ids:
                print("\n\n\n-222---------222->")
                print("\n\n\n-----t_ids------->", t_ids)
                amt_per += t_ids.tax_per
                print("\n\n\n-----t_ids.tax_per------->", t_ids.tax_per)
            rec.tax_amount = (rec.amount * amt_per) / 100
            print("\n\n\n-----rec.tax_amount------->", rec.tax_amount)
