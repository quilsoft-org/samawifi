# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Account Custom SAMA',
    'version': "0.1",
    'description': """
Functional
----------

This module add brand and sub-category on invoice report
""",
    'author': 'Antonio Silva',
    'category': 'Accounting',
    'depends': [
        'account',
        'itatix_brand_product',
    ],
    'data': [
        'report/invoice_report_view.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
