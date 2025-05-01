from odoo import _, api, fields, models, Command


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    search_by_vendor = fields.Selection(
        [("current_vendor", "Current Vendor"), ("all", "All")], default="all"
    )
    search_input = fields.Char()
    search_by_filter = fields.Selection(
        [
            ("all", "All"),
            ("name", "Name"),
            ("internal_reference", "Internal Reference"),
            ("barcode", "Barcode"),
            ("vender_product_name", "Vender Product Name"),
            ("vender_product_code", "Vender Product Code"),
            ("attribute", "Attribute"),
            ("attribute_value", "Attribute Value"),
        ],
        default="all",
    )
    # sh_product_ids = fields.One2many("product.product", "sh_purchase_order_id")
    # sh_purchase_order_line_ids = fields.One2many('purchase.order.line', 'sh_purchase_order_id')
    sh_purchase_order_line_ids = fields.One2many(
        "sh.purchase.order.line", "sh_purchase_order_id"
    )
    
    def add_selected_lines(self):
        record=self.sh_purchase_order_line_ids.search([("sh_multi_add","=",True)])
        for rec in record:
            rec.single_product()
            rec.sh_multi_add=False

    def test(self):
        domain = []

        if self.search_by_filter == "all":
            record = self.env["product.product"].search(domain)
            for rec in record:
                print("\n\n\n-----rec------->", rec)
                self.sh_purchase_order_line_ids = [
                    Command.create({"product_id": rec.id})
                ]

        elif self.search_by_filter == "name":
            ele = ("name", "ilike", self.search_input)
            domain.append(ele)
            record = self.env["product.product"].search(domain)
            for rec in record:
                print("\n\n\n-----rec------->", rec)
                self.sh_purchase_order_line_ids = [
                    Command.create({"product_id": rec.id})
                ]

        elif self.search_by_filter == "internal_reference":
            ele = ("default_code", "=", self.search_input)
            domain.append(ele)
            record = self.env["product.product"].search(domain)
            for rec in record:
                print("\n\n\n-----rec------->", rec)
                self.sh_purchase_order_line_ids = [
                    Command.create({"product_id": rec.id})
                ]

        elif self.search_by_filter == "barcode":
            ele = ("barcode", "=", self.search_input)
            domain.append(ele)
            record = self.env["product.product"].search(domain)
            for rec in record:
                print("\n\n\n-----rec------->", rec)
                self.sh_purchase_order_line_ids = [
                    Command.create({"product_id": rec.id})
                ]

        elif self.search_by_filter == "attribute":
            ele = ("barcode", "=", self.search_input)
            domain.append(ele)
            record = self.env["product.template"].search(domain)

            for rec in record:
                print("\n\n\n-----rec------->", rec)
                self.sh_purchase_order_line_ids = [
                    Command.create({"product_id": rec.id})
                ]
        print("\n\n\n-----self(vendor)------->", self.search_by_vendor)
        print("\n\n\n-----self(filter)------->", self.search_by_filter)


# class PurchaseOrderLine(models.Model):
#     _inherit = "purchase.order.line"

#     sh_purchase_order_id = fields.Many2one(
#         "purchase.order",
#         string="Sh PUrchase Order",
#     )
#     sh_cost = fields.Float(string="Cost", related="product_id.standard_price")
#     sh_unit_price = fields.Float(string="Unit Price", related="product_id.list_price")
#     sh_on_hand = fields.Float(related="product_id.qty_available")
#     sh_forcast_qty = fields.Float(related="product_id.virtual_available")
#     sh_multi_add = fields.Boolean(string="Multi Add")


class ShPurchaseOrderLine(models.Model):
    _name = "sh.purchase.order.line"
    _description = "product search line"

    name = fields.Char(string="name")
    description = fields.Char(related="product_id.name")
    product_id = fields.Many2one(
        "product.product",
        string="product",
    )
    sh_purchase_order_id = fields.Many2one(
        "purchase.order",
        string="Sh PUrchase Order",
    )
    sh_cost = fields.Float(string="Cost", related="product_id.standard_price")
    sh_unit_price = fields.Float(string="Unit Price", related="product_id.list_price")
    sh_on_hand = fields.Float(related="product_id.qty_available")
    sh_forcast_qty = fields.Float(related="product_id.virtual_available")
    sh_multi_add = fields.Boolean(string="Multi Add")

    def single_product(self):
        is_product=False
        for rec in self.sh_purchase_order_id.order_line:
            if rec.product_id.id == self.product_id.id:
                rec.product_qty = rec.product_qty + 1.00
                is_product = True
        if not is_product:
            self.sh_purchase_order_id.order_line = [
                Command.create(
                    {
                        "product_id": self.product_id.id,
                        "order_id": self.sh_purchase_order_id.id,
                    }
                )
            ]
