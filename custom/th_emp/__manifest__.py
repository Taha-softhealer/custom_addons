# -*- coding: utf-8 -*-
# Part of Softhealer Technologies. See LICENSE file for full copyright and licensing details.
{
    "name": "sh_employee",
    "version": "2.0",
    "summary": "Employee management system",
    "description": "basic employee management system",
    "category": "Productivity/Employee",
    "website": "https://www.softhealer.com",
    "depends": ["base_setup", "web"],
    "data": [
        "security/ir.model.access.csv",
        "views/job_view.xml",
        "views/department_view.xml",
        "views/blood_group.xml",
        "views/category_view.xml",
        "views/employee_category.xml",
        "views/sh_job_report.xml",
        "views/sh_employee.xml"
    ],
    "installable": True,
    "application": True,
}
