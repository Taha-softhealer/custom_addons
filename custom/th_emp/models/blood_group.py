from odoo import fields, models, api


class blood_group(models.Model):
    _name = "sh.blood.group"
    _description = "blood group table"
    
    name=fields.Char(string="Blood type", required=True)
    employee_ids = fields.One2many('sh.employee', 'blood_group_model', string='employee')