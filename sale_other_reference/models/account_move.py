# -*- coding: utf-8 -*-


from odoo import models, fields

import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    purchase_order_reference = fields.Char('Purchase Order')

AccountMove()