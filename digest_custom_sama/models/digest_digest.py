from odoo import fields, models


class DigestDigestInherit(models.Model):
    _inherit = 'digest.digest'

    def _get_kpi_compute_parameters(self):
        return fields.Date.to_string(self._context.get('start_date')), fields.Date.to_string(self._context.get('end_date')), self.company_id
