# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models, api


class ResPartner(models.Model):

    _inherit = "res.partner"

    is_student = fields.Boolean(string='is_student')
