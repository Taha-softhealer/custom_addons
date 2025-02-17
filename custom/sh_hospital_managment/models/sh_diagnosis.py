from odoo import fields, models, api


class sh_diagnosis(models.Model):
    _name = "sh.diagnosis"
    _description = "diagnosis table"
    
    name=fields.Char(string="Name", required=True)
    patients_ids=fields.Many2many("sh.patient",string="patients")