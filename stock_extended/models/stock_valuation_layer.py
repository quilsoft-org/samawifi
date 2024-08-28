from odoo import fields, models, api, _

class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'
    
    mx_value = fields.Float(string=_("Valor MXN"),compute="_compute_data")
    usd_value = fields.Float(string=_("Valor USD"),compute="_compute_data")
    rate_value = fields.Float(string=_("Tasa"),compute="_compute_rate")

    def _compute_rate(self):
        for record in self:
            usd_rate = self.env['res.currency.rate'].search(
                [('currency_id', '=', self.env.ref('base.MXN').id),('company_id','=',2)],limit=1,order="name desc")
            record.rate_value = usd_rate.rate
     
    def _compute_data(self):
        for record in self:
            record = record.with_company(record.company_id)
            mxn_currency = self.env.ref('base.MXN')
            usd_currency = self.env.ref('base.USD')
            if record.company_id.currency_id.id == mxn_currency.id:
                record.mx_value = record.value
                if record.rate_value > 0:
                    record.usd_value = record.value / record.rate_value
                else:
                    record.usd_value = record.value
                
            if record.company_id.currency_id.id == usd_currency.id:
                record.mx_value = record.value * record.rate_value
                record.usd_value = record.value
    
    @api.model 
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        res = super().read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)
        if 'mx_value' in fields:
            for line in res:
                if '__domain' in line:
                    lines = self.search(line['__domain'])
                    total_mx_value = 0.0
                    for record in lines:
                        total_mx_value += record.mx_value
                    line['mx_value'] = total_mx_value
        if 'usd_value' in fields:
            for line in res:
                if '__domain' in line:
                    lines = self.search(line['__domain'])
                    total_usd_value = 0.0
                    for record in lines:
                        total_usd_value += record.usd_value
                    line['usd_value'] = total_usd_value
        if 'rate_value' in fields:
            for line in res:
                if '__domain' in line:
                    lines = self.search(line['__domain'])
                    total_rate_value = 0.0
                    for record in lines:
                        total_rate_value += record.rate_value
                    line['rate_value'] = total_rate_value / len(lines)

        return res
