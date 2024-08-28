{
    'name': "Sale Purchase Order Extra Reference",
    'summary': """Sale Purchase Order Extra Reference""",
    'description': """Sale Purchase Order Extra Reference""",
    'author': "Quilsoft",
    'website': "https://www.quilsoft.com",
    'category': 'Sale',
    'version': "16.0.1.0.0",
    'license': "AGPL-3",    
    'depends': ['sale_management', 'account'],
    'data': [
        'security/groups.xml',
        'views/sale_view.xml',
        'views/account_move_view.xml',
        'report/sale_order_report_tmpl.xml',
    ],
}
