# -*- coding: utf-8 -*-
{
    'name': "VIP-Stamp Slider",

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
    'version': '0.5',

    # any module necessary for this one to work correctly
    'depends': ['website'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/snippets.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}