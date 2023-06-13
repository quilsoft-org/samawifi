# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import date


class ProductTemplate(models.Model):
    _inherit = "product.template"


    cost_usd = fields.Float("Cost (USD)", compute='_compute_cost_usd', digits=(12, 2), readonly=True)


    @api.depends('standard_price')
    def _compute_cost_usd(self):
        currency_usd = self.env.ref('base.USD')
        if not currency_usd:
            self.cost_usd = self.standard_price
            return

        for product in self:
           product.cost_usd =  product.standard_price 
           if product.currency_id != currency_usd:
              product.cost_usd = product.standard_price * (currency_usd.with_context(date=date.today()).rate  or 1.0)


    #compute_sudo=True, store=True,
