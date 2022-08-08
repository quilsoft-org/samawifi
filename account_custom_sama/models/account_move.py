# -*- coding: utf-8 -*-

from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = "account.move"

    currency_rate_usd = fields.Float("Currency Rate(USD)", compute='_compute_currency_rate_usd', compute_sudo=True,
                                     store=True, digits=(12, 6), readonly=True)
    product_id = fields.Many2one('product.product', compute='_compute_product_id', store=True, copy=False)
    sama_brand_id = fields.Many2one('sama.brand', related='product_id.sama_brand_id', store=True, copy=False)

    # ivanporras
    total_real_cost = fields.Monetary(string="Costo Real", compute='_compute_real_margin', store=True)
    real_margin = fields.Monetary(string="Margen Real", compute='_compute_real_margin', store=True)
    real_margin_percent = fields.Float(string="Margen Real (%)", compute='_compute_real_margin', store=True)

    @api.depends('invoice_line_ids.real_margin', 'invoice_line_ids.real_cost_subtotal', 'amount_untaxed')
    def _compute_real_margin(self):
        if not all(self._ids):
            for invoice in self:
                invoice.total_real_cost = sum(invoice.invoice_line_ids.mapped('real_cost_subtotal'))
                invoice.real_margin = sum(invoice.invoice_line_ids.mapped('real_margin'))
                invoice.real_margin_percent = invoice.amount_untaxed and invoice.real_margin / invoice.amount_untaxed
        else:
            self.env["account.move.line"].flush(['real_margin'])
            # On batch records recomputation (e.g. at install), compute the margins
            # with a single read_group query for better performance.
            # This isn't done in an onchange environment because (part of) the data
            # may not be stored in database (new records or unsaved modifications).
            grouped_invoice_lines_data = self.env['account.move.line'].read_group(
                [
                    ('move_id', 'in', self.ids), ('product_id', '!=', False),
                ], ['real_margin', 'move_id'], ['move_id'])
            mapped_data = {m['move_id'][0]: m['real_margin'] for m in grouped_invoice_lines_data}
            for invoice in self:
                invoice.total_real_cost = sum(invoice.invoice_line_ids.mapped('real_cost_subtotal'))
                invoice.real_margin = mapped_data.get(invoice.id, 0.0)
                invoice.real_margin_percent = invoice.amount_untaxed and invoice.real_margin / invoice.amount_untaxed

    # end ivanporras

    @api.depends('currency_id', 'date', 'company_id')
    def _compute_currency_rate_usd(self):
        currency_usd = self.env.ref('base.USD')
        if not currency_usd:
            self.currency_rate_usd = 0.0
            return

        for move in self:
            move.currency_rate_usd = 1.0 if move.currency_id == currency_usd else currency_usd.with_context(
                date=move.date).rate or 1.0

    @api.depends('invoice_line_ids', 'invoice_line_ids.product_id')
    def _compute_product_id(self):
        for move in self:
            move.product_id = False
            for line in move.invoice_line_ids.filtered(lambda l: l.product_id):
                move.product_id = line.product_id


class SalesTargetLines(models.Model):
    _inherit = "sales.target.lines"

    team_id = fields.Many2one(related='target_id.sales_team_id')


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    real_cost = fields.Float(string="Costo Real")
    real_cost_subtotal = fields.Float(string="Costo Real Subtotal", compute='_compute_real_margin', store=True)
    real_margin = fields.Monetary(string="Margen Real", compute='_compute_real_margin', store=True)
    real_margin_percent = fields.Float(string="Margen Real (%)", compute='_compute_real_margin', store=True)

    @api.depends('real_cost', 'quantity', 'price_subtotal')
    def _compute_real_margin(self):
        for line in self:
            line.real_cost_subtotal = line.real_cost * line.quantity
            line.real_margin = line.price_subtotal - line.real_cost_subtotal
            line.real_margin_percent = line.price_subtotal and (line.real_margin / line.price_subtotal) * 100