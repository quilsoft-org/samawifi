# -*- coding: utf-8 -*-

from odoo import models, fields, api



class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    real_margin = fields.Float(string="Margen Real", readonly=True)
    real_margin_percent = fields.Float(string="Margen Real (%)", readonly=True)
    real_cost = fields.Float(string="Costo Real", readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields[
            'real_margin'] = ", SUM(line.real_margin / CASE COALESCE(move.currency_rate, 0) WHEN 0 THEN 1.0 ELSE move.currency_rate END) AS real_margin"
        fields['real_margin_percent'] = ", SUM(line.real_margin_percent) AS real_margin_percent"
        fields[
            'real_cost'] = ", SUM((line.real_cost * line.product_uom_qty) / CASE COALESCE(move.currency_rate, 0) WHEN 0 THEN 1.0 ELSE move.currency_rate END) AS real_cost"



        return super(AccountInvoiceReport, self)._query(with_clause, fields, groupby, from_clause)

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        res = super(AccountInvoiceReport, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby,
                                                 lazy=lazy)
        groupby = [groupby] if isinstance(groupby, str) else groupby

        for record in res:
            if "real_margin" in record:
                if record['real_margin']:
                    record['real_margin_percent'] = record['real_margin'] * 100 / record['price_subtotal']
                else:
                    record['real_margin_percent'] = record['real_margin'] or 1.0 / 1.0
        if not groupby:
            for record in res:
                if "real_margin" in record:
                    if record['real_margin']:
                        record['real_margin_percent'] = record['real_margin'] * 100 / record['price_subtotal']
                    else:
                        record['real_margin_percent'] = record['real_margin'] or 1.0 / 1.0
        return res
