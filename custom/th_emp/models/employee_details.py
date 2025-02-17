from odoo import fields, models, api
from datetime import datetime, date


class Employee(models.Model):
    _name = "sh.employee"
    _description = "employee detailes"

    Emp_img = fields.Binary()
    name = fields.Char(string="Employee Name", required=True)
    Birthdate = fields.Date(string="Birthdate")
    Gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("other", "Other")]
    )
    # Blood_Group = fields.Selection(
    #     [
    #         ("a+", "A+"),
    #         ("a-", "A-"),
    #         ("b+", "B+"),
    #         ("b-", "B-"),
    #         ("o+", "O+"),
    #         ("o+", "O-"),
    #     ]
    # )
    Age = fields.Integer(string="Age", compute="_compute_Age")
    Place_Of_Birth = fields.Char(string="Place of Birth")
    Height = fields.Integer(string="Height")
    Weight = fields.Integer(string="Weight")
    distance_home_work_meter = fields.Float(string="distance in meter")
    km_home_work = fields.Float(
        string="distance in kilometer", compute="_compute_kilometer"
    )
    Marital_Status = fields.Selection(
        [
            ("married", "Married"),
            ("single", "Single"),
        ]
    )
    # Marital_Status=fields.Boolean(default=False,string="Married")
    Physical_disability = fields.Boolean(default=False, string="Physical Disability")
    Private_Address = fields.Text(string="Private Address")
    Private_Email = fields.Char(string="Private Email")
    Private_Phone = fields.Char(string="Private Phone")
    Work_Address = fields.Text(string="Work Address")
    Work_Email = fields.Char(string="Work Email")
    Work_Phone = fields.Char(string="Work Phone")
    Aadhar_no = fields.Char(string="Aadhar Number", required=True)
    Pan_no = fields.Char(string="Pan Number")
    Driving_lisance = fields.Char(string="Driving Lisance")
    Bank_Name = fields.Char(string="Bank Name")
    Account_Name = fields.Char(string="Account Name")
    Account_Number = fields.Char(string="Account Number")
    IFSC_Code = fields.Char(string="IFSC Code")
    job_ids = fields.Many2one(comodel_name="sh.job", string="Job")
    department_id = fields.Many2one(related="job_ids.department_id")
    User_id = fields.Many2one("res.users", string="User id")
    blood_group_model = fields.Many2one("sh.blood.group", string="Blood group")
    category_id = fields.Many2one("sh.employee.category", string="category")
    ref = fields.Char(string="ref", readonly=True)
    # job_many_ids = fields.Many2many(comodel_name='sh.job', string='123456')

    tz = fields.Char(string="Time Zone")

    # @api.onchange('blood_group_model')
    # def _change_blood_group(self):
    #     print("\n\n\n\n\n\n\n",self.job_ids,"\n\n\n\n\n\n")
    #     for i in self.job_ids:
    #         print("\n\n\n\n\n\n\n",i.name,"\n\n\n\n\n\n")

    @api.model_create_multi
    def create(self, vals_list):
        ref = ""
        for vals in vals_list:
            vals["name"] = vals["name"].upper()
            if vals["Private_Phone"]:
                print("\n\n\n-222---------222->")
                if (vals["Private_Phone"][:3]) != "+91":
                    vals["Private_Phone"] = "+91 " + vals["Private_Phone"]
            print("\n\n\n-----vals------->", vals)
            # vals.ref=vals.category_id.ref

        rec = super(Employee, self).create(vals_list)

        rec.ref = rec.category_id.ref
        print("\n\n\n-----rec------->", rec.category_id.ref)

        return rec

    def write(self, vals):
        if "Private_Phone" in vals:
            if vals["Private_Phone"]:
                if (vals["Private_Phone"][:3]) != "+91":
                    vals["Private_Phone"] = "+91 " + vals["Private_Phone"]
        if "category_id" in vals:
            result = self.env["sh.employee.category"].browse(vals["category_id"])

            print("\n\n\n-----vals------->", vals)
            vals["ref"] = result.ref
        print("\n\n\n----------->")
        rec = super().write(vals)
        return rec

    @api.onchange("blood_group_model")
    def _blood_group_change(self):
        self.job_ids.blood_group += self.blood_group_model.name

    @api.onchange("User_id")
    def _onchange_User_id(self):
        self.name = self.User_id.name
        self.tz = self.User_id.tz

    @api.depends("Birthdate")
    def _compute_Age(self):
        # print(self)
        for rec in self:
            print(rec.Birthdate)
            if rec.Birthdate:
                dob_year = (rec.Birthdate).year
                current_year = datetime.now().year
                rec.Age = current_year - dob_year
                print(rec.Age)
                print(">>>>>>>>>>if>>>>>>>>>>>>>>")
            else:
                rec.Age = 0
                print(">>>>>>>>>>else>>>>>>>>>>>>>>")

    @api.depends("distance_home_work_meter")
    def _compute_kilometer(self):
        for rec in self:
            if rec.distance_home_work_meter:
                km = rec.distance_home_work_meter / 1000
                print(km)
                rec.km_home_work = km
            else:
                rec.km_home_work = 0
