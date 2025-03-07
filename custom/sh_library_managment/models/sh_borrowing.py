from odoo import fields, models, api
from odoo.exceptions import UserError  # type: ignore
from datetime import datetime, timedelta


class sh_member(models.Model):
    _name = "sh.library.borrowing"
    _description = "borrowing details"

    name = fields.Char(string="Name")
    member_id = fields.Many2one("sh.library.member", string="Member id", required=True)
    book_ids = fields.Many2one("sh.library.book", string="book ids", required=True)
    borrow_date = fields.Date(string="Borrow Date", default=fields.Datetime.now)
    return_date = fields.Date(string="Return Date", readonly=True)
    state = fields.Selection(
        [("borrowed", "Borrowed"), ("returned", "Returned")], required=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        print('\n\n\n-----self------->',self)
        for vals in vals_list:
            print("\n\n\n-----vals------->", vals)
            if vals.get("state") == "returned":
                raise UserError("you can not return a book before borrowing")
            vals["return_date"] = datetime.now() + timedelta(days=15)
            if vals.get("state") == "borrowed":
                if vals.get("member_id"):
                    record = self.env["sh.library.member"].browse(vals["member_id"])
                    if record.total_issued_book > 5:
                        raise UserError(
                            "This member has reached to the borrowing limit"
                        )

                if vals.get("book_ids"):
                    record = self.env["sh.library.book"].browse(vals["book_ids"])
                    for rec in record.member_ids:
                        if vals.get("member_id") == rec.id:
                            raise UserError("Book is already assign to Member")
                    if not (record.availabele_book_count > 0):
                        raise UserError(
                            f"There is no {record.name} left to render member"
                        )
                    else:
                        record.availabele_book_count -= 1
                        print("\n\n\n------------>", vals.get("member_id"))
                        record.member_ids = [(4, vals.get("member_id"))]
                        # self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
                        #     'type': 'success',
                        #     'title': "Success",
                        #     'message': "book issued sucessfully"
        print("\n\n\n-create calling---------create calling->")  # })
        result = super(sh_member, self).create(vals_list)
        return result

    def write(self, vals):
        print("\n\n\n-----self------->", self)
        print("\n\n\n-----vals------->", vals)
        if vals.get("book_ids") or vals.get("member_id"):
            raise UserError(
                "once book is borrowed you can not change book or member!!!"
            )
        if vals.get("state") == "returned":
            self.book_ids.availabele_book_count += 1
            self.book_ids.member_ids = [(3, self.member_id.id)]
            
        if vals.get("state") == "borrowed":
            self.book_ids.availabele_book_count -= 1
            self.book_ids.member_ids = [(4, self.member_id.id)]
                        
        result = super(sh_member, self).write(vals)
        return result

    def borrow(self):
        if self.member_id.total_issued_book < 5 and self.state == "borrowed":
            self.env["bus.bus"]._sendone(
                self.env.user.partner_id,
                "simple_notification",
                {
                    "type": "success",
                    "title": ("Success"),
                    "message": "This member can borrow book",
                },
            )
