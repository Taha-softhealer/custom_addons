from odoo import fields, models, api


class sh_tag(models.Model):
    _name = "sh.tag"
    _description = "Tags"

    name = fields.Char(string="Tag", required=True)
    timesheets = fields.Many2many(comodel_name="sh.timesheet", string="timesheets")
    manager_id = fields.Many2one(
        "res.users",
        string="manager",
    )
