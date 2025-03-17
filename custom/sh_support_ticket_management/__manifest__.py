# -*- coding: utf-8 -*-
# Part of Softhealer Technologies. See LICENSE file for full copyright and licensing details.
{
    "name": "sh support ticket",
    "version": "1.0",
    "summary": "support ticket system",
    "description": "basic support ticket system",
    "category": "Productivity",
    "website": "https://www.softhealer.com",
    "depends": ["base_setup", "web"],
    "data": [
        "security/ir.model.access.csv",
        "views/sh_support_ticket_views.xml",
        "views/sh_support_ticket_menuitem.xml"
    ],
    "installable": True,
    "application": True,
}
