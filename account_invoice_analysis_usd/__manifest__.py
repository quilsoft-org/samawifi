{
    'name': 'Account Invoice Analysis Report',
    'version': "17.0.1.0.0",
    'category': 'Accounting',
    'author': "QuilSoft",
    'license': 'LGPL-3',
    'maintainer': 'Luis Aquino - luis.aquino@quilsoft.com',
    'website': 'https://www.quilsoft.com',
    'summary': """Account Invoice Analysis Report""",
    'depends': [
        'account', 
        'account_custom_sama', 
        'itatix_account_extended'
    ],
    'data': [
        'security/ir.model.access.csv',
        'reports/account_invoice_analysis_report_view.xml',
        'views/menuitems.xml',
    ],
    'installable': True,
    'application': False,
    'sequence': 1,
    'auto_install': False,
}
