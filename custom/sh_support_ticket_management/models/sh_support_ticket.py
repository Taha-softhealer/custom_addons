from odoo import _, fields, models, api
import logging


_logger = logging.getLogger(__name__)


class sh_support_ticket(models.Model):
    _name = "sh.support.ticket"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "sh support ticket"

    name = fields.Char("name", default="New", readonly=True)

    def default_get(self, fields):
        res = super(sh_support_ticket, self).default_get(fields)
        res["priority"] = "low"
        res["state"] = "open"

        return res

    priority = fields.Selection(
        [
            ("", ""),
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
            ("very high", "Very high"),
        ]
    )

    last_state_update = fields.Datetime()

    assigned_developer = fields.Many2one(
        "res.users",
        string="assign developer",
    )
    state = fields.Selection(
        [
            ("open", "Open"),
            ("in progress", "In progress"),
            ("resolved", "Resolved"),
            ("close", "Close"),
        ]
    )

    date = fields.Datetime(default=fields.Datetime.now)

    leadership_rating = fields.Selection(
        [
            ("", ""),
            ("good", "Good"),
            ("average", "Average"),
            ("excellent", "Excellent"),
        ]
    )

    customers = fields.Many2one("res.partner", string="customer", required=True)

    # invoices_ids = fields.One2many('', '')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                seq_date = (
                    fields.Datetime.context_timestamp(
                        self, fields.Datetime.to_datetime(vals["date_order"])
                    )
                    if "date_order" in vals
                    else None
                )
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "sh.support.ticket", sequence_date=seq_date
                ) or _("New")

        return super().create(vals_list)

    def write(self, values):
        if values.get("state"):
            print("\n\n\n-write is called---------write is called->")
            self.last_state_update = fields.Datetime.now()
            _logger.info(
                "%s ticket state has change to %s", self.name, values.get("state")
            )
        res = super().write(values)

        return res

    def close(self):
        self.state = "close"

    def close_ticket(self):
        # print("\n\n",self,"\n\n")
        records = self.search([("state", "=", "resolved")])
        for rec in records:
            print(
                "\n\n\n-----((rec.last_state_update - fields.Datetime.now()).days)------->",
                (type((fields.Datetime.now() - rec.last_state_update).days)),
            )
            if ((fields.Datetime.now() - rec.last_state_update).days) == 7:
                print("\n\n\n-in---------in->")
                rec.state = "close"
            print("\n\n\n-out---------out->")

    def resolved(self):
        self.state = "resolved"


class sh_res_partner(models.Model):
    _inherit = "res.partner"

    ticket_ids = fields.One2many(
        "sh.support.ticket", inverse_name="customers", string="tickets"
    )

    def tickets_count(self):
        self.ensure_one()
        disc = {
            "name": "Customer tickets",
            "type": "ir.actions.act_window",
            "res_model": "sh.support.ticket",
            "domain": [("id", "in", self.ticket_ids.ids)],
            "view_mode": "list",
        }
        return disc
