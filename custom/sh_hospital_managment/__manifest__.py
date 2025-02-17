# -*- coding: utf-8 -*-
# Part of Softhealer Technologies. See LICENSE file for full copyright and licensing details.
{
    "name": "sh_hospital_management",
    "version": "2.0",
    "summary": "hospital management system",
    "description": "basic hospital management system",
    "category": "Productivity/Employee",
    "website": "https://www.softhealer.com",
    "depends": ["base_setup", "web"],
    "data": [
        "security/ir.model.access.csv",
        "views/sh_patient.xml",
        "views/sh_diagnosis.xml",
        "views/sh_doctor.xml",
    ],
    "installable": True,
    "application": True,
}
