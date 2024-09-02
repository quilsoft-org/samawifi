from odoo import api, fields, models


class ProductSupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    discount = fields.Float(string="Discount (%)", digits="Discount")
    price_list = fields.Float(digits="Price list")

    @api.onchange("name")
    def onchange_name(self):
        for supplierinfo in self.filtered("name"):
            supplierinfo.discount = supplierinfo.name.default_supplierinfo_discount

    @api.model
    def _get_po_to_supplierinfo_synced_fields(self):
        return ["discount"]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            product_tmpl_id = vals["product_tmpl_id"]
            po_line_map = self.env.context.get("po_line_map", {})
            if product_tmpl_id in po_line_map:
                po_line = po_line_map[product_tmpl_id]
                for field in self._get_po_to_supplierinfo_synced_fields():
                    if not vals.get(field):
                        vals[field] = po_line[field]
        return super().create(vals_list)
