# -*- coding: utf-8 -*-

from odoo import fields, models

class SaleReport(models.Model):
    _inherit = 'sale.report'

    real_margin = fields.Float(string="Margen Real", readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['real_margin'] = ", SUM(l.real_margin / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) AS real_margin"

        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)


class SaleReportSama(models.Model):
    _inherit = 'sale.report.sama'

    real_margin = fields.Float(string="Margen Real", readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['real_margin'] = ", CASE WHEN l.product_id IS NOT NULL THEN sum(CASE WHEN s.currency_id = 2 THEN l.real_margin ELSE s.exchange_currency_rate END) ELSE 0 END as real_margin"
        return super(SaleReportSama, self)._query(with_clause, fields, groupby, from_clause)


