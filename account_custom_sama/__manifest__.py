# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Account Custom SAMA',
    'version': "17.0.1.0.0",
    'description': """
Functional
----------
This module add brand and sub-category on invoice report
""",
    'author': 'Antonio Silva',
    'license': 'LGPL-3',
    'category': 'Accounting',
    'depends': [
        'account',
        'itatix_brand_product',
        'itatix_sales_person_target',
    ],
    'data': [
        'security/ir.model.access.csv',
        'report/invoice_report_view.xml',
        'report/invoice_report_sama_view.xml',
        'views/account_move.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
