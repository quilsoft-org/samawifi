from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    region_id = fields.Many2one(comodel_name="partner.region",string="Region")
