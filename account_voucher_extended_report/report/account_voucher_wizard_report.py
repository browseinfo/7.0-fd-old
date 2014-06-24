# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2014-Today BrowseInfo (<http://www.browseinfo.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

import time
import operator
import itertools
from datetime import datetime
from dateutil import relativedelta
from report import report_sxw
from openerp.tools.amount_to_text_en import amount_to_text
import time
from datetime import datetime
from openerp.osv import osv, fields
from openerp.tools.translate import _ 

class account_voucher_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(account_voucher_report, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            #'mergelines': self.mergelines,
            'date_format': self.date_format,
            'get_begining_balance': self.get_begining_balance,
            'sum_debit': self.sum_debit,
            'sum_credit': self.sum_credit,
            'sum_closing': self.sum_closing,
            'get_rate': self.get_rate,
            'get_balance_idr': self.get_balance_idr,
        })
        
    def merge_lists(self,l1, l2, key):
        merged = {}
        for item in l1+l2:
            if item[key] in merged:
                merged[item[key]].update(item)
            else:
                merged[item[key]] = item
        return [val for (_, val) in merged.items()]

    def sum_debit(self):
        return self.debit_total

    def sum_credit(self):
        return self.credit_total

    def sum_closing(self):
        return self.closing_total


    def set_context(self, objects, data, ids, report_type=None):
        period_obj = self.pool.get('account.period')
        move_line_obj = self.pool.get('account.move.line')
        jrnl_obj = self.pool.get('account.journal')
        cur_obj = self.pool.get('res.currency.rate')
        period_browse = period_obj.browse(self.cr, self.uid, data['form']['period_id'][0])
        self.period_id = data['form']['period_id']
        start_date = period_browse.date_start
        end_date = period_browse.date_stop
        self.journal_id = data['form']['journal_id'][0]
        jrnl_browse = jrnl_obj.browse(self.cr, self.uid, data['form']['journal_id'][0])
        self.browse_curency = jrnl_browse.currency
        if not self.browse_curency:
           raise osv.except_osv(_('Warning'), _('There is no Currency Defined For Selected Journal'))
        for self.newrate in self.browse_curency.rate_ids:
            self.datecmp = self.newrate.name
        formatter_string = "%Y-%m-%d" 
        datetime_object = datetime.strptime(start_date, formatter_string)
        date_object = datetime_object.date()
        datetime_object_to = datetime.strptime(end_date, formatter_string)
        date_object_to = datetime_object_to.date()
        self.start_date = date_object.strftime("%d-%B-%Y")
        self.end_date = date_object_to.strftime("%d-%B-%Y")
        self.cr.execute("SELECT pl.id from account_move_line as pl "\
                        "WHERE pl.period_id = %s "\
                        "ORDER BY date",
                        (self.period_id[0],))
        self.voucher_ids = [x[0] for x in self.cr.fetchall()]
        objects = move_line_obj.browse(self.cr, self.uid, self.voucher_ids)
        return super(account_voucher_report, self).set_context(objects, data, ids, report_type=report_type)

    def get_rate(self):
        return self.rate

    def get_balance_idr(self):
        return self.idr_balance

    def get_begining_balance(self, obj):
		move_obj = self.pool.get('account.move')
		payslip_line = self.pool.get('account.move.line')
		voucher_line = self.pool.get('account.voucher.line')
		currency_obj = self.pool.get('res.currency')
		cur_obj = self.pool.get('res.currency.rate')
		move_lines = []
		res = []
		result = {}
		idr_debit = 0.0
		idr_credit = 0.0
		usd_debit = 0.0
		usd_credit = 0.0
		jpy_debit = 0.0
		self.debit_total = 0.0
		self.credit_total = 0.0
		self.closing_total = 0.0
		self.opening_total = 0.0
		self.idr_balance = 0.0
		opening_balance = 0.0

		self.cr.execute("SELECT SUM(debit), sum(credit) from account_move_line as pl "\
                        "WHERE pl.period_id < %s "\
                        "GROUP BY pl.date ORDER BY pl.date", (self.period_id[0],))
		fetch = self.cr.fetchall()
		if len(fetch) > 0:
			sumcredit = sumdebit = 0
			for period in fetch:
				sumdebit += period[0]
				sumcredit += period[1]
			opening_balance = sumdebit - sumcredit
		self.opening_total = opening_balance
		self.cr.execute("SELECT pl.id from account_move_line as pl "\
                        "WHERE pl.period_id = %s "\
                        "ORDER BY date",
                        (self.period_id[0],))
		move_lines = [x[0] for x in self.cr.fetchall()]

		newids = []
		lessids = []
		counter = 0
		for line in payslip_line.browse(self.cr, self.uid, move_lines):
			datelist= []
			for curr_obj in currency_obj.browse(self.cr, self.uid, [self.browse_curency.id]):
				for rate_obj in curr_obj.rate_ids:
					datelist.append(rate_obj.name)
			get_datetime = lambda s: datetime.strptime(s, "%Y-%m-%d")
			base = get_datetime(line.date)
			later = filter(lambda d: get_datetime(d) <= base, datelist)
			closest_date = max(later, key = lambda d: get_datetime(d))
			
			rate_search = cur_obj.search(self.cr, self.uid, [('name', '=', closest_date), ('currency_id', '=', self.browse_curency.id)])[0]
			rate_browse = cur_obj.browse(self.cr, self.uid, rate_search)
			self.rate = rate_browse.rate
			res.append({
				'id': line.id,
				'journal': line.journal_id.name,
				'partner': line.partner_id.name,
				'name': line.name,
				'ref':line.ref,
				'account': line.account_id.code,
				'move': line.move_id.name,
				'date': self.date_format(line.date),
				'rateof': self.rate,
				'debit': line.debit,
				'credit': line.credit,
				'reconcile': line.reconcile,
				'opening_balance': opening_balance,
				'new_balance': opening_balance * self.rate,
				'idr_debit': idr_debit,
				'idr_credit': idr_credit,
				'jpy_debit': jpy_debit,
			})
			if line.debit and line.credit:
				latest_balance = opening_balance + (line.debit - line.credit)
			elif line.debit and not line.credit:
				latest_balance = opening_balance + line.debit
			else:
				latest_balance = opening_balance - line.credit
			opening_balance = latest_balance
			self.debit_total += line.debit
			self.credit_total += line.credit
			self.closing_total = opening_balance
			self.idr_balance = latest_balance * self.rate
	
		groups = itertools.groupby(res, key=operator.itemgetter('jpy_debit'))
		result = [{'date':k,'values':[x for x in v]} for k, v in groups]
		self.total_sum = 0
		for vals in result:
			self.qty_main_total = 0
			self.main_total = 0
			for loop in vals['values']:
				self.main_total += loop['opening_balance']
			vals['opening'] = self.main_total
			self.total_sum += vals['opening']
	
		return result
