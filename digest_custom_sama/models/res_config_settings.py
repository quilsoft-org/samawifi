# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    digest_emails = fields.Boolean(related='company_id.digest_emails', readonly=False)
    digest_id = fields.Many2one(related='company_id.digest_id', readonly=False)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()

        res['digest_emails'] = self.env.company.digest_emails
        res['digest_id'] = self.env.company.digest_id.id

        return res

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('digest.default_digest_emails', self.digest_emails)
        self.env['ir.config_parameter'].sudo().set_param('digest.default_digest_id', self.digest_id.id)

        super(ResConfigSettings, self).set_values()
