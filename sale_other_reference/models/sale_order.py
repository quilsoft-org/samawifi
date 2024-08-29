

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    purchase_order_reference = fields.Char('Purchase Order Reference')

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        if self.purchase_order_reference:
            res.update({
                'purchase_order_reference': self.purchase_order_reference,
            })
        return res
