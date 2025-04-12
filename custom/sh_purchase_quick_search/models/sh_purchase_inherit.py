from odoo import _, api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    search_by_vendor = fields.Selection([('current_vendor', 'Current Vendor'),('all', 'All')],default="all")
    search_input = fields.Char()
    search_by_filter = fields.Selection([('all', 'All'),('name', 'Name'),('internal_reference', 'Internal Reference'),('barcode','Barcode'),('vender_product_name','Vender Product Name'),('vender_product_code','Vender Product Code'),('attribute','Attribute'),('attribute_value','Attribute Value')],default="all")
    
    def test(self):
        print('\n\n\n-----self------->',self)