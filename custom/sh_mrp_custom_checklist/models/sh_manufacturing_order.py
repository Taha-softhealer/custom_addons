from odoo import  api, fields, models, Command

class ShManufacturingOrder(models.Model):
    _inherit = 'mrp.production'

    checklist_template_ids = fields.Many2many('sh.manufacturing.checklist.template')
    checklist_ids = fields.One2many('sh.manufacturing.checklist.line', 'sh_manufacture_id')
    progress = fields.Integer(string='Progress Level',compute="_compute_progress",store=True)
    
    @api.depends("checklist_ids.state")
    def _compute_progress(self):
        for record in self:
            if record.checklist_ids:
                rec=record.checklist_ids.search([("state","=","completed"),("sh_manufacture_id","=",self.id)])
                record.progress = (len(rec)/len(record.checklist_ids))*100
            else:
                record.progress=0
    
    
    
    @api.onchange("checklist_template_ids")
    def _onchange_checklist_template(self):
        rec_ls=[]
        for rec in self.checklist_template_ids:
            print('\n\n\n-----rec.checklist_ids.ids------->',rec.checklist_ids.ids)
            for i in rec.checklist_ids.ids:
                rec_set=self.env["sh.manufacturing.checklist.line"].create({"checklist_id":i})
                rec_ls.append(rec_set)
        self.checklist_ids=[(6,0,[i.id for i in rec_ls])]