# -*- coding: utf-8 -*-
# Part of Softhealer Technologies. See LICENSE file for full copyright and licensing details.
{
    "name": "sh_music_academy",
    "version": "1.0",
    "summary": "music academy management system",
    "description": "music academy student, lesson and course management system",
    "category": "Music",
    "website": "https://www.softhealer.com",
    "depends": ["base_setup", "web", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/sh_student.xml",
        "views/sh_menuitems.xml",
    ],
    # "image":["static/description/download.jpeg"],
    "installable": True,
    "application": True,
}
