# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit="account.move" 
    
    
    sh_school_classes_id=fields.Many2one("sh.school.classes",string="class")