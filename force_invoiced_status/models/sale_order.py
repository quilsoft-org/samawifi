from odoo import models, api, fields, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    force_invoiced_status = fields.Selection([
        ('no', 'Nothing to Invoice'),
        ('invoiced', 'Fully Invoiced')],
        tracking=True,
        copy=False,
    )

    @api.constrains('force_invoiced_status')
    def check_force_invoiced_status(self):
        group = self.sudo().env.ref('base.group_system')
        for rec in self:
            if rec.force_invoiced_status and not self.user_has_groups('base.group_system'):
                raise ValidationError(_(
                    'Only users with "%s / %s" can Set Invoiced manually') % (
                    group.category_id.name, group.name))

