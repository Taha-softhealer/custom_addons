from odoo import fields, models, api


class Animal(models.Model):

    _name = "animal"

    height = fields.Float(string="height")


class Dog(models.Model):

    _name = "animal.dog"

    _inherit = "animal"

    sound = fields.Char(string="Sound")

    food = fields.Char(string="Food")


class Cat(models.Model):

    _name = "animal.cat"

    _inherit = "animal"

    sound = fields.Char(string="Sound")

    sleeping_time = fields.Char(string="Sleeping Time")


class Animal_more(models.Model):

    _inherit = "animal"

    Weight = fields.Float(string="Weight")

class Animal(models.Model):

    _name = "animal"

    _inherit = "animal"

    color = fields.Float(string="Color")
