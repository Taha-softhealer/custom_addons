from odoo import fields, models, api
from odoo.exceptions import UserError  # type: ignore


SALE_ORDER_STATE = [
    ("available", "Available"),
    ("borrowed", "Borrowed"),
]
# compute="_count_available"


class sh_book(models.Model):
    _name = "sh.library.book"
    _description = "book details"
    _inherit = ["mail.thread"]

    # total_book_count = fields.Integer(string="Total books")
    availabele_book_count = fields.Integer(
        string="Availabel books",
        tracking=True,
    )
    name = fields.Char(
        string="Name",
        required=True,
        tracking=True,
    )
    author = fields.Char(string="Author")
    isbn = fields.Integer(string="isbn")
    published_date = fields.Date(string="published_date")
    category_id = fields.Many2one("sh.library.category", string="category")
    member_ids = fields.Many2many("sh.library.member", string="member")
    # state = fields.Selection(
    #     selection=SALE_ORDER_STATE,
    #     string="Status",
    #     default="available",
    #     readonly=True,
    #     tracking=True,
    # )

    # @api.depends("member_ids", "total_book_count")
    # def _count_available(self):
    #     for rec in self:
    #         if rec.total_book_count:
    #             rec.availabele_book_count = rec.total_book_count - len(self.member_ids)
    #         else:
    #             rec.availabele_book_count = 0

    # @api.onchange("member_ids")
    # def _member_change(self):
    #     if self.availabele_book_count < 0:
    #         # for i in self.member_ids:
    #         #     print("\n\n\n-----self.member_ids------->", type(i))
    #         raise UserError("There is no book left to render member")

    @api.onchange("name")
    def _onchange_name(self):
        # self.name
        print("\n\n\n-----self.name.lower()------->", self.name)
        if self.name:
            ls = self.name.split(" ")
            for rec in ls:
                string = rec
                compute_id = self.env["sh.library.category"].search_read(
                    domain=[("name", "ilike", string)], limit=1
                )
                print("\n\n\n-----compute_id------->", compute_id)
                if compute_id:
                    rec = compute_id[0]
                    self.category_id = rec["id"]

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if not val["category_id"]:
                raise UserError("please select catogery")
        rec = super(sh_book, self).create(vals_list)
        return rec

    def unlink(self):
        for rec in self:
            if len(rec.member_ids):
                raise UserError("You can't remove this book it is already assigned!!!")
            else:
                return super().unlink()

    # def write(self,vals):
    #     print('\n\n\n-----vals------->',vals)
    #     if not len(self.member_ids):
    #         vals["state"]="issue"
    #     return super().write(vals)

    # def borrow(self):
    #     if self.availabele_book_count > 0:
    #         self.state = "available"
    #     else:
    #         self.state = "borrowed"
    # if self.availabele_book_count<0:
    #     raise UserError("There is no book left to render member")
    # raise UserError("There is no book left to render member")
