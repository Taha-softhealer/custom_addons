from odoo import fields, models, api


class sh_member(models.Model):
    _name = "sh.library.member"
    _description = "member details"

    name = fields.Char(string="Name",required=True)
    mid = fields.Char(string="Member id",readonly=True,default="New")
    email = fields.Char(string="Email",required=True)
    phone = fields.Char(string="phone")
    book_ids = fields.Many2many("sh.library.book", string="books")
    member_type= fields.Char(string="Member Type",compute="_compute_type")

    @api.model_create_multi
    def create(self, vals_list):
        rec = super(sh_member, self).create(vals_list)
        string = "SHL" + str(rec.id)
        print("\n\n\n-----string------->", string)
        rec.mid = string
        return rec

    @api.depends("book_ids")
    def _compute_type(self):
        for rec in self:
            if(len(rec.book_ids)>=3):
                rec.member_type="Premium"
            else:
                rec.member_type="Regular"