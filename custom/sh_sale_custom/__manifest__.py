# -*- coding: utf-8 -*-
# Part of Softhealer Technologies. See LICENSE file for full copyright and licensing details.
{
    "name": "sh_sale_custom",
    "version": "2.0",
    "summary": "sh sale Custom module",
    "description": " basic sale Custom module",
    "category": "Sales",
    "website": "https://www.softhealer.com",
    "depends": ["base_setup", "web", "sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/sh_note.xml",
        "views/sh_sale_order_inherit.xml",
        "views/sh_sale_order_line_inherit.xml"
    ],
    "installable": True,
    "application": True,
}
