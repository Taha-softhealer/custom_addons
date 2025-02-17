from odoo import fields, models, api
from odoo.exceptions import UserError  # type: ignore
from datetime import datetime, timedelta

class sh_member(models.Model):
    _name = "sh.library.borrowing"
    _description = "borrowing details"

    name = fields.Char(string="Name")
    member_id = fields.Many2one("sh.library.member", string="Member id")
    book_ids = fields.Many2one("sh.library.book", string="book ids")
    borrow_date = fields.Date(string="Borrow Date", default=fields.Datetime.now)
    return_date = fields.Date(string="Return Date",readonly=True)
    state = fields.Selection(
        [("borrowed", "Borrowed"), ("returned", "Returned")],
        required=True
    )





    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            print('\n\n\n-----vals------->',vals)
            vals["return_date"]=datetime.now() + timedelta(days=15)
            if vals.get("book_ids"):
                record=self.env["sh.library.book"].search([("id", "=", vals["book_ids"])])
                if(not (record.availabele_book_count>0)):
                    raise UserError(f"There is no {record.name} left to render member")
                else:
                    record.availabele_book_count-=1
        result=super(sh_member,self).create(vals_list)
        return result
    
    def write(self,vals):
        if vals.get('state')=="returned":
            self.book_ids.availabele_book_count+=1
            
        result=super(sh_member,self).write(vals)
        return result