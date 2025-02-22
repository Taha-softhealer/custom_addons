from odoo import fields, models, api
from datetime import datetime
from odoo.exceptions import UserError  # type: ignore


class sh_student(models.Model):
    _name = "sh.search"
    _description = "search table"

    name = fields.Char(string="Name", required=True)
    select_member = fields.Many2one("sh.library.member", string="select a member")
    select_category = fields.Many2one("sh.library.category", string="select a category")
    enter_number = fields.Integer(string="Enter the number of book")


    
    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            if vals.get("select_member"):
                rec = self.env["sh.library.member"].browse(vals["select_member"])
                for i in rec.book_ids:
                    print('\n\n\n-----i.book_ids.name------->',i.name)

            if vals.get("select_category"):
                rec = self.env["sh.library.category"].browse(vals["select_category"])
                rec.books.search([()])

            if vals.get("enter_number"):
                rec = self.env["sh.library.member"].search(
                    [("total_issued_book", ">", vals["enter_number"])]
                )
                for i in rec:
                    print('\n\n\n-----rec------->',i.name)
        res= super().create(vals_list)
        return res
    # lines = self.env['account.bank.statement.line'].search(
    #             domain=[
    #                 ('internal_index', '<=', current_st_line.internal_index),
    #                 ('internal_index', '>', line_before.internal_index or ''),
    #                 ('journal_id', '=', current_st_line.journal_id.id),
    #             ],
    #             order='internal_index desc',
    #         )
