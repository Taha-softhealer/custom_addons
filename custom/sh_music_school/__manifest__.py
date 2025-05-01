# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Music Academy Management",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Industries",
    "license": "OPL-1",
    "summary": "Music Academy Management Academy of music Curriculum for music academy management Music School Management Music school administration Music education Courses in music education Music academy programs Music teaching academy Instrumental instruction Music theory school Music Institute Management System Music Classes Management System Manage Music Classes Music Academy Management App Music Academy Management Software Music School software Student Management Odoo",
    "description": """Are you tired of managing your music school with outdated techniques? We have an amazing module for you! Our module allows you to effortlessly manage classes, lessons, attendance, and invoicing. You can also handle student, teacher, instrument, and service details with ease. Additionally, generating PDF attendance reports is quick and simple!""",
    "version": "0.0.1",
    "depends": ["sale", "account", "hr", "calendar", "maintenance","base"],
    "application": True,
    "data": [
        "security/school_security.xml",
        "security/ir.model.access.csv",
        "views/sh_school_student_views.xml",
        "wizard/sh_students_wizard.xml",
        "wizard/sh_create_attendance_wizard.xml",        
        "views/sh_class_lesson_line.xml",
        "views/sh_school_classes_views.xml",
        "views/sh_school_lessons_views.xml",
        "views/sh_school_attendance_views.xml",
        "views/hr_employee.xml",
        "views/product_product.xml",
        "views/account_move.xml",
        "wizard/sh_reporting_view.xml",
        "report/ir_actions_report.xml",
        "report/class_report.xml",
        "views/res_config_setting_views.xml",
        "views/all_menu.xml"
    ],
    "images": ["static/description/background.png", ],
    "auto_install": False,
    "installable": True,
    "price": 183,
    "currency": "EUR"
}
