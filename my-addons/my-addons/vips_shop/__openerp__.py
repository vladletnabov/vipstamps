# -*- coding: utf-8 -*-
{
    'name': "VIPS shop",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Asgat Consalting",
    'website': "http://www.asgat.ru",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Website',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','sale', 'product', 'vips_vc'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/viewmenu.xml',
        'views/partner.xml',
        'views/delivery.xml',
        'views/sale_order.xml',
        'views/vips_vc.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}