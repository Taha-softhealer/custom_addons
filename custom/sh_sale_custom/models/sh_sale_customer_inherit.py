from odoo import fields, models, api


class sh_sale_order_inherit(models.Model):
    _inherit = "res.partner"
    _description = "res partner details"
                    
    custom_note=fields.Many2many("sh.note",string="Note")