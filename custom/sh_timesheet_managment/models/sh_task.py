from odoo import fields, models, api


class sh_tag(models.Model):
    _name = "sh.task"
    _description = "Tasks"

    name = fields.Char(string="Task")
    amount = fields.Float(string="Amount")
    timesheet_id = fields.Many2one(
        "sh.timesheet",
        string="timesheet",
    )
