from odoo import fields, models, api


class sh_sale_order_inherit(models.Model):
    _inherit = "sale.order"
    _description = "sales note details"
                    
    custom_note=fields.Many2many("sh.note",string="Note")
    sh_sr_num=fields.Integer("abcd")
    
    @api.onchange("order_line")
    def __count_sr(self):
        count=0
        for rec in self.order_line:
            rec.sr_num=count
            count+=1
            print('\n\n\n-----rec.sr_num------->',rec.sr_num)
