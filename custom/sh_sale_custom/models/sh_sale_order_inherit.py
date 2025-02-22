from odoo import fields, models, api


class sh_sale_order_inherit(models.Model):
    _inherit = "sale.order"
    _description = "sales note details"
                    
    custom_note=fields.Many2many("sh.note",string="Note")
    sh_sr_num=fields.Integer("abcd")
    
    @api.onchange("partner_id")
    def _change_note(self):
        # self.custom_note=self.partner_id.custom_note
        self.custom_note=[(6, False, [p.id for p in self.partner_id.custom_note])]
        print('\n\n\n-----self.partner_id.custom_note------->',self.partner_id.custom_note)
    
    
    
    @api.onchange("order_line")
    def __count_sr(self):
        count=0
        for rec in self.order_line:
            rec.sr_num=count
            count+=1
            print('\n\n\n-----rec.sr_num------->',rec.sr_num)
