# -*- coding: utf-8 -*-
# Part of Softhealer Technologies. See LICENSE file for full copyright and licensing details.
{
    "name": "sh_meeting_auto_timesheet",
    "version": "1.0",
    "summary": "Meeting Auto Timesheet",
    "description": "Meeting auto timesheet generation",
    "category": "Timesheet",
    "website": "https://www.softhealer.com",
    "depends": ["base_setup", "web", "mail", "calendar", "hr", "project","timesheet_grid"],
    "data": [
        "security/sh_meeting_auto_timesheet_security.xml",
        "views/sh_calender_inherit.xml",
    ],
    "installable": True,
    "application": True,
}
