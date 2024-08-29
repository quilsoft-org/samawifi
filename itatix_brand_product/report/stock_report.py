from odoo import fields, models


class StockReport(models.Model):
    _inherit = 'stock.report'

    sama_category_id = fields.Many2one('sama.category', readonly=True, string='Category')
    sama_subcategory_id = fields.Many2one('sama.subcategory', readonly=True, string='Subcategory')
    sama_brand_id = fields.Many2one('sama.brand', readonly=True, string="Brand")

    def _select(self):
        res = super()._select()
        res += """,
            t.sama_category_id AS sama_category_id,
            t.sama_subcategory_id AS sama_subcategory_id,
            t.sama_brand_id AS sama_brand_id
        """
        return res

    def _group_by(self):
        res = super()._group_by()
        res += """,
            t.sama_category_id,
            t.sama_subcategory_id,
            t.sama_brand_id
        """
        return res
