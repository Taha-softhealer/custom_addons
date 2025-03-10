from odoo import fields, models, api

class sh_student(models.Model):
    _name = "sh.student"
    _description = "student details"

    name = fields.Char()
    partner_id = fields.Many2one("res.partner")
    image = fields.Binary()
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
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="Email")
    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street2")
    city = fields.Char(string="City")
    zip = fields.Char(string="Zip")
    state_id = fields.Char(string="State")
    country_id = fields.Char(string="Country")
    classes_count = fields.Integer()
    invoice_count = fields.Integer()

    @api.onchange("partner_id")
    def onchange_name(self):
        if self.partner_id:
            self.name=self.partner_id.name
            # string = base64.b64encode(self.partner_id.image_1920)
            # print('\n\n\n-----string------->',string)
            self.image = self.partner_id.image_1920
            # print("\n\n\n-----self.image_1920------->", self.image_1920)
            self.phone = self.partner_id.phone
            self.mobile = self.partner_id.mobile
            self.email = self.partner_id.email
            self.street = self.partner_id.street
            self.street2 = self.partner_id.street2
            self.city = self.partner_id.city
            self.zip = self.partner_id.zip
            self.state_id = self.partner_id.state_id.name if self.partner_id.state_id else ""
            self.country_id = self.partner_id.country_id.name if self.partner_id.country_id else ""

    @api.model_create_multi
    def create(self, values):
        for rec in values:
            print("\n\n\n-----rec------->", rec)

        result = super().create(values)

        return result
