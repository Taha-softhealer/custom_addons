from odoo import fields, models, api


class res_config_setting_inherit(models.TransientModel):
    _inherit = "res.config.settings"

    last_no_order = fields.Integer(
        string="Last No. of Orders", related="company_id.last_no_order", readonly=False
    )
    last_no_days = fields.Integer(
        string="Last No. of Day's Orders",
        related="company_id.last_no_days",
        readonly=False,
    )
    sale_order_states_ids = fields.Many2many(
        "ir.model.fields.selection",
        related="company_id.sale_order_states_ids",
        domain="[('field_id.name', '=', 'state'),('field_id.model', '=', 'sale.order')]",
        readonly=False,
    )
    enable_reorder = fields.Boolean(
        string="Enable Reorder", related="company_id.enable_reorder", readonly=False
    )


class res_config_setting_inherit(models.Model):
    _inherit = "res.company"

    last_no_order = fields.Integer(string="Last No. of Orders")
    last_no_days = fields.Integer(string="Last No. of Day's Orders")
    sale_order_states_ids = fields.Many2many("ir.model.fields.selection")
    enable_reorder = fields.Boolean(string="Enable Reorder")