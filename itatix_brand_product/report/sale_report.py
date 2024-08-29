# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"
    
    sama_category_id = fields.Many2one('sama.category', readonly=True)
    sama_subcategory_id = fields.Many2one('sama.subcategory', readonly=True)
    sama_brand_id = fields.Many2one('sama.brand', readonly=True, string="Brand")

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res.update({
            'sama_category_id': 't.sama_subcategory_id',
            'sama_subcategory_id': 't.sama_subcategory_id',
            'sama_brand_id': 't.sama_brand_id'
        })
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += """,
            t.sama_category_id,
            t.sama_subcategory_id,
            t.sama_brand_id
        """
        return res
