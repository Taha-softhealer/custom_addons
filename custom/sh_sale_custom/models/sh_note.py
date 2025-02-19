from odoo import fields, models, api


class sh_note(models.Model):
    _name = "sh.note"
    _description = "sales note details"
    
    name = fields.Char(string="ref",required=True)
