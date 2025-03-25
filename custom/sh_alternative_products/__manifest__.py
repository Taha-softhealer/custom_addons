# -*- coding: utf-8 -*-
# Part of Softhealer Technologies. See LICENSE file for full copyright and licensing details.
{
    "name": "sh_alternative_product",
    "version": "1.0",
    "summary": "alternative product managemnt system",
    "description": "basic alternative product managemnt system",
    "category": "Sales",
    "website": "https://www.softhealer.com",
    "depends": ["base_setup", "web", "mail", "stock", "sale_management", "account"],
    "data": [
        "security/ir.model.access.csv",
        "security/sh_alternative_product_security.xml",
        "views/sh_replace_product.xml",
        "views/sh_product_template_inherit.xml",
        "views/sh_sale_order_line_inherit.xml",
    ],
    "installable": True,
    "application": True,
}
