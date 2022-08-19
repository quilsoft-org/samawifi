# -*- coding: utf-8 -*-

from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = "account.move"

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