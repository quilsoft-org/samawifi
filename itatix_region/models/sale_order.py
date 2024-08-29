from odoo import fields, models, api,_

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    region_id = fields.Many2one(comodel_name="partner.region", string="Region",
                                domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                compute="_compute_region_id",store=True, inverse="_inverse_region_id")
    #Opportunity to Sale Order
    @api.depends('opportunity_id.region_id')
    def _compute_region_id(self):
        for r in self:
            r.region_id = r.opportunity_id.region_id.id if r.opportunity_id else False
            r._set_region_id()

    #Sale order to Opportunity
    def _inverse_region_id(self):
        for r in self:
            r.opportunity_id.region_id = r.region_id.id if r.region_id else False

    @api.onchange('region_id')
    def _set_region_id(self):
        for order in self:
            invoices = order.order_line.invoice_lines.move_id.filtered(
                lambda r: r.move_type in ('out_invoice', 'out_refund'))
            for i in invoices:
                i.region_id = order.region_id.id