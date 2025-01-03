# -*- coding: utf-8 -*-

from odoo import models, fields, api

from functools import lru_cache

import logging
_logger = logging.getLogger(__name__)

class AccountInvoiceAnalysisReport(models.Model):
    _name = "account.invoice.analysis.report.usd"
    _description = "Invoices Analysis Report in USD"
    _auto = False
    _rec_name = 'invoice_date'
    _order = 'invoice_date desc'

    # ==== Invoice fields ====
    move_id = fields.Many2one('account.move', readonly=True)
    journal_id = fields.Many2one('account.journal', string='Journal', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    company_currency_id = fields.Many2one('res.currency', string='Company Currency', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner', readonly=True)
    commercial_partner_id = fields.Many2one('res.partner', string='Partner Company', help="Commercial Entity")
    country_id = fields.Many2one('res.country', string="Country")
    invoice_user_id = fields.Many2one('res.users', string='Salesperson', readonly=True)
    move_type = fields.Selection([
        ('out_invoice', 'Customer Invoice'),
        ('in_invoice', 'Vendor Bill'),
        ('out_refund', 'Customer Credit Note'),
        ('in_refund', 'Vendor Credit Note'),
        ], readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Open'),
        ('cancel', 'Cancelled')
        ], string='Invoice Status', readonly=True)
    payment_state = fields.Selection(selection=[
        ('not_paid', 'Not Paid'),
        ('in_payment', 'In Payment'),
        ('paid', 'paid')
    ], string='Payment Status', readonly=True)
    fiscal_position_id = fields.Many2one('account.fiscal.position', string='Fiscal Position', readonly=True)
    invoice_date = fields.Date(readonly=True, string="Invoice Date")

    # ==== Invoice line fields ====
    quantity = fields.Float(string='Product Quantity', readonly=True)
    price_unit = fields.Float(string="Precio unitario", readonly=True)
    discount = fields.Float(string="Descuento", readonly=True)
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure', readonly=True)
    product_categ_id = fields.Many2one('product.category', string='Product Category', readonly=True)
    invoice_date_due = fields.Date(string='Due Date', readonly=True)
    account_id = fields.Many2one('account.account', string='Revenue/Expense Account', readonly=True, domain=[('deprecated', '=', False)])
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', groups="analytic.group_analytic_accounting")
    price_subtotal = fields.Float(string='Untaxed Total', readonly=True)
    price_average = fields.Float(string='Average Price', readonly=True, group_operator="avg")

    #Margin custom fields
    real_margin = fields.Float(string="Margen Real", readonly=True)
    real_margin_percent = fields.Float(string="Margen Real (%)", readonly=True)
    real_cost = fields.Float(string="Costo Real", readonly=True)
    
    #Product SAMA custom fields
    product_sama_category_id = fields.Many2one('sama.category', copy=False)
    product_sama_subcategory_id = fields.Many2one('sama.subcategory', copy=False)
    product_sama_brand_id = fields.Many2one('sama.brand', copy=False)
    price_subtotal_usd = fields.Float(string='Untaxed Total(USD)', readonly=True)
    region_id = fields.Many2one('partner.region', readonly=True)

    _depends = {
        'account.move': [
            'name', 'state', 'move_type', 'partner_id', 'invoice_user_id', 'fiscal_position_id',
            'invoice_date', 'invoice_date_due', 'invoice_payment_term_id', 'partner_bank_id',
        ],
        'account.move.line': [
            'quantity', 'price_unit', 'discount', 'price_subtotal', 'amount_residual', 'balance', 'amount_currency',
            'move_id', 'product_id', 'product_uom_id', 'account_id', 'analytic_account_id',
            'journal_id', 'company_id', 'currency_id', 'partner_id', 'real_cost', 'real_margin', 
            'real_margin_percent', 'real_cost',
        ],
        'product.product': ['product_tmpl_id'],
        'product.template': ['categ_id'],
        'uom.uom': ['category_id', 'factor', 'name', 'uom_type'],
        'res.currency.rate': ['currency_id', 'name'],
        'res.partner': ['country_id'],
    }

    @property
    def _table_query(self):
        query = '%s %s %s' % (self._select(), self._from(), self._where())
        _logger.info('*******************QUERY********************')
        _logger.info(query)
        return '%s %s %s' % (self._select(), self._from(), self._where())

    @api.model
    def _select(self):
        return '''
            SELECT
                line.id,
                line.move_id,
                line.product_id,
                line.account_id,
                line.analytic_account_id,
                line.journal_id,
                line.company_id,
                line.company_currency_id,
                line.partner_id AS commercial_partner_id,
                move.state,
                move.move_type,
                move.partner_id,
                move.invoice_user_id,
                move.fiscal_position_id,
                move.payment_state,
                move.invoice_date,
                move.invoice_date_due,
                move.region_id,
                uom_template.id                                             AS product_uom_id,
                template.categ_id                                           AS product_categ_id,
                template.sama_category_id                                   AS product_sama_category_id,
                template.sama_subcategory_id                                AS product_sama_subcategory_id,
                template.sama_brand_id                                      AS product_sama_brand_id,
                CASE WHEN move.amount_untaxed_signed < 0 THEN -line.price_subtotal * move.currency_rate_usd ELSE line.price_subtotal * move.currency_rate_usd END  AS price_subtotal_usd,
                line.quantity / NULLIF(COALESCE(uom_line.factor, 1) / COALESCE(uom_template.factor, 1), 0.0) * (CASE WHEN move.move_type IN ('in_invoice','out_refund','in_receipt') THEN -1 ELSE 1 END)
                                                                            AS quantity,
                line.price_unit,
                line.discount,
                line.price_subtotal AS price_subtotal,
                COALESCE(
                   -- Average line price
                   (line.price_subtotal / NULLIF(line.quantity, 0.0)) * (CASE WHEN move.move_type IN ('in_invoice','out_refund','in_receipt') THEN -1 ELSE 1 END)
                   -- convert to template uom
                   * (NULLIF(COALESCE(uom_line.factor, 1), 0.0) / NULLIF(COALESCE(uom_template.factor, 1), 0.0)),
                   0.0) * currency_table.rate                               AS price_average,
                COALESCE(partner.country_id, commercial_partner.country_id) AS country_id,
                (CASE WHEN line.company_currency_id <> 2 THEN 
                 (CASE WHEN move.amount_untaxed_signed < 0 THEN -line.price_subtotal * move.currency_rate_usd ELSE line.price_subtotal * move.currency_rate_usd END) - (line.real_cost * line.quantity)
                 ELSE line.real_margin END) AS real_margin, 
                
                
                (CASE WHEN line.company_currency_id <> 2 THEN 
( 
(CASE WHEN line.company_currency_id <> 2 THEN 
    (CASE WHEN move.amount_untaxed_signed < 0 THEN -line.price_subtotal * move.currency_rate_usd ELSE line.price_subtotal * move.currency_rate_usd END) - 
	(line.real_cost * line.quantity)
                 ELSE line.real_margin END) 
/ 
COALESCE(NULLIF((CASE WHEN move.amount_untaxed_signed < 0 THEN -line.price_subtotal * move.currency_rate_usd ELSE line.price_subtotal * move.currency_rate_usd END),0),1)
) * 100 
ELSE line.real_margin_percent END) AS real_margin_percent,

                (line.real_cost * line.quantity) AS real_cost
        '''

    # ((CASE WHEN line.company_currency_id <> 2 THEN line.real_cost * move.currency_rate_usd ELSE line.real_cost END) * line.quantity) AS real_cost

    @api.model
    def _from(self):
        return '''
            FROM account_move_line line
                LEFT JOIN res_partner partner ON partner.id = line.partner_id
                LEFT JOIN product_product product ON product.id = line.product_id
                LEFT JOIN account_account account ON account.id = line.account_id
                LEFT JOIN account_account_type user_type ON user_type.id = account.user_type_id
                LEFT JOIN product_template template ON template.id = product.product_tmpl_id
                LEFT JOIN uom_uom uom_line ON uom_line.id = line.product_uom_id
                LEFT JOIN uom_uom uom_template ON uom_template.id = template.uom_id
                INNER JOIN account_move move ON move.id = line.move_id
                LEFT JOIN res_partner commercial_partner ON commercial_partner.id = move.commercial_partner_id
                JOIN {currency_table} ON currency_table.company_id = line.company_id
        '''.format(
            currency_table=self.env['res.currency']._get_query_currency_table({'multi_company': True, 'date': {'date_to': fields.Date.today()}}),
        )

    @api.model
    def _where(self):
        return '''
            WHERE move.move_type IN ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt')
                AND line.account_id IS NOT NULL
                AND NOT line.exclude_from_invoice_tab
        '''

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        res = super(AccountInvoiceAnalysisReport, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
                                                           orderby=orderby,
                                                           lazy=lazy)
        groupby = [groupby] if isinstance(groupby, str) else groupby

        for record in res:

            if "real_margin" in record:
                # if record['price_subtotal']:
                if record.get('price_subtotal_usd', False):
                    # record['real_margin_percent'] = (record['real_margin'] / record['price_subtotal']) * 100
                    record['real_margin_percent'] = (record['real_margin'] / record['price_subtotal_usd']) * 100
                else:
                    record['real_margin_percent'] = record['real_margin'] or 1.0 / 1.0
        if not groupby:
            for record in res:
                if "real_margin" in record:
                    # if record['price_subtotal']:
                    if record.get('price_subtotal_usd', False):
                        # record['real_margin_percent'] = (record['real_margin'] / record['price_subtotal']) * 100
                        record['real_margin_percent'] = (record['real_margin'] / record['price_subtotal_usd']) * 100
                    else:
                        record['real_margin_percent'] = record['real_margin'] or 1.0 / 1.0
        return res
AccountInvoiceAnalysisReport()