from odoo import fields, models, api


class sh_reject_reason(models.TransientModel):
    _name = "sh.reject.reason"
    _description = "Rejection reason"

    def default_get(self, fields):
        print("\n\n\n-----fields------->", fields)
        res = super(sh_reject_reason, self).default_get(fields)
        print("\n\n\n-----res------->", res)
        # Set default values based on conditions or logic
        # if "name" in fields:
        res["name"] = "Default Name"
        # if "user_id" in fields:
        res["user_id"] = self.env.uid
        print('\n\n\n-----res------->',res)


        # You can also set defaults dynamically
        # res["date_field"] = fields.Date.today  # default to today's date

        return res

    name = fields.Char(string="reject reason", required=True)
    user_id = fields.Many2one("res.users", string="User Id")

    def save(self):
        active_model = self.env.context["active_model"]
        active_id = self.env.context["active_id"]

        record = self.env[active_model].browse(active_id)
        record.rejection_reason = self.name
        record.state = "rejected"
        print("\n\n\n-----self.env.context------->", self.env.context)

        # from odoo import models, fields


# class MyModel(models.Model):
#     _name = 'my.model'

#     name = fields.Char('Name')
#     description = fields.Text('Description')
#     active = fields.Boolean('Active', default=True)
#     date_field = fields.Date('Date')
