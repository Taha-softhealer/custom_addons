from odoo import fields, models, api


class sh_sales_order(models.Model):
    _name = "sh.sale.order"
    _description = "sale order table"

    name = fields.Char(
        string="Order id", default="New", required=True,readonly=True
    )
    date = fields.Date(string="Date", default=fields.Datetime.now)
    partner_id = fields.Many2one("sh.res.partner", string="partner", required=True)
    order_line_ids = fields.One2many(
        "sh.sale.order.line", "sale_order_id", string="order"
    )
    company_id=fields.Many2one("res.company",default=lambda self: self.env.company)
    company_data=fields.Char(company_dependent=True)
    total = fields.Float(string="Total:", compute="_cal_total")
    tax_total = fields.Float(string="Total Tax:", compute="_cal_tax_total")
    grand_total = fields.Float(string="Grand Total:",store=True , compute="_cal_grand_total")
    sh_text=fields.Json(string="text")
    tax_percen=fields.Char("tex")

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            rec = super(sh_sales_order, self).create(vals_list)
            string = ""
            string = "SH" + str(rec.id)
            print("\n\n\n-----string------->", string)
            rec.name = string
        return rec
        
    @api.depends("order_line_ids.amount")
    def _cal_total(self):
        for rec in self:
            rec.total = 0
            for line_total in rec.order_line_ids:
                rec.total += line_total.amount

    @api.depends("order_line_ids.tax_amount")
    def _cal_tax_total(self):
        for rec in self:
            rec.tax_total = 0
            rec.sh_text = {
                'sh_amount': 200
            }
            # print(rec.sh_text.get("sh_amount"))
            rec.tax_percen=rec.sh_text.get("sh_amount")
            print("\n\n\n-333---------333->")
            for line_total in rec.order_line_ids:
                rec.tax_total += line_total.tax_amount
            print("\n\n\n-----rec.tax_total------->", rec.tax_total)

    @api.depends("total", "tax_total")
    def _cal_grand_total(self):
        for rec in self:
            rec.grand_total = 0
            if rec.total and rec.tax_total:
                rec.grand_total = rec.total + rec.tax_total
