from odoo import fields, models, api,_
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_real_cost = fields.Monetary(string="Costo Real", compute='_compute_real_margin', store=True)
    real_margin = fields.Monetary(string="Margen Real", compute='_compute_real_margin', store=True)
    real_margin_percent = fields.Float(string="Margen Real (%)", compute='_compute_real_margin', store=True)
    
    
    @api.depends('order_line.real_margin','order_line.real_cost_subtotal', 'amount_untaxed')
    def _compute_real_margin(self):
        if not all(self._ids):
            for order in self:
                order.total_real_cost = sum(order.order_line.mapped('real_cost_subtotal'))
                order.real_margin = sum(order.order_line.mapped('real_margin'))
                order.real_margin_percent = order.amount_untaxed and order.real_margin / order.amount_untaxed
        else:
            self.env["sale.order.line"].flush(['real_margin'])
            # On batch records recomputation (e.g. at install), compute the margins
            # with a single read_group query for better performance.
            # This isn't done in an onchange environment because (part of) the data
            # may not be stored in database (new records or unsaved modifications).
            grouped_order_lines_data = self.env['sale.order.line'].read_group(
                [
                    ('order_id', 'in', self.ids),
                ], ['real_margin', 'order_id'], ['order_id'])
            mapped_data = {m['order_id'][0]: m['real_margin'] for m in grouped_order_lines_data}
            for order in self:
                order.total_real_cost = sum(order.order_line.mapped('real_cost_subtotal'))
                order.real_margin = mapped_data.get(order.id, 0.0)
                order.real_margin_percent = order.amount_untaxed and order.real_margin / order.amount_untaxed
    
    
    def action_confirm(self):
        for line in self.order_line:        
            if line.real_cost <=0 and line.display_type != 'line_section' and  line.display_type != 'line_note':
                raise UserError(_('El costo real debe de ser mayor a cero en cada una de las lineas'))
        
        return super(SaleOrder,self).action_confirm()
    




class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    real_cost = fields.Float(string="Costo Real")
    real_cost_subtotal = fields.Float(string="Costo Real Subtotal",compute='_compute_real_margin', store=True)
    real_margin = fields.Monetary(string="Margen Real", compute='_compute_real_margin', store=True)
    real_margin_percent = fields.Float(string="Margen Real (%)", compute='_compute_real_margin', store=True)

    @api.depends('real_cost', 'product_uom_qty','price_subtotal')
    def _compute_real_margin(self):
        for line in self:
            line.real_cost_subtotal = line.real_cost * line.product_uom_qty
            line.real_margin = line.price_subtotal - line.real_cost_subtotal
            line.real_margin_percent = line.price_subtotal and (line.real_margin / line.price_subtotal)*100