# Part of softener Technologies
# Part of Softhealer Technologies. See LICENSE file for full copyright and licensing details.
{
    'name':'Sale Order Automatic Workflow',
    'description':'Automatic Workflow',
    'version':'1.0.0',
    'summary':'manage sale order',
    'sequence':1,
    'category':'CRM/Sales',
    'website':'https://softhealer.com',
    'depends':['contacts','calendar','sale_stock','sale_management','account'],
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "views/sh_auto_sale_workflow_views.xml",
        "views/sale_order.xml",
    ],
    
    'installation':True,
    'application':True,
    'license':'OPL-1'
}