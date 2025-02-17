from odoo import fields, models, api


class Employee_category(models.Model):
    _name = "sh.employee.category"
    _description = "employee category detailes"
    
    name = fields.Char(string="category name", required=True)
    ref = fields.Char(string="ref", required=True)