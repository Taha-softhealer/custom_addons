from odoo import fields, models


class Department(models.Model):
    _name = "sh.department"
    _description = "department table"
    _rec_name = "Name"

    Name = fields.Char(string="Name", required=True)
    Active = fields.Boolean(string="Active")
    parent_id = fields.Many2one("sh.department", string="parent id")
    Manager_id = fields.Many2one("sh.employee", string="Manager id")
    User_id = fields.Many2one("res.users", string="User id")
    Country_id = fields.Many2one("res.country", string="Country id")
    Country_birth = fields.Many2one("res.country", string="Country of birth")
    own_ids = fields.Many2one("sh.department")
    department_ids = fields.One2many(
        comodel_name="sh.department", inverse_name="own_ids", string="department"
    )
    member_ids = fields.One2many(
        comodel_name="sh.employee", inverse_name="department_id", string="Employee ids"
    )
    job_ids = fields.One2many(
        comodel_name="sh.job", inverse_name="department_id", string="Job ids"
    )
