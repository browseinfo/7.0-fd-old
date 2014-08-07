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


class purchase_ledger_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(purchase_ledger_report, self).__init__(cr, uid, name, context)
        self.partner_name = ''
        self.partner_list = []
        self.index = 1
        self.line_quantity = 0
        self.localcontext.update({  
            'get_partner_data': self._get_partner_data,
            'get_partner_reference': self._get_partner_reference,
            'get_data': self._get_data,
            'get_start_date': self.get_start_date,
            'get_end_date': self.get_end_date,
            'get_partner': self.get_partner,
            'get_total_qty': self.get_total_qty,
            #'get_total_qty_cust': self.get_total_qty_cust,
            'get_subtotal_qty': self.get_subtotal_qty,
            'get_total_amount': self.get_total_amount,
 #           'get_page_break':self.get_page_break,
            'date_format': self.date_format,
            'get_partner_name': self.get_partner_name,
        })

    def set_context(self, objects, data, ids, report_type=None):
        obj_partner = self.pool.get('res.partner')
        start_date = data['form']['start_date']
        end_date = data['form']['end_date']
        formatter_string = "%Y-%m-%d" 
        datetime_object = datetime.strptime(start_date, formatter_string)
        date_object = datetime_object.date()
        datetime_object_to = datetime.strptime(end_date, formatter_string)
        date_object_to = datetime_object_to.date()
        self.start_date = date_object.strftime("%d-%B-%Y")
        self.end_date = date_object_to.strftime("%d-%B-%Y")
        self.cr.execute(
            "SELECT DISTINCT ai.partner_id  FROM account_invoice_line AS l "\
                "left join account_invoice as ai on (l.invoice_id = ai.id) "\
                "WHERE (ai.date_invoice >= %s) AND (ai.date_invoice <= %s) AND ai.type = 'in_invoice' AND ai.state not in ('draft', 'open') "\
                "group by l.id, ai.id,ai.partner_id", (self.start_date, self.end_date)
        )
        self.partner_ids = [x[0] for x in self.cr.fetchall()]
        objects = obj_partner.browse(self.cr, self.uid, self.partner_ids)
        return super(purchase_ledger_report, self).set_context(objects, data, self.partner_ids, report_type=report_type)

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def get_total_qty(self):
        return int(self.total_qty)

    def get_subtotal_qty(self):
        return self.total_sum

#     def get_total_qty_cust(self):
#         return int(self.qty)

    def get_total_amount(self):
        return self.total_amount

    def get_partner(self):
        return self.partner_name
    
