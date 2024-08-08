from odoo import _, api, fields, models


class ResCompanyInherit(models.Model):
    _inherit = 'res.company'

    digest_emails = fields.Boolean(string='Resumen Activo')
    digest_id = fields.Many2one('digest.digest', string='Plantilla de Resumen') 
