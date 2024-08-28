

from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    purchase_order_reference = fields.Char('Purchase Order')