#     def get_voucher_data(self, obj):
#         voucher_obj = self.pool.get('account.voucher')
#         line_obj = self.pool.get('account.voucher.line')
#         res = []
#         moveres = []
#         newres = []
#         line_name = []
#         self.cr.execute("select DISTINCT av.id from account_voucher_line avl "\
#         "left join account_voucher as av on (avl.voucher_id = av.id) "\
#         "WHERE (av.date >= %s) AND (av.date <= %s)"\
#         "AND journal_id =%s", (self.start_date, self.end_date, self.journal_id))
#         temp = [x[0] for x in self.cr.fetchall()]
#         if temp:
#             for voucher in voucher_obj.browse(self.cr, self.uid, temp):
#                 for line in voucher.line_ids:
#                     res.append({
#                                 'date': self.date_format(voucher.date),
#                                 'number': voucher.number or '',
#                                 'name': line.name or '',
#                                 'account_id': line.account_id.code or '',
#                                 'partner_id': voucher.partner_id.name,
#                                
#                             })
#             return res
#                 
#     def get_move_data(self, obj):
#         voucher_obj = self.pool.get('account.voucher')
#         line_obj = self.pool.get('account.voucher.line')
#         res = []
#         moveres = []
#         newres = []
#         line_name = []
#         idr_debit = 0.0
#         idr_credit = 0.0
#         usd_debit = 0.0
#         usd_credit = 0.0
#         jpy_debit = 0.0
#         self.cr.execute("select DISTINCT av.id from account_voucher_line avl "\
#         "left join account_voucher as av on (avl.voucher_id = av.id) "\
#         "WHERE (av.date >= %s) AND (av.date <= %s)"\
#         "AND journal_id =%s", (self.start_date, self.end_date, self.journal_id))
#         temp = [x[0] for x in self.cr.fetchall()]
#         if temp:
#             for voucher in voucher_obj.browse(self.cr, self.uid, temp):
#                 for moveline in voucher.move_ids:
#                     if voucher.journal_id.currency.name == 'IDR':
#                         idr_debit = moveline.debit
#                         idr_credit = moveline.credit
#                     if voucher.journal_id.currency.name == 'USD':
#                          usd_debit = moveline.debit
#                          usd_credit = moveline.credit
#                     else: #voucher.journal_id.currency.name == 'JPY':
#                         jpy_debit = moveline.debit
#                     res.append({
#                                 'number': voucher.number or '',
#                                 'idr_debit': idr_debit,
#                                 'idr_credit': idr_credit,
#                                 'usd_debit': usd_debit,
#                                 'usd_credit': usd_credit,
#                                 'jpy_debit': jpy_debit,
#                             })
#             return res
# 
#     def mergelines(self, obj):
#         oldfields = []
#         newfields = []
#         newres = []
#         newlist = []
# 
#         res = self.get_voucher_data(obj)
#         for resval in res:
#             linedict = {
#                     'date': resval['date'],
#                     'number': resval['number'],
#                     'name': resval['name'],
#                     'account_id': resval['account_id'],
#                     'partner_id': resval['partner_id'],
#                 }
#             oldfields.append(linedict) 
#             
#             
#         newline = self.get_move_data(obj)  
#         for newval in newline:
#             newlinedict = {
#                     'number': newval['number'],
#                     'idr_debit': newval['idr_debit'],
#                     'idr_credit': newval['idr_credit'],
#                     'usd_debit': newval['usd_debit'],
#                     'usd_credit': newval['usd_credit'],
#                     'jpy_debit': newval['jpy_debit'],
#                 }
#             
#             newfields.append(newlinedict)
#             
#             
#         new = self.merge_lists(oldfields, newfields, 'number')
#         if new:
#             for data in new:
#                 newres.append({
#                     'date': data.get('date', False),
#                     'number': data.get('number', False),
#                     'name': data.get('name', False),
#                     'account_id': data.get('account_id', False),
#                     'partner_id': data.get('partner_id', False),
#                     'idr_debit': data.get('idr_debit',0.0),
#                     'idr_credit': data.get('idr_credit',0.0),
#                     'usd_debit': data.get('usd_debit',0.0),
#                     'usd_credit': data.get('usd_credit',0.0),
#                     'jpy_debit': data.get('jpy_debit',0.0),
#                  })
#                         
#         return newres
                    


    def date_format(self, datedetail):
        if datedetail:
            a = time.strptime(datedetail,'%Y-%m-%d')
            b = time.strftime('%d-%B-%Y', a)
            return b
        else:
            return ''

report_sxw.report_sxw('report.account.invoice.report.voucher', 'account.voucher', 'account_voucher_extended_report/report/account_voucher_report.mako', parser=account_voucher_report, header=False)
