from odoo import fields, models, api


class sh_patient(models.Model):
    _name = "sh.patient"
    _description = "patient table"
    
    name=fields.Char(string="Name", required=True)
    age=fields.Integer(string="Age")
    doctor_id=fields.Many2one("sh.doctor",string="doctor")
    diagnosis_ids=fields.Many2many("sh.diagnosis",string="diagnosis")
