# -*- coding: utf-8 -*-
# Part of Softhealer Technologies. See LICENSE file for full copyright and licensing details.
{
    "name": "sh_sales",
    "version": "1.0",
    "summary": "sales system",
    "description": "basic sales system",
    "category": "Productivity/Employee",
    "website": "https://www.softhealer.com",
    "depends": ["base_setup", "web"],
    "data": [
        "security/ir.model.access.csv",
        "views/sh_account_tax.xml",
        "views/sh_product_product.xml",
        "views/sh_sales_order.xml",
        "views/sh_sales_order_line.xml",
        "views/sh_res_partner.xml",
        "views/sh_sale_report.xml"
    ],
    "installable": True,
    "application": True,
}
