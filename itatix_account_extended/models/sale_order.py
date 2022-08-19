from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line()
        res['real_cost'] = self.real_cost
        return res