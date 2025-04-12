# -*- coding: utf-8 -*-
# Part of Softhealer Technologies. See LICENSE file for full copyright and licensing details.
{
    "name": "sh_backdated_timesheet",
    "version": "1.0",
    "summary": "backdated timesheet creation system",
    "description": "basic backdated timesheet creation system",
    "category": "Timesheet",
    "website": "https://www.softhealer.com",
    "depends": ["base_setup", "web", "timesheet_grid"],
    "data": ["security/sh_backdated_timesheet_security.xml", "views/res_setting.xml"],
    "installable": True,
    "application": True,
}
