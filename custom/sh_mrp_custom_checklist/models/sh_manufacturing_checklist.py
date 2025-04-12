from odoo import fields, models, api


class ShManufacturingChecklist(models.Model):

    _name = "sh.manufacturing.checklist"
    _description = "Manufacturing Checklist"

    name = fields.Char(string="Name",required=True)
    manufacture_order_id = fields.Many2one(
        'mrp.production',
        string='Manufacture Order',
        )
    sequence = fields.Integer(default=10)
    description = fields.Char(string="Description" )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company.id
    )
