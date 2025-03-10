from odoo import fields, models, api


class sh_lesson(models.Model):
    _name = "sh.lesson"
    _description = "lesson details details"

    name = fields.Char()
    student_ids = fields.Many2many("sh.student")
    duration = fields.Integer(string="Duration")
    total_space = fields.Integer(string='Total space')
