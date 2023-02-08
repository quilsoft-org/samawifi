# -*- coding: utf-8 -*-
{
    'name': "Sale Purchase Order Extra Reference",
    'summary': """Sale Purchase Order Extra Reference""",
    'description': """Sale Purchase Order Extra Reference""",
    'author': "Quilsoft",
    'website': "https://www.quilsoft.com",
    'category': 'Sale',
    'version': '0.01.1',
    'license': "AGPL-3",    
    'depends': ['sale', 'sale_management', 'account'],
    'data': [
        'security/groups.xml',
        'views/sale_view.xml',
        'views/account_move_view.xml',
        'report/sale_order_report_tmpl.xml',
    ],
}
