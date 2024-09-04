{
    "name": "Purchase order lines with discounts",
    "author": "ITATIX SA DE CV, Quilsoft"
    "Odoo Community Association (OCA)",
    'license': 'AGPL-3',
    "version": "17.0.1.0.0",
    "category": "Purchase Management",
    "depends": ["purchase_stock", "sale", "crm", "sale_crm", "sale_purchase", "sale_purchase_stock", "web", "account"],
    "data": [
        "views/purchase_discount_view.xml",
        "views/report_purchaseorder.xml",
        "views/product_supplierinfo_view.xml",
        "views/res_partner_view.xml",
        "views/sale_order_view.xml",
        "views/crm_lead_views.xml",
        "views/account_move_view.xml",
        "views/sale_order_portal_content.xml",
        "report/purchase_reports_document.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
