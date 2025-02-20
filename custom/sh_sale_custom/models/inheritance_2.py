from odoo import fields, models, api


class A(models.Model):

    _name = "a.a"

    A1 = fields.Char(string="Name")


class B(models.Model):

    _name = "b.b"

    B1 = fields.Char(string="Name")


class C(models.Model):

    _name = "c.c"

    _inherit = ["a.a", "b.b"]

    C1 = fields.Char(string="Name")


class D(models.Model):

    _name = "d.d"

    _inherit = ["c.c"]

    D1 = fields.Char(string="Name")
