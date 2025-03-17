from odoo import _,fields, models, api


class sh_support_ticket(models.Model):
    _name = "sh.support.ticket"
    _description = "sh support ticket"

    name = fields.Char("name",default="New",readonly=True)

    def default_get(self, fields):
        res = super(sh_support_ticket, self).default_get(fields)
        res["priority"] = "low"

        # You can also set defaults dynamically
        # res["date_field"] = fields.Date.today  # default to today's date

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
    assigned_developer = fields.Many2one(
        "res.users",
        string="assign developer",
    )
    state = fields.Selection(
        [("open", "Open"), ("in progress", "In progress"), ("resolved", "Resolved")]
    )

    leadership_rating = fields.Selection(
        [
            ("", ""),
            ("good", "Good"),
            ("average", "Average"),
            ("excellent", "Excellent"),
        ]
    )

    customers = fields.Many2one(
        "res.partner",
        string="customer",
        required=True
    )

    # invoices_ids = fields.One2many('', '')


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _("New")) == _("New"):
                seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(vals['date_order'])
                ) if 'date_order' in vals else None
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sh.support.ticket', sequence_date=seq_date) or _("New")

        return super().create(vals_list)