#     def get_page_break(self,partner):
#         if index > 1:
#             print "hello page break============",partner
#             partner_obj = self.pool.get('res.partner')
#             self.partner_list.append(partner)
#             print "listpart============",self.partner_list
#         if partner not in list_part:
#              return True

    def _get_partner_data(self, obj):
        if obj:
            partner_name = obj.name or ''
        return partner_name

    def _get_partner_reference(self, obj):
        if obj:
            partner_ref = obj.ref or ''
        return partner_ref
    
    def get_partner_name(self, ref):
        for line in ref['values']:
            return line['partner_id']
            
    def _get_data(self, obj):
        inv_obj = self.pool.get('account.invoice')
        line_obj = self.pool.get('account.invoice.line')
        currency_obj = self.pool.get('res.currency')
        cur_obj = self.pool.get('res.currency.rate')
        self.total_qty = 0
        self.total_amount = 0.0
        self.sub_total_qty = 0
        res = []
        line_name = []
        self.cr.execute("select DISTINCT ai.id from account_invoice_line ail "\
        "left join account_invoice as ai on (ail.invoice_id = ai.id) "\
        "WHERE (ai.date_invoice >= %s) AND (ai.date_invoice <= %s)"\
        "AND ai.type = 'in_invoice' AND ai.state not in ('draft', 'open') "\
        "AND ai.partner_id = %s"\
        "group by ai.id,ai.partner_id", (self.start_date, self.end_date, obj.id))
        temp = [x[0] for x in self.cr.fetchall()]
        if temp:
            for inv in inv_obj.browse(self.cr, self.uid, temp):
                self.sub_total_qty = 0
                self.total_amount = self.total_amount + inv.amount_untaxed
                self.partner_name = inv.partner_id.name
                
                to_datelist = []
                from_datelist = []
                
                self.cr.execute(" select * from res_currency where name = 'USD' ")
                browse_curency = self.cr.fetchone()
                
                for to_curr_obj in currency_obj.browse(self.cr, self.uid, [browse_curency[0]]):
			        for to_rate_obj in to_curr_obj.rate_ids:
				        to_datelist.append(to_rate_obj.name)
                to_get_datetime = lambda s: datetime.strptime(s, "%Y-%m-%d")
                to_base = to_get_datetime(inv.date_invoice)
                to_later = filter(lambda d: to_get_datetime(d) <= to_base, to_datelist)
                to_closest_date = max(to_later, key = lambda d: to_get_datetime(d))
		
                to_rate_search = cur_obj.search(self.cr, self.uid, [('name', '=', to_closest_date), ('currency_id', '=', browse_curency[0])])[0]
                to_rate_browse = cur_obj.browse(self.cr, self.uid, to_rate_search)
                to_rate = to_rate_browse.rate
                
                for from_curr_obj in currency_obj.browse(self.cr, self.uid, [inv.currency_id.id]):
			        for from_rate_obj in from_curr_obj.rate_ids:
				        from_datelist.append(from_rate_obj.name)
                from_get_datetime = lambda s: datetime.strptime(s, "%Y-%m-%d")
                from_base = from_get_datetime(inv.date_invoice)
                from_later = filter(lambda d: from_get_datetime(d) <= from_base, from_datelist)
                from_closest_date = max(from_later, key = lambda d: from_get_datetime(d))
		
                from_rate_search = cur_obj.search(self.cr, self.uid, [('name', '=', from_closest_date), ('currency_id', '=', inv.currency_id.id)])[0]
                from_rate_browse = cur_obj.browse(self.cr, self.uid, from_rate_search)
                from_rate = from_rate_browse.rate
                
                rate = round((to_rate / from_rate), 2)

                for line in inv.invoice_line:
                    profit = 0.0 
                    profit_percent = 0.0
                    if line.product_id:
                        self.sub_total_qty = self.sub_total_qty + line.quantity
                    res.append({'date_invoice': self.date_format(inv.date_invoice),
                                'partner_id': inv.partner_id.name,
                                'number': inv.number,
                                'invoice_id': inv and inv.id or False,
                                'origin':inv.origin,
                                'default_code': line.product_id.default_code,
                                'product_id': line.product_id.name,
                                'quantity': int(line.quantity),
                                'qty_total': int(self.sub_total_qty),
                                'price_unit': line.price_unit,
                                'price_subtotal': line.price_subtotal,
                                'total_amount': inv.amount_untaxed,
                                'us_total_amount': (line.price_subtotal * rate),
                                'ref': inv.partner_id.ref or ''
                            })
                    self.total_qty = self.total_qty + line.quantity
                    
        newlist = sorted(res, key=lambda k: k['invoice_id'])
        groups = itertools.groupby(newlist, key=operator.itemgetter('invoice_id'))
        
        result = [{'invoice_id':k,'values':[x for x in v]} for k,v in groups]
        self.total_sum_qty = 0
        self.total_sum = 0
        for vals in result:
            self.qty_main_total = 0
            self.main_total = 0
            for loop in vals['values']:
                self.qty_main_total += loop['quantity']
                self.main_total += loop['us_total_amount']
            vals['total'] = self.qty_main_total
            vals['sum_total'] = self.main_total
            self.total_sum_qty += vals['total']
            self.total_sum += vals['sum_total']
            
        return result

        
    def date_format(self, datedetail):
        if datedetail:
            a = time.strptime(datedetail,'%Y-%m-%d')
            b = time.strftime('%d-%b-%Y', a)
            return b
        else:
            return ''
        
report_sxw.report_sxw('report.purchase.ledger.report', 'account.invoice', 'purchase_extended_webkit_report/report/purchase_ledger_report.rml', parser=purchase_ledger_report, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

