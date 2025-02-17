from odoo import fields, models, api


class sh_doctor(models.Model):
    _name = "sh.doctor"
    _description = "doctor table"
    
    name=fields.Char(string="Name", required=True)
    specialization=fields.Char(string="specialization", required=True)
    patient_ids=fields.One2many("sh.patient","doctor_id",string="patients")
    # patients=