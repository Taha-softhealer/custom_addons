from odoo import fields, models, api
import base64


class sh_student(models.Model):
    _name = "sh.student"
    _inherit = 'avatar.mixin'
    _description = "student details"

    name = fields.Many2one(
        "res.partner",
    )
    image_1920 = fields.Binary(related="name.image_1920",force_save=1)
    # image_128 = fields.Image(
    #     "Image 128", related="img", max_width=128, max_height=128, store=True
    # )
    # img_1920 = fields.Image(
    #     "Image 1920", related="img", max_width=1920, max_height=1920, store=True
    # )
    gender = fields.Selection(
        string="Gender",
        selection=[("male", "Male"), ("female", "Female"), ("other", "Other")],
    )
    language = fields.Char(string="Language")
    birthdate = fields.Date(string="Birthdate")
    visa_info = fields.Text(string="visa info")
    blood_group = fields.Selection(
        [("a+", "A+"), ("b+", "B+"), ("ab+", "AB+"), ("ab-", "AB-")]
    )
    # address
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="Email")
    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street2")
    city = fields.Char(string="City")
    zip = fields.Char(string="Zip")
    state_id = fields.Char(string="State")
    country_id = fields.Char(string="Country")

    @api.onchange("name")
    def onchange_name(self):
        if self.name:
            print("\n\n\n-----self.name------->", self.name)

            self.phone = self.name.phone
            self.mobile = self.name.mobile
            self.email = self.name.email
            # lala=base64.b64decode(self.name.image_1920)
            # print('\n\n\n-----lala------->',lala)
            # self.img = lala
            # print("\n\n\n-----self.name.image_1920------->", self.name.image_1920)
            self.street = self.name.street
            self.street2 = self.name.street2
            self.city = self.name.city
            self.zip = self.name.zip
            self.state_id = self.name.state_id.name
            self.country_id = self.name.country_id.name


    @api.model_create_multi
    def create(self, values):
        for rec in values:
            print('\n\n\n-----rec------->',rec)
        
        result = super().create(values)
        
        return result