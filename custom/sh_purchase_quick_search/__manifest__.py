# -*- coding: utf-8 -*-
# Part of Softhealer Technologies. See LICENSE file for full copyright and licensing details.
{
    "name": "sh_purchase_quick_search",
    "version": "1.0",
    "summary": "Purchase product quick search",
    "description": "Purchase product quick search",
    "category": "Purchase",
    "website": "https://www.softhealer.com",
    "depends": [
        "base_setup",
        "web",
        "purchase",
        "mail",
        "stock",
        "sale_management",
        "account"
    ],
    "data": ["views/sh_purchase_inherit.xml"],
    "installable": True,
    "application": True,
}
