from odoo import fields, models, api,_
from odoo.exceptions import UserError

class CrmLead(models.Model):
    _inherit = 'account.move'

    region_id = fields.Many2one(comodel_name="partner.region", string="Region",
                                domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                compute='_compute_region_id',store=True,inverse="_inverse_region_id"
                                )

    @api.depends('invoice_origin')
    def _compute_region_id(self):
        for r in self:
            if r.invoice_origin:
                so = self.env['sale.order'].search([('name','=',r.invoice_origin)])
                r.region_id = so.region_id.id if so else False
            else:
                r.region_id = False

    def _inverse_region_id(self):
        for r in self:
            if r.invoice_origin:
                so = self.env['sale.order'].search([('name', '=', r.invoice_origin)])
                if so:
                    so.region_id = r.region_id.id if r.region_id else False
