# This class defines a model for job positions with various fields such as name, active status,
# address, department, employees, and user relationships.
from odoo import fields, models, api


class Jobs(models.Model):
    _name = "sh.job"
    _description = "department table"

    name = fields.Char(string="Job name", required=True)
    Active = fields.Boolean(string="Looking for job?")
    Address_id = fields.Many2one("res.partner", string="Address")
    count = fields.Integer(string="Number of employee", compute="_count_total")
    department_id = fields.Many2one("sh.department", string="Department")
    # Employee_ids = fields.One2many('sh.employee', 'name', string='Employee Ids')
    Employee_ids = fields.One2many("sh.employee", "job_ids", string="Employees")
    favorite_user_ids = fields.Many2many(
        "res.users", "favorite_user_res_user_rel", string="Favorite user"
    )
    interviewer_ids = fields.Many2many(
        "res.users", "interviewer_res_user_rel", string="Interviewer"
    )
    extended_interviewer_ids = fields.Many2many(
        "res.users",
        "extended_interviewer_res_user_rel",
        string="Extended interviewer user",
    )
    # Employee_many_ids = fields.Many2many("sh.employee", string="Field Name")
    blood_group = fields.Char(string="blood groups")


    @api.depends("Employee_ids")
    def _count_total(self):
        for rec in self:
            count = 0
            for i in rec.Employee_ids:
                count += 1
        rec.count = count
        
    

    # @api.depends("Employee_ids")
    # def _blood_group(self):
    #     for rec in self:
    #         string=""
    #         for i in rec.Employee_ids:
    #             print("\n\n\n\n\n",i.blood_group_model.name,"\n\n\n\n\n")
    #             string+=i.blood_group_model.name
    #     rec.blood_group=string
    # for k in i.blood_group_model:
    # rec.blood_group = k
