from odoo import _, fields, models, api, Command
import logging
from odoo.exceptions import ValidationError


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
        required=True,
    )
    state = fields.Selection(
        [
            ("open", "Open"),
            ("in progress", "In progress"),
            ("resolved", "Resolved"),
            ("close", "Close"),
            ("cancle", "Cancle"),
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

    invoices_id = fields.Many2one("account.move")

    # -------------------------------- methods ---------------------------------

    # @api.constrains("state")
    # def check_state_updation(self):
    #     print('\n\n\n-----self.state------->',self.state)

    @api.constrains("assigned_developer")
    def check_availability(self):
        print(
            "\n\n\n-----self.assigned_developer------->",
            len(self.assigned_developer.ticket_ids),
        )
        record = self.assigned_developer.ticket_ids.search(
            [
                ("state", "not in", ("close", "cancle")),
                ("assigned_developer", "=", self.assigned_developer.name),
            ]
        )
        if len(self.assigned_developer.ticket_ids) > 1:
            if record:
                raise ValidationError("Developer has already assigned ticket")

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
        if self.state in ("close", "cancle"):
            raise ValidationError(
                "You can not change state of ticket once it's close or cancle"
            )
            
        if values.get("state"):
            print("\n\n\n-write is called---------write is called->")
            self.last_state_update = fields.Datetime.now()
            _logger.info(
                "%s ticket state has change to %s", self.name, values.get("state")
            )

        if values.get("state") == "close":
            invoice = self.env["account.move"].create(
                {
                    "partner_id": self.customers.id,
                    "invoice_date": fields.Date.today(),
                    "ticket_id": self.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": f"SH Ticket {self.name}",
                                "quantity": 1.0,
                                "price_unit": 500.0,
                            }
                        ),
                    ],
                }
            )

            self.invoices_id = invoice.id
            print("\n\n\n-----record------->", self.invoices_id)
        res = super().write(values)

        return res

    def invoice(self):
        self.ensure_one()
        disc = {
            "name": "Customer tickets",
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "res_id": self.invoices_id.id,
            "view_mode": "form",
        }
        return disc

    def resolved(self):
        self.state = "resolved"

    def in_progress(self):
        self.state = "in progress"

    def cancle(self):
        self.state = "cancle"

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

    def open_batch_update(self):
        disc = {
            "name": "Customer tickets",
            "type": "ir.actions.act_window",
            "res_model": "sh.batch.update",
            "view_mode": "form",
            "target": "new",
        }
        return disc


class sh_res_partner(models.Model):
    _inherit = "res.partner"

    ticket_ids = fields.One2many("sh.support.ticket", "customers", string="tickets")

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


class sh_res_user(models.Model):
    _inherit = "res.users"

    ticket_ids = fields.One2many(
        "sh.support.ticket", "assigned_developer", string="tickets"
    )


class sh_account_move(models.Model):
    _inherit = "account.move"

    ticket_id = fields.Many2one("sh.support.ticket", string="tickets")
