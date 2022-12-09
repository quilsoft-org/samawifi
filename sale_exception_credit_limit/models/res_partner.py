from odoo import fields,models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    credit_limit = fields.Float(string='Credit Limit', default="1.0")