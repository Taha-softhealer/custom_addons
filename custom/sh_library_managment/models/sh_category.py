from odoo import fields, models, api


class sh_category(models.Model):
    _name = "sh.library.category"
    _description = "category details"
    
    name = fields.Char(string="Name",required=True)
    description=fields.Char(string="description")
    books = fields.One2many("sh.library.book", "category_id", string="books")
    total_books = fields.Integer(
        string="Total book", readonly=True, compute="_compute_total"
    )

    @api.depends("books")
    def _compute_total(self):
        for rec in self:
            rec.total_books = len(rec.books)
