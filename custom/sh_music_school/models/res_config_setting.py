from odoo import api, fields, models,modules, _



class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    sh_lesson_duration = fields.Selection(related="company_id.sh_lesson_duration", string='Lesson Duration',readonly=False)