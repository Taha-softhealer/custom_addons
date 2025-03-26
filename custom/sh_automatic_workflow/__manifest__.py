# -*- coding: utf-8 -*-
# Part of Softhealer Technologies. See LICENSE file for full copyright and licensing details.
{
    "name": "sh_automatic_workflow",
    "version": "1.0",
    "summary": "automatic sale workflow system",
    "description": "basic automatic sale workflow system",
    "category": "Sales",
    "website": "https://www.softhealer.com",
    "depends": ["base_setup", "web", "mail", "stock", "sale_management", "account"],
    "data": ["security/ir.model.access.csv","views/sh_automatic_workflow_view.xml","views/res_config_form.xml"],
    "installable": True,
    "application": True,
}
