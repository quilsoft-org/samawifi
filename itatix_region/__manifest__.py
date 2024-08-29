{
    'name': 'ITATIX Region',
    'category': 'Sale',
    'description': "Custom Fields for PeruggySama",
    'summary': 'Real Cost and Reports',
    'author': "ITATIX SA DE CV",
    'license': 'AGPL-3',
    "version": "16.0.1.0.0",
    'depends': ['sale_management','sale_enterprise','account','sale_crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/partner_region_views.xml',
        'views/crm_lead_view.xml',
        'views/sale_order_view.xml',
        'views/account_move_view.xml',
        'views/res_partner_view.xml',
    ],
    'installable': True,
}
