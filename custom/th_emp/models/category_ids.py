from odoo import fields, models


class employee_category(models.Model):
    _name = "sh.resource.calendar"
    _description = "employee category"

    name = fields.Char(string="Name")
    Active = fields.Boolean(string="Active")
    color = fields.Integer(string="color")
    employee_ids = fields.Many2many("sh.employee")
