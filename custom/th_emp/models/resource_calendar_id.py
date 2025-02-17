from odoo import fields, models


class calender:
    _name = "sh.resource.calendar"
    _description = "resource calendar"

    name = fields.Char(string="Name")
    active = fields.Boolean(string="Active")
    