from odoo import fields, models, api


class ShManufacturingChecklistTemplate(models.Model):

    _name = "sh.manufacturing.checklist.template"
    _description = "Manufacturing Checklist"

    name = fields.Char(string="Name",required=True)
    sequence = fields.Integer(default=10)
    checklist_ids = fields.Many2many('sh.manufacturing.checklist',"sh_manufacturing_checklist_rel",string="Check list")
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company.id
    )
