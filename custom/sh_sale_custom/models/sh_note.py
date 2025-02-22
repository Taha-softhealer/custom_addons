from odoo import fields, models, api


class sh_note(models.Model):
    _name = "sh.note"
    _description = "sales note details"
    
    name = fields.Char(string="name",required=True)
    custom_note_partner=fields.Many2many("res.partner",string="Note")