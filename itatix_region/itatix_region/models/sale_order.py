from odoo import fields, models, api,_

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    region_id = fields.Many2one(comodel_name="partner.region", string="Region",
                                domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                compute="_compute_region_id",store=True)

    @api.depends('opportunity_id')
    def _compute_region_id(self):
        for r in self:
            if r.opportunity_id:
                r.region_id = r.opportunity_id.region_id.id
            else:
                r.region_id = False