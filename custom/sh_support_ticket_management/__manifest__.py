# -*- coding: utf-8 -*-
# Part of Softhealer Technologies. See LICENSE file for full copyright and licensing details.
{
    "name": "sh support ticket",
    "version": "1.0",
    "summary": "support ticket system",
    "description": "basic support ticket system",
    "category": "Productivity",
    "website": "https://www.softhealer.com",
    "depends": ["base_setup", "web", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "security/sh_support_ticket_security.xml",
        "views/sh_batch_update.xml",
        "views/sh_support_ticket_views.xml",
        "views/sh_support_ticket_menuitem.xml",
        "views/sequence_and_schedualing.xml",
    ],
    "installable": True,
    "application": True,
}
