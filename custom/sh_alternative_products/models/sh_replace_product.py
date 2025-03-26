from odoo import fields, models, api
from odoo.exceptions import UserError  # type: ignore


class sh_replace_product(models.TransientModel):
    _name = "sh.replace.product"
    _description = "replace product reason"

    # def default_get(self, fields):
    #     res = super(sh_replace_product, self).default_get(fields)
    #     # Get context values
    #     print('\n\n\n-----parent_record.id------->',self.env.context)
    #     if self.env.context.get('default_product_id'):
    #         parent_record = self.env['product.template'].browse(self.env.context['default_product_id'])
    #         print('\n\n\n-----parent_record.id------->',parent_record.id)
    #         res.update({
    #             'name': parent_record.name,
    #             'product_id': parent_record.id
    #         })
    #     return res

    name = fields.Char(string="Name", readonly=True)
    # product_id = fields.Many2one(
    #     'product.template',
    #     string='product',
    #     )
    replaceing_product_id = fields.Many2one(
        "product.product",
        string="Replaceing Product",
    )
    alternative_products_ids = fields.Many2many("product.product", readonly=True)

    def replace_product(self):
        active_model = self.env.context["active_model"]
        active_id = self.env.context["active_id"]

        record = self.env[active_model].browse(active_id)
        print(
            "\n\n\n-----record.product_template_id------->", record.product_template_id
        )
        if self.replaceing_product_id:
            record.product_id = self.replaceing_product_id.id
            print("\n\n\n----product_template_id------->", record.product_template_id)
        else:
            raise UserError("please select product to replace")