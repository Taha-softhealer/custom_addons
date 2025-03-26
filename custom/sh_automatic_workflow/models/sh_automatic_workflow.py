from odoo import fields, models, api
from odoo.exceptions import ValidationError

class sh_automatic_workflow(models.Model):
    _name="sh.automatic.workflow"
    _description="Automatic workflow management"

    name = fields.Char(string='Name')
    delivery_order = fields.Boolean(string='Delivery Order')
    force_transfer = fields.Boolean(string='Force Transfer')
    create_invoice = fields.Boolean(string='Create Invoice')
    validate_invoice = fields.Boolean(string='Validate Invoice')
    register_payment = fields.Boolean(string='Register Payment')
    send_invo_by_email = fields.Boolean(string='Send Invoice By Email')

    # sale journal
    # payment journal
    # payment method
    # company
    
    @api.constrains("force_transfer")
    def check_force_transfer(self):
        for rec in self:
            print('\n\n\n-----rec.force_transfer------->',rec.force_transfer)
            print('\n\n\n-----rec.delivery_order------->',rec.delivery_order)
            if rec.force_transfer:
                if not rec.delivery_order:
                    raise ValidationError("You can not select force transfer without selecting delivery order")
                
    @api.constrains("create_invoice")
    def check_create_invoice(self):
        for rec in self:
            print('\n\n\n-----rec.force_transfer------->',rec.force_transfer)
            print('\n\n\n-----rec.delivery_order------->',rec.delivery_order)
            if rec.create_invoice:
                if not rec.force_transfer:
                    raise ValidationError("You can not select create invoice without selecting force transfer")
                
    @api.constrains("validate_invoice")
    def check_validate_invoice(self):
        for rec in self:
            print('\n\n\n-----rec.force_transfer------->',rec.force_transfer)
            print('\n\n\n-----rec.delivery_order------->',rec.delivery_order)
            if rec.validate_invoice:
                if not rec.create_invoice:
                    raise ValidationError("You can not select validate invoice without selecting create invoice")

    @api.constrains("register_payment")
    def check_register_payment(self):
        for rec in self:
            print('\n\n\n-----rec.force_transfer------->',rec.force_transfer)
            print('\n\n\n-----rec.delivery_order------->',rec.delivery_order)
            if rec.register_payment:
                if not rec.validate_invoice:
                    raise ValidationError("You can not select register payment without selecting validate invoice")

    @api.constrains("send_invo_by_email")
    def check_send_invo_by_email(self):
        for rec in self:
            print('\n\n\n-----rec.force_transfer------->',rec.force_transfer)
            print('\n\n\n-----rec.delivery_order------->',rec.delivery_order)
            if rec.send_invo_by_email:
                if not rec.register_payment:
                    raise ValidationError("You can not select send invoice by email without selecting register payment")
    
    def write(self, vals):
        print('\n\n\n-----values------->',vals)
        res = super(sh_automatic_workflow,self).write(vals)
        return res