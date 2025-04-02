from odoo import fields, models, api
from odoo.exceptions import ValidationError


class sh_automatic_workflow(models.Model):
    _name = "sh.automatic.workflow"
    _description = "Automatic workflow management"

    name = fields.Char(string="Name")
    delivery_order = fields.Boolean(string="Delivery Order")
    create_invoice = fields.Boolean(string="Create Invoice")
    validate_invoice = fields.Boolean(string="Validate Invoice")
    register_payment = fields.Boolean(string="Register Payment")
    send_invo_by_email = fields.Boolean(string="Send Invoice By Email")

    sale_journal_id = fields.Many2one(
        "account.journal", string="Sale Journal", domain="[('type','=','sale')]"
    )
    payment_journal_id = fields.Many2one(
        "account.journal",
        string="Payment Journal",
        domain="[('type','in',('bank','cash'))]",
    )
    sh_payment_method_id = fields.Many2one(
        "account.payment.method",
        string="Payment Method",
        domain="[('payment_type','=','inbound')]",
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
    )
