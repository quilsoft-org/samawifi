import calendar

from odoo import models, fields, api
from odoo.osv import expression

months = {
        'ENERO':1,
        'FEBRERO':2,
        'MARZO':3,
        'ABRIL':4,
        'MAYO':5,
        'JUNIO':6,
        'JULIO':7,
        'AGOSTO':8,
        'SEPTIEMBRE':9,
        'OCTUBRE':10,
        'NOVIEMBRE':11,
        'DICIEMBRE':12,
        'JANUARY':1,
        'FEBRUARY':2,
        'MARCH':3,
        'APRIL':4,
        'MAY':5,
        'JUNE':6,
        'JULY':7,
        'AUGUST':8,
        'SEPTEMBER':9,
        'OCTOBER':10,
        'NOVEMBER':11,
        'DECEMBER':12,
    }

class InvoiceReportSama(models.Model):
    _name = "invoice.report.sama"
    _auto = False
    _rec_name = 'date_order'
    _order = 'date_order desc'
    _description = 'Invoice Report Sama'

    # ==== Invoice fields ====
    move_id = fields.Many2one('account.move', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    user_id = fields.Many2one('res.users', string='Salesperson', readonly=True)
    team_id = fields.Many2one('crm.team', string='Sales Team')
    region_id = fields.Many2one('partner.region',string="Region")
    move_type = fields.Selection([
        ('out_invoice', 'Customer Invoice'),
        ('out_refund', 'Customer Credit Note'),
        ], readonly=True)
    date_order = fields.Date(readonly=True, string="Invoice Date")
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    product_categ_id = fields.Many2one('product.category', string='Product Category', readonly=True)
    price_subtotal = fields.Float(string='Achieve', readonly=True)
    product_sama_category_id = fields.Many2one('sama.category', copy=False)
    product_sama_subcategory_id = fields.Many2one('sama.subcategory', copy=False)
    product_sama_brand_id = fields.Many2one('sama.brand', copy=False)
    price_subtotal_usd = fields.Float(string='Achieve(USD)', readonly=True)
    amount_target = fields.Float(string='Quota', default= 0.0, readonly=True)
    gap = fields.Float(string='Gap', readonly=True)
    achieve_perct = fields.Float('Achievement %', readonly=True)

    _depends = {
        'account.move': [
            'name', 'state', 'move_type', 'partner_id', 'invoice_user_id', 'fiscal_position_id',
            'invoice_date', 'invoice_date_due', 'invoice_payment_term_id', 'partner_bank_id',
        ],
        'account.move.line': [
            'quantity', 'price_subtotal', 'amount_residual', 'balance', 'amount_currency',
            'move_id', 'product_id', 'product_uom_id', 'account_id', 'analytic_account_id',
            'journal_id', 'company_id', 'currency_id', 'partner_id',
        ],
        'product.product': ['product_tmpl_id'],
        'product.template': ['categ_id'],
        'uom.uom': ['category_id', 'factor', 'name', 'uom_type'],
        'res.currency.rate': ['currency_id', 'name'],
        'res.partner': ['country_id'],
    }

    @property
    def _table_query(self):
        return '%s %s %s' % (self._select(), self._from(), self._where())

    groupable_fields = ['user_id']
    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super(InvoiceReportSama, self).fields_get(allfields, attributes=attributes) 
        not_groupable_fields = set(self._fields.keys()) - set(self.groupable_fields)
        for field in not_groupable_fields:
            if field in res:
                res[field]['selectable'] = False ## Remove FilterBy       
                res[field]['sortable'] = False ## Remove FilterBy                
                res[field]['searchable'] = False ## Remove FilterBy                
        return res
        
    @api.model
    def _select(self):
        return '''
            SELECT
                line.id,
                line.move_id,
                line.company_id,
                line.product_id,
                move.move_type                                              AS move_type,
                move.invoice_user_id                                        AS user_id,
                move.team_id                                                AS team_id,
                move.region_id                                              AS region_id,
                move.invoice_date                                           AS date_order,
                template.categ_id                                           AS product_categ_id,
                template.sama_category_id                                   AS product_sama_category_id,
                template.sama_subcategory_id                                AS product_sama_subcategory_id,
                template.sama_brand_id                                      AS product_sama_brand_id,
                -line.balance * currency_table.rate                         AS price_subtotal,
                CASE WHEN move.amount_untaxed_signed < 0 THEN -line.price_subtotal * move.currency_rate_usd ELSE line.price_subtotal * move.currency_rate_usd END  AS price_subtotal_usd,
                0.0                                                         AS amount_target,
                0.0                                                         AS gap,
                0.0                                                         AS achieve_perct
        '''

    @api.model
    def _from(self):
        return '''
            FROM account_move_line line
                LEFT JOIN product_product product ON product.id = line.product_id
                LEFT JOIN product_template template ON template.id = product.product_tmpl_id
                INNER JOIN account_move move ON move.id = line.move_id
                JOIN {currency_table} ON currency_table.company_id = line.company_id
        '''.format(
            currency_table=self.env['res.currency']._get_query_currency_table({'multi_company': True, 'date': {'date_to': fields.Date.today()}}),
        )

    @api.model
    def _where(self):
        return '''
            WHERE move.move_type IN ('out_invoice','out_refund')
                AND move.state NOT IN ('draft', 'cancel')
                AND line.account_id IS NOT NULL
                AND NOT line.exclude_from_invoice_tab
        '''

    @api.model
    def read_group_bad(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        result = super(InvoiceReportSama, self).read_group(domain, fields, groupby, offset, limit, orderby, lazy)
        reverse_domain = domain.copy()
        reverse_domain.reverse()
        date_domain = []
        for item in reverse_domain:
            if (isinstance(item, list) and len(item) == 3 and item[0] == 'date_order'):
                item_copy = item.copy()
                date_domain.append(item_copy)
            elif item in ('|','&'):
                date_domain.append(item)
            else:
                break

        date_domain.reverse()

        if 'user_id' in groupby:
            for line in result:
                if 'amount_target' in line:
                    line['amount_target'] = 0.0
                    line_domain = date_domain.copy()
                    if 'date_order:month' in line:
                        date = line['date_order:month'].split(' ')
                        month = months[date[0].upper()]
                        year = int(date[1])
                        first, last = calendar.monthrange(year, month)
                        date_begin = "%s-%.2d-01"%(date[1], month)
                        date_end = "%s-%.2d-%.2d"%(date[1], month, last)
                        line_domain = [('date_order', '>=', date_begin), ('date_order', '<=', date_end)]

                    if 'user_id' in line and line['user_id']:
                        line_domain = expression.AND([line_domain, [('user_id','=',line['user_id'][0])]])
                        target_lines = self.env['sales.target.lines'].search(line_domain)
                        amount_target = sum(target_lines.mapped('monthly_target'))
                        line['amount_target'] = amount_target

                if 'gap' in line:
                    line['gap'] = line.get('price_subtotal_usd', 0.0) - line.get('amount_target', 0.0)

                if 'achieve_perct' in line:
                    line['achieve_perct'] = line.get('price_subtotal_usd', 0.0) * 100.0 / (line.get('amount_target', 0.0) or 1.0)

        elif 'team_id' in groupby:
            for line in result:
                if 'amount_target' in line:
                    line['amount_target'] = 0.0
                    line_domain = date_domain.copy()
                    if 'date_order:month' in line:
                        date = line['date_order:month'].split(' ')
                        month = months[date[0].upper()]
                        year = int(date[1])
                        first, last = calendar.monthrange(year, month)
                        date_begin = "%s-%.2d-01"%(date[1], month)
                        date_end = "%s-%.2d-%.2d"%(date[1], month, last)
                        line_domain = [('date_order', '>=', date_begin), ('date_order', '<=', date_end)]

                    if 'team_id' in line and line['team_id']:
                        team_id = line['team_id'][0]
                        team = self.env['crm.team'].browse(int(team_id))
                        line_domain = expression.AND([line_domain, [('user_id','in',team.member_ids.ids)]])
                        target_lines = self.env['sales.target.lines'].search(line_domain)
                        amount_target = sum(target_lines.mapped('monthly_target'))
                        line['amount_target'] = amount_target

                if 'gap' in line:
                    line['gap'] = line.get('price_subtotal_usd', 0.0) - line.get('amount_target', 0.0)

                if 'achieve_perct' in line:
                    line['achieve_perct'] = line.get('price_subtotal_usd', 0.0) * 100.0 / (line.get('amount_target', 0.0) or 1.0)
        elif 'region_id' in groupby:
            for line in result:
                if 'amount_target' in line:
                    line['amount_target'] = 0.0
                    line_domain = date_domain.copy()
                    if 'date_order:month' in line:
                        date = line['date_order:month'].split(' ')
                        month = months[date[0].upper()]
                        year = int(date[1])
                        first, last = calendar.monthrange(year, month)
                        date_begin = "%s-%.2d-01"%(date[1], month)
                        date_end = "%s-%.2d-%.2d"%(date[1], month, last)
                        line_domain = [('date_order', '>=', date_begin), ('date_order', '<=', date_end)]

                    if 'region_id' in line and line['region_id']:
                        region_id = line['region_id'][0]
                        region = self.env['partner.region'].browse(int(region_id))
                        line_domain = expression.AND([line_domain, [('region_id','in',region_id.id)]])
                        target_lines = self.env['sales.target.lines'].search(line_domain)
                        amount_target = sum(target_lines.mapped('monthly_target'))
                        line['amount_target'] = amount_target

                if 'gap' in line:
                    line['gap'] = line.get('price_subtotal_usd', 0.0) - line.get('amount_target', 0.0)

                if 'achieve_perct' in line:
                    line['achieve_perct'] = line.get('price_subtotal_usd', 0.0) * 100.0 / (line.get('amount_target', 0.0) or 1.0)

        return result
    
    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        result = super(InvoiceReportSama, self).read_group(domain, fields, groupby, offset, limit, orderby, lazy)
        print('domain', domain, "\n")

        for line in result:
            print('line', line)
            line.setdefault('price_subtotal_usd', 0.0)
            try:
                __domain = line.get('__domain', [])
                print('__domain', __domain)
                if not __domain:
                    __domain = domain
                target_lines = self.env['sales.target.lines'].search(__domain)
                amount_target = sum(target_lines.mapped('monthly_target'))
                line['amount_target'] = amount_target
            except:
                line['amount_target'] = 0.0

            if 'gap' in line:
                try:
                    line['gap'] = line.get('price_subtotal_usd', 0.0) - line.get('amount_target', 0.0)
                except:
                    line['gap'] = 0.0

            if 'achieve_perct' in line:
                try:
                    line['achieve_perct'] = line.get('price_subtotal_usd', 0.0) * 100.0 / (line.get('amount_target', 0.0) or 1.0)
                except:
                    line['achieve_perct'] = 0.0

        return result
