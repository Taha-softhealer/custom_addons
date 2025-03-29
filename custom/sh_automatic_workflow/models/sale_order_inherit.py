from odoo import fields, models, api


class sh_sale_order_inherit(models.Model):
    _inherit = "sale.order"
    _description = "sales note details"

    def default_get(self, fields):
        res = super(sh_sale_order_inherit, self).default_get(fields)

        # Get context values
        res_enable = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("sh_automatic_workflow.enable_automatic_workflow")
        )
        res_auto_id = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("sh_automatic_workflow.automatic_workflow_id")
        )

        if res_enable:
            res["enable_automatic_workflow"] = res_enable
        else:
            res["enable_automatic_workflow"] = False

        if res_auto_id:
            res_auto_id = int(res_auto_id)
            res_auto_id_record = self.env["sh.automatic.workflow"].browse(res_auto_id)
            if res_auto_id_record:
                res["automatic_workflow_id"] = res_auto_id_record.id

        print(
            "\n\n\n-----automatic_workflow_id------->", res.get("automatic_workflow_id")
        )
        return res

    enable_automatic_workflow = fields.Boolean(
        string="Enable Auto Workflow",
    )
    automatic_workflow_id = fields.Many2one(
        "sh.automatic.workflow",
        string="Automatic Workflow",
    )

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        if self.partner_id:
            if self.partner_id.automatic_workflow_id:
                self.automatic_workflow_id = self.partner_id.automatic_workflow_id
            else:
                res_auto_id = (
                    self.env["ir.config_parameter"]
                    .sudo()
                    .get_param("sh_automatic_workflow.automatic_workflow_id")
                )
                self.automatic_workflow_id = int(res_auto_id)

    def action_confirm(self):
        super().action_confirm()
        if self.automatic_workflow_id:
            if self.automatic_workflow_id.delivery_order:
                rec = self.env["stock.picking"].search([("sale_id", "=", self.id)])
                print('\n\n\n-----rec------->',rec)
                val=rec.button_validate()
                print('\n\n\n-----val------->',val)

            if self.automatic_workflow_id.create_invoice:
                invoice_created = self._create_invoices()

                if self.automatic_workflow_id.validate_invoice:
                    invoice_created.action_post()

                    if self.automatic_workflow_id.send_invo_by_email:
                        invoice_created.action_invoice_sent()
                        invoice_created.action_send_and_print()

                    if self.automatic_workflow_id.register_payment:
                        return (
                            self.env["account.payment.register"]
                            .with_context(
                                active_model="account.move",
                                active_ids=invoice_created.ids,
                                default_payment_method_line_id=self.automatic_workflow_id.sh_payment_method_id.id,
                                default_journal_id=self.automatic_workflow_id.payment_journal_id.id,
                            )
                            .create({"group_payment": False})
                            .action_create_payments()
                        )
