from odoo import fields, models, api
from datetime import datetime
from odoo.exceptions import UserError  # type: ignore


class sh_student(models.Model):
    _name = "sh.student"
    _description = "sudent table"

    name = fields.Char(string="Name", required=True)
    mobile_num = fields.Integer(string="Mobile")
    mobile_bool = fields.Boolean(
        string="Mobile number already excisting", readonly=True
    )
    Birthdate = fields.Date(string="Birthdate")
    category = fields.Char(string="Category", readonly=True)
    email = fields.Char(string="Email")

    # for rec in self:
    #     print(rec.Birthdate)
    #     if rec.Birthdate:
    #         dob_year = (rec.Birthdate).year
    #         current_year = datetime.now().year
    #         rec.Age = current_year - dob_year
    #         print(rec.Age)
    #         print(">>>>>>>>>>if>>>>>>>>>>>>>>")
    #     else:
    #         rec.Age = 0
    #         print(">>>>>>>>>>else>>>>>>>>>>>>>>")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("email"):
                record = self.search([("email", "=", vals.get("email"))])
                if record:
                    raise UserError("User with this email id already exist")

            if vals.get("Birthdate"):
                datetime_object = datetime.strptime(vals["Birthdate"], "%Y-%m-%d")
                dob_year = datetime_object.year
                current_year = datetime.now().year
                # age = current_year - dob_year
                # dob_year = vals.get("Birthdate").year
                # current_year = datetime.now().year
                age = current_year - dob_year
                category_rec = self.env["sh.category"].search(
                    ["&", ("min_age", "<=", age), ("max_age", ">=", age)]
                )
                vals["category"] = category_rec.name

            existing_record = self.search([("mobile_num", "=", vals.get("mobile_num"))])
            if existing_record:
                vals["mobile_bool"] = True
            else:
                vals["mobile_bool"] = False

            return super(sh_student, self).create(vals)

    def write(self, vals):
        if vals.get("email"):
            record = self.search([("email", "=", vals.get("email"))])
            if record:
                raise UserError("User with this email id already exist")

        if vals.get("Birthdate"):
            print('\n\n\n-----vals["Birthdate"]------->', vals["Birthdate"])
            datetime_object = datetime.strptime(vals["Birthdate"], "%Y-%m-%d")
            dob_year = datetime_object.year
            current_year = datetime.now().year
            age = current_year - dob_year
            print("\n\n\n-----age------->", age)
            category_rec = self.env["sh.category"].search(
                ["&", ("min_age", "<=", age), ("max_age", ">=", age)]
            )
            vals["category"] = category_rec.name

        if vals.get("mobile_num"):
            existing_record = self.search([("mobile_num", "=", vals.get("mobile_num"))])
            if existing_record:
                vals["mobile_bool"] = True
            else:
                vals["mobile_bool"] = False

        return super(sh_student, self).write(vals)
