# -*- coding: utf-8 -*-
# Softhealer Technologies

from odoo import api, fields, models, _ 

class Company(models.Model):
    _inherit='res.company'
    
    sh_lesson_duration = fields.Selection(([
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5')]),string='Lesson Duration')
    