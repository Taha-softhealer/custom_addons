# -*- coding: utf-8 -*-
# Part of Softhealer Technologies. See LICENSE file for full copyright and licensing details.
{
    "name": "sh_sale_order_history",
    "version": "1.0",
    "summary": "sale order history system",
    "description": "basic sale order history system",
    "category": "Sales",
    "website": "https://www.softhealer.com",
    "depends": ["base_setup", "web", "mail", "sale_management", "account"],
    "data": [
        "views/res_config_form.xml",
        "views/sh_sale_order.xml"
    ],
    "installable": True,
    "application": True,
}
