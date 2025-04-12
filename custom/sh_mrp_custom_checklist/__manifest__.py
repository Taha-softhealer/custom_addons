# -*- coding: utf-8 -*-
# Part of Softhealer Technologies. See LICENSE file for full copyright and licensing details.
{
    "name": "sh_mrp_custom_checklist",
    "version": "1.0",
    "summary": "MRP custom checklist",
    "description": "MRP custom checklist generation",
    "category": "Manufacturing",
    "website": "https://www.softhealer.com",
    "depends": [
        "base_setup",
        "web",
        "mail",
        "mrp",
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/sh_mrp_custom_checklist.xml",
        "views/sh_manufacturing_checklist_view.xml",
        "views/sh_manufacturing_template.xml",
        "views/sh_manufacturing_order_form.xml",
        "views/sh_manufacturing_order_line.xml",
        "views/sh_manufacturing_views.xml",
        "views/sh_import_checklist_wizard.xml",
        "views/sh_manufacturing_menuitem.xml",
    ],
    "installable": True,
    "application": True,
}
