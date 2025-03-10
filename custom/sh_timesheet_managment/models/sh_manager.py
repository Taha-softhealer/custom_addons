from odoo import fields, models, api


class sh_manager(models.Model):
    _name = "sh.manager"
    _description = "manager details"

    name = fields.Char()
