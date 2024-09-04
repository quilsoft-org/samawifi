# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Itatix Account Extended',
    'version': "17.0.1.0.0",
    'description': """
Functional
----------
This module add brand and sub-category on invoice report
""",
    'author': 'Ivan Porras',
    'license': 'AGPL-3',
    'category': 'Accounting',
    'depends': [
        'account',
        'itatix_sales',
    ],
    'data': [
        'views/account_move.xml',
        'report/account_invoice_report.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
