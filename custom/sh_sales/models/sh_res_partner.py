from odoo import fields, models, api


class sh_res_partner(models.Model):
    _name = "sh.res.partner"
    _description = "partner table"
    
    name=fields.Char(string="Name", required=True)
    city=fields.Char(string="City", required=True)