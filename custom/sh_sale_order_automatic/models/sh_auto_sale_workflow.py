from odoo import models, fields, api,Command

class ShAutoSaleWorkflow(models.Model):
    _name = "sh.auto.sale.workflow"
    _description = "sale workflow"
    
    name = fields.Char(string="Name")
    delivery_order = fields.Boolean(string="Delivery Order")
    force_transfer = fields.Boolean(string="Force Transfer")
    create_invoice = fields.Boolean(string="Create Invoice")
    validate_invoice = fields.Boolean(string="Validate Invoice")
    register_payment = fields.Boolean(string="Register Payment")
    send_invoice_by_email = fields.Boolean(string="Send Invoice by Email")
    sale_journal = fields.Many2one(comodel_name='account.journal',string="Sale Journal")
    payment_journal = fields.Many2one(comodel_name='account.journal',string="Payment Journal")
    payment_method = fields.Many2one(comodel_name='account.payment.method',string="Payment Method")
    company_id =fields.Many2one(comodel_name='res.company',string="Company")
    
    @api.onchange('delivery_order')
    def _onchange_delivery_order(self):
        for rec in self:
            if rec.delivery_order == False:
                rec.force_transfer = False

    @api.onchange('create_invoice')
    def _onchange_create_invoice(self):
        for rec in self:
            if rec.create_invoice == False:
                rec.validate_invoice = False
                rec.register_payment = False
                rec.send_invoice_by_email = False
                
                rec.payment_journal=[Command.clear()]
                rec.sale_journal=[Command.clear()]
                rec.payment_method=[Command.clear()]
                
    
    @api.onchange('validate_invoice')
    def _onchange_validate_invoice(self):
        for rec in self:
            if rec.validate_invoice == False:
                rec.register_payment = False
                rec.send_invoice_by_email = False