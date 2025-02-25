# -*- coding: utf-8 -*-
# Part of Softhealer Technologies. See LICENSE file for full copyright and licensing details.
{
    "name": "sh_sale_order_warranty",
    "version": "1.0",
    "summary": "sale order warranty management system",
    "description": "sale order warranty creation and expiration management system",
    "category": "Sale",
    "website": "https://www.softhealer.com",
    "depends": ["base_setup", "web", "sale", "sale_management", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/sh_warranty_view.xml",
        "views/sh_sale_order_inherit.xml",
        "views/sh_sale_warranty_menu.xml",
    ],
    "installable": True,
    "application": True,
}
