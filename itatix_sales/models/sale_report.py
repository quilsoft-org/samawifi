# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'

    real_margin = fields.Float(string="Margen Real", readonly=True)
    real_margin_percent = fields.Float(string="Margen Real (%)", readonly=True, group_operator="avg")

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields[
            'real_margin'] = ", SUM(l.real_margin / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) AS real_margin"
        fields[
            'real_margin_percent'] = ", l.real_margin_percent AS real_margin_percent"

        groupby_ = """
                ,l.real_margin_percent %s
            """ % (groupby)

        return super(SaleReport, self)._query(with_clause, fields, groupby_, from_clause)


class SaleReportSama(models.Model):
    _inherit = 'sale.report.sama'

    real_margin = fields.Float(string="Margen Real", readonly=True)
    real_margin_percent = fields.Float(string="Margen Real (%)", readonly=True, group_operator="avg")

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['real_margin'] = ", sum(l.real_margin) as real_margin"
        fields['real_margin_percent'] = ",l.real_margin_percent as real_margin_percent"
        groupby_ = """
                ,l.real_margin_percent %s
            """ % (groupby)
        return super(SaleReportSama, self)._query(with_clause, fields, groupby_, from_clause)


