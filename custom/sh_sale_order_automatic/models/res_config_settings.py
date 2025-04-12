from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sh_enable = fields.Boolean(string="Enable")
    sh_default_workflow = fields.Many2one(comodel_name='sh.auto.sale.workflow',string="Default Workflow")
    

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    sh_enable = fields.Boolean(related="company_id.sh_enable",string="Enable",readonly=False)
    sh_default_workflow = fields.Many2one(related="company_id.sh_default_workflow",string="Default Workflow",readonly=False)


