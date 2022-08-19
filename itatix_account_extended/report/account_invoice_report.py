# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    real_margin = fields.Float(string="Margen Real", readonly=True)
    real_margin_percent = fields.Float(string="Margen Real (%)", readonly=True)
    real_cost = fields.Float(string="Costo Real", readonly=True)

    _depends = {
        'account.move.line': [
            'real_cost', 'real_margin', 'real_margin_percent', 'real_cost',
        ],
    }

    def _select(self):
        return super()._select() + ", (line.real_margin / CASE COALESCE(currency_table.rate , 0) WHEN 0 THEN 1.0 ELSE currency_table.rate END) AS real_margin, (line.real_margin_percent) AS real_margin_percent,((line.real_cost * line.quantity) / CASE COALESCE(currency_table.rate, 0) WHEN 0 THEN 1.0 ELSE currency_table.rate END) AS real_cost"

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        res = super(AccountInvoiceReport, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
                                                           orderby=orderby,
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
