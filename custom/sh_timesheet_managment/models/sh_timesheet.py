from odoo import fields, models, api


class sh_timesheet(models.Model):
    _name = "sh.timesheet"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Timesheets"

    def _get_id(self):
        return self.env.uid

    name = fields.Char(string="Timesheet", required=True, tracking=True)
    user_id = fields.Many2one("res.users", string="User Id", default=_get_id, tracking=True)
    description = fields.Html("description")
    date = fields.Date(string="Date", default=fields.Datetime.now)
    hours = fields.Float(string="hours")
    tag_ids = fields.Many2many("sh.tag", string="Tags")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("submitted", "Submitted"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        string="Status",
        default="draft",
        readonly=True,
    )
    rejection_reason = fields.Text("Rejection reason")
    task_ids = fields.One2many("sh.task", "timesheet_id", "task ids")
    total_amount = fields.Float("total amount")

    def submit(self):
        # print('\n\n\n-----self------->',self)
        self.state = "submitted"

    def approve(self):
        self.state = "approved"

    def reject(self):
        self.state = "rejected"

    def task_count(self):
        self.ensure_one()
        disc = {
            "name": "Customer Invoices",
            "type": "ir.actions.act_window",
            "res_model": "sh.task",
            "domain": [("id", "in", self.task_ids.ids)],
            "view_mode": "list",
        }
        return disc
