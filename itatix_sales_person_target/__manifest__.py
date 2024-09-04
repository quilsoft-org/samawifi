{
    'name': 'ITATIX SALES PERSON TARGET',
    'category': 'Sale',
    'description': "Custom Salesperson Target for PeruggySama",
    'summary': 'Sales Person Target for sales',
    'author': "ITATIX SA DE CV",
    'license': 'AGPL-3',
    "version": "17.0.1.0.0",
    'depends': ['sale', 'sales_team', 'sale_management', 'stock', 'itatix_region', 'itatix_brand_product'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'report/sales_target_report.xml',
        'report/sale_report_views.xml'
    ],
    'installable': True,
}
