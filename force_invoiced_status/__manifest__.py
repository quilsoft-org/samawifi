{
    'name': 'Force Invoiced Status',
    'version': "17.0.1.0.0",
    'category': 'sale',
    'summary': """
        This module adds the possibility of 
        marking a sales order as invoiced.
    """,
    'author': "Quilsoft",
    'license': 'AGPL-3',
    'depends': [
        'sale'
    ],
    'data': [
        'views/sale_order_views.xml'
    ],
    'installable': True,
    'application': False,
}