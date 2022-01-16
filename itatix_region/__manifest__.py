{
    'name': 'ITATIX Region',
    'category': 'Sale',
    'description': "Custom Fields for PeruggySama",
    'summary': 'Real Cost and Reports',
    'author': "ITATIX SA DE CV",
    "version": '14.0.0.3',
    'depends': ['sale','sale_management','sale_enterprise','crm','account','sale_crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_view.xml',
        'views/sale_order_view.xml',
        'views/account_move_view.xml',
    ],
    'installable': True,
}
