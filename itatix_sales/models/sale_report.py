from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)


class SaleReport(models.Model):
    _inherit = 'sale.report'

    real_margin = fields.Float(string="Margen Real", readonly=True)
    real_margin_percent = fields.Float(string="Margen Real (%)", readonly=True)
    real_cost = fields.Float(string="Costo Real", readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields[
            'real_margin'] = ", SUM(l.real_margin / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) AS real_margin"
        fields['real_margin_percent'] = ", SUM(l.real_margin_percent) AS real_margin_percent"
        fields[
            'real_cost'] = ", SUM((l.real_cost * l.product_uom_qty) / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) AS real_cost"

        # groupby += ',l.real_margin_percent'

        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        res = super(SaleReport, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby,
                                                 lazy=lazy)
        _logger.error(res)
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


class SaleReportSama(models.Model):
    _inherit = 'sale.report.sama'

    real_margin = fields.Float(string="Margen Real", readonly=True)
    real_margin_percent = fields.Float(string="Margen Real (%)", readonly=True)
    real_cost = fields.Float(string="Costo Real", readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['real_margin'] = ", sum(l.real_margin) as real_margin"
        fields['real_margin_percent'] = ", SUM(l.real_margin_percent) AS real_margin_percent"
        fields['real_cost'] = ", SUM(l.real_cost * l.product_uom_qty) AS real_cost"
        return super(SaleReportSama, self)._query(with_clause, fields, groupby, from_clause)

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        res = super(SaleReportSama, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
                                                     orderby=orderby, lazy=lazy)
        _logger.error(res)
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