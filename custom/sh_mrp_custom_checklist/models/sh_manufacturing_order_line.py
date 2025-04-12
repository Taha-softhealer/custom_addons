from odoo import fields, models, api


class ShManufacturingChecklistLine(models.Model):

    _name = "sh.manufacturing.checklist.line"
    _description = "Manufacturing Checklist"

    name = fields.Char(string="Name")
    checklist_id = fields.Many2one(
        "sh.manufacturing.checklist",
        string="Name",
    )
    sh_manufacture_id = fields.Many2one(
        "mrp.production",
        string="manufacture",
    )
    description = fields.Char(string="Description",related="checklist_id.description", readonly=False)
    date = fields.Datetime(string='Date',related="sh_manufacture_id.date_start", readonly=False)
    state = fields.Selection(
        string="State",
        default="new",
        selection=[("new", "New"), ("completed", "Completed"), ("cancle", "Cancle")],
    )
    
    def do_complete(self):
        self.state="completed"
    
    def do_cancle(self):
        self.state="cancle"