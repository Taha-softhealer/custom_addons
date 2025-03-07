# -*- coding: utf-8 -*-
# Part of Softhealer Technologies. See LICENSE file for full copyright and licensing details.
{
    "name": "sh_timesheet_managment",
    "version": "1.0",
    "summary": "Timesheet managment system",
    "description": "basic timesheet managment system",
    "category": "Timesheet",
    "website": "https://www.softhealer.com",
    "depends": ["base_setup", "web","mail"],
    "data": [
        "security/sh_timesheet_security.xml",
        "security/ir.model.access.csv",
        "views/sh_res_user_inherit.xml",
        "views/sh_reject_reason_views.xml",
        "views/sh_timesheet_view.xml",
        "views/sh_task_view.xml",
        "views/sh_tag_view.xml",
    ],
    "installable": True,
    "application": True,
}
