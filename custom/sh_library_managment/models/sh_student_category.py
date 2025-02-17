from odoo import fields, models, api


class sh_student_category(models.Model):
    _name = "sh.category"
    _description = "sudent category table"
    
    name=fields.Char(string="Name", required=True)
    min_age=fields.Integer(string="min age")
    max_age=fields.Integer(string="max age")


    @api.model_create_multi
    def create(self, vals_list):
        print('\n\n\n-----vals_list------->',vals_list)
        print('\n\n\n-----self------->',self)
        res=super().create(vals_list)
        return res