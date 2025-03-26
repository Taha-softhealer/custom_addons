from odoo import fields, models, api


class product_product_inherit(models.Model):
    _inherit="product.product"

    alternative_products_ids = fields.Many2many(
        "product.product","product_product_rel","product_product"
    )

    def write(self, vals):
        if vals.get("alternative_products_ids"):
            for rec in vals["alternative_products_ids"]:
                if rec[0] == 3:
                    record = self.env["product.product"].browse(rec[1])
                    super().write({'alternative_products_ids':[(3,record.id)]})
                    if self.id in record.alternative_products_ids.ids:
                        record.write({
                            'alternative_products_ids': [(3, self.id)]
                        })
                    
                        

                if rec[0]==4:
                    print(
                        '\n\n\n-----vals["alternative_products_ids"]------->',
                        vals["alternative_products_ids"],
                    )
                    res_ls = []
                    res_ls.append(self.id)
                    for recs in vals["alternative_products_ids"]:
                        if recs[0]==4:
                            res_ls.append(recs[1])
                    
                    if(self.alternative_products_ids):
                        for i in self.alternative_products_ids.ids:
                            res_ls.append(i)

                
                    for rec in vals["alternative_products_ids"]:
                        record = self.env["product.product"].browse(rec[1])
                        record.alternative_products_ids = [
                            (6, False, [p for p in res_ls if p != rec[1]])
                        ]
            
            rec = super().write(vals)
            return rec


class sh_produt_template_inherit(models.Model):
    _inherit = "product.template"
    _description = "product details"

    alternative_products_ids = fields.Many2many(
        "product.template", "product_template_rel", "product_temp"
    )