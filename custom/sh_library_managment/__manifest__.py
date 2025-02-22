# -*- coding: utf-8 -*-
# Part of Softhealer Technologies. See LICENSE file for full copyright and licensing details.
{
    "name": "sh_library_managment",
    "version": "2.0",
    "summary": "library management system",
    "description": "basic library management system",
    "category": "Productivity/Employee",
    "website": "https://www.softhealer.com",
    "depends": ["base_setup", "web", "portal", "mail","sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/sh_category.xml",
        "views/sh_student_category.xml",
        "views/sh_borrowing.xml",
        "views/sh_student.xml",
        "views/sh_member.xml",
        "views/sh_search.xml",
        "views/sh_book.xml",
    ],
    "installable": True,
    "application": True,
}
