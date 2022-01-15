from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    region_id = fields.Many2one(comodel_name="partner.region",string="Region",
                                domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")


class Region(models.Model):
    _name = "partner.region"

    name = fields.Char(string="Nombre de la region")
    company_id = fields.Many2one('res.company', 'Company', required=True, default=lambda self: self.env.company)
