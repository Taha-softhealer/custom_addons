from odoo import fields, models, api


class product_product_inherit(models.Model):
    _inherit="product.product"

    alternative_products_ids = fields.Many2many(
        "product.product","product_product_rel","product_product"
    )

    def write(self, vals):
            print("\n\n\n-----self.------->", self.alternative_products_ids.ids)
            if vals.get("alternative_products_ids"):
                print(
                    '\n\n\n-----vals["alternative_products_ids"]------->',
                    vals["alternative_products_ids"],
                )
                res_ls = []
                res_ls.append(self.id)
                for rec in vals["alternative_products_ids"]:
                    res_ls.append(rec[1])

                print("\n\n\n-----res_ls------->", res_ls)
                # temp_ls=res_ls.copy()

                for rec in vals["alternative_products_ids"]:
                    record = self.env["product.product"].browse(rec[1])
                    record.alternative_products_ids = [
                        (6, False, [p for p in res_ls if p != rec[1]])
                    ]
                    # ------------------------
                    # record.alternative_products_ids=[(6,False,res_ls(rec[1]))]
                    # temp_ls=res_ls.copy()

                # if(len(vals["alternative_products_ids"])==1):
                #     record=self.env["product.template"].browse(vals["alternative_products_ids"][0][1])
                #     record.alternative_products_ids=[(6,False,[self.id])]

                # for product_out in vals['alternative_products_ids']:
                #     for product_in in vals['alternative_products_ids']:
                #         if(product_out==product_in):
                #             print('\n\n\n----inside that in==out------->')
                #         else:
                #             record=self.env["product.template"].browse(product_out[1])
                #             record.alternative_products_ids=[(6,False,[self.id,product_in[1]])]

            rec = super().write(vals)
            return rec


class sh_produt_template_inherit(models.Model):
    _inherit = "product.template"
    _description = "product details"

    alternative_products_ids = fields.Many2many(
        "product.template", "product_template_rel", "product_temp"
    )