from odoo import api, fields, models


class BatchUpdating(models.TransientModel):
    _name = "sh.batch.update"

    name = fields.Char("name")

    state = fields.Selection(
        [
            ("open", "Open"),
            ("in progress", "In progress"),
            ("resolved", "Resolved"),
            ("close", "Close"),
        ]
    )


    def save(self):
        
        active_model = self.env.context["active_model"]
        active_id = self.env.context["active_ids"]
        
        for rec in active_id:
            record=self.env[active_model].browse(rec)
            record.state=self.state
        print('\n\n\n-----self------->',active_id)