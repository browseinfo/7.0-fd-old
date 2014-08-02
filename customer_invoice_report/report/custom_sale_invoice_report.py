# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014-Today BrowseInfo (<http://www.browseinfo.in>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import time
from openerp.report import report_sxw
from openerp.osv import fields, osv, orm
import datetime


import time
import operator
import itertools

from dateutil import relativedelta
from report import report_sxw
from openerp.tools.amount_to_text_en import amount_to_text



class custom_inv_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(custom_inv_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
                                  
            'get_order_lines': self.get_order_lines,
            'get_total_sum': self.get_total_sum,
            'get_date_form': self.get_date_form,
            'get_date_to': self.get_date_to,
            'get_total_qty': self.get_total_qty,
            'get_total_amount': self.get_total_amount,
            'get_subtotal_qty': self.get_subtotal_qty,
            'get_start_date': self.get_start_date,
            'get_end_date': self.get_end_date,
            'get_total_amount_us': self.get_total_amount_us,
            'get_total_profit_us': self.get_total_profit_us,
            'get_total_profit_per': self.get_total_profit_per
            
        })
    
    def get_start_date(self, data):
        dt = datetime.datetime.strptime(data['form']['start_date'], '%Y-%m-%d')
        return dt.strftime('%d-%b-%Y')
    
    def get_end_date(self, data):
        dt = datetime.datetime.strptime(data['form']['end_date'], '%Y-%m-%d')
        return dt.strftime('%d-%b-%Y')
    
    
    def set_context(self, objects, data, ids, report_type=None):
        from datetime import datetime
        date_from = data['form']['start_date']
        date_to = data['form']['end_date']
        formatter_string = "%Y-%m-%d" 
        datetime_object = datetime.strptime(date_from, formatter_string)
        date_object = datetime_object.date()
        datetime_object_to = datetime.strptime(date_to, formatter_string)
        date_object_to = datetime_object_to.date()
        self.date_from = date_object.strftime("%d-%b-%Y")
        self.date_to = date_object_to.strftime("%d-%b-%Y")
        return super(custom_inv_report, self).set_context(objects, data, ids, report_type=report_type)

    def get_date_form(self):
        return self.date_from

    def get_date_to(self):
        return self.date_to

    def get_total_sum(self, form):
        return self.total_sum
        
    def get_subtotal_qty(self, li):
        #print "\nBEfore SubTOTAL TOTAL", li, type(li)
        return li
        
    def get_total_qty(self):
        return int(self.total_qty)
        
    def get_total_amount(self):
        return self.total_amount
    
    def get_total_amount_us(self):
        return self.total_amount_us
    
    def get_total_profit_us(self):
        return self.total_profit_us
    
    def get_total_profit_per(self):
        return self.total_profit_per
    

    def get_order_lines(self, obj):
        from datetime import datetime
        print '____________get_lines______________________'
        sale_obj = self.pool.get('sale.order')
        order_line = self.pool.get('sale.order.line')
        partner_obj = self.pool.get('res.partner')
        currency_obj = self.pool.get('res.currency')
        cur_obj = self.pool.get('res.currency.rate')
        fromdate = self.date_from
        todate = self.date_to
        self.total_qty = 0
        self.total_amount = 0.0
        self.sub_total_qty = 0
        self.qty_total = 0
        
        move_lines = []
        res = []
        final_res = []
        result = []
        
        query = ("SELECT * from sale_order as sl "\
                        "WHERE sl.date_order >= '"+ fromdate + "'" \
                        " AND sl.date_order <= '" + todate + "'" \
                        "AND sl.state='manual'"\
                        " ORDER BY sl.date_order"
                        
                        )
        self.cr.execute(query)
        move_lines = [x[0] for x in self.cr.fetchall()]
        
        
        
        for order in sale_obj.browse(self.cr, self.uid, move_lines):
            self.sub_total_qty = 0
            from_datelist = []
            to_datelist= []
            self.total_amount = self.total_amount + order.amount_total
            
            
            self.cr.execute(" select * from res_currency where name = 'USD' ")
            browse_curency = self.cr.fetchone()
            
            for to_curr_obj in currency_obj.browse(self.cr, self.uid, [browse_curency[0]]):
                for to_rate_obj in to_curr_obj.rate_ids:
                    to_datelist.append(to_rate_obj.name)
            to_get_datetime = lambda s: datetime.strptime(s, "%Y-%m-%d")
            to_base = to_get_datetime(order.date_order)
            to_later = filter(lambda d: to_get_datetime(d) <= to_base, to_datelist)
            to_closest_date = max(to_later, key = lambda d: to_get_datetime(d))
            
            to_rate_search = cur_obj.search(self.cr, self.uid, [('name', '=', to_closest_date), ('currency_id', '=', browse_curency[0])])[0]
            to_rate_browse = cur_obj.browse(self.cr, self.uid, to_rate_search)
            to_rate = to_rate_browse.rate
            
            for from_curr_obj in currency_obj.browse(self.cr, self.uid, [order.pricelist_id.currency_id.id]):
                for from_rate_obj in from_curr_obj.rate_ids:
                    from_datelist.append(from_rate_obj.name)
            from_get_datetime = lambda s: datetime.strptime(s, "%Y-%m-%d")
            from_base = from_get_datetime(order.date_order)
            from_later = filter(lambda d: from_get_datetime(d) <= from_base, from_datelist)
            from_closest_date = max(from_later, key = lambda d: from_get_datetime(d))
            
            from_rate_search = cur_obj.search(self.cr, self.uid, [('name', '=', from_closest_date), ('currency_id', '=', order.pricelist_id.currency_id.id)])[0]
            from_rate_browse = cur_obj.browse(self.cr, self.uid, from_rate_search)
            from_rate = from_rate_browse.rate
            
            rate = round((to_rate / from_rate), 2)
            
            
            for line in order.order_line:
                self.sub_total_qty = self.sub_total_qty + line.product_uom_qty
                print "\nProduct ID===", line.product_id.id
                res.append({
                    'partner': order.partner_id.name,
                    'ref':order.partner_id.ref,
                    'family_code': line.product_id.default_code,
                    'qty': int(line.product_uom_qty),
                    'amount': line.price_subtotal,
                    'currency': order.pricelist_id.currency_id.name,
                    'total_amount': order.amount_total,
                    'qty_total': int(self.sub_total_qty),
                    'amount_us': (line.price_subtotal * rate),
                    'profit_us': (line.cost * rate) - (line.price_unit * rate),
                    'profit_per': ((line.cost * rate) - (line.price_unit * rate) * 100 ) / (line.price_subtotal * rate) 
                    
                })
                self.total_qty = self.total_qty + line.product_uom_qty
        
        newlist = sorted(res, key=lambda k: k['ref'])

        groups = itertools.groupby(newlist, key=operator.itemgetter('ref'))
                    
        result = [{'ref':k, 'values':[x for x in v]} for k,v in groups]
        
        
        self.total_sum_qty = 0
        self.total_sum_amount = 0
        self.total_amount_us = 0.0
        self.total_profit_us = 0.0
        self.total_profit_per = 0.0
        
        for vals in result:
           self.qty_main_total = 0
           self.main_total = 0
           
           self.amount_us = 0.0
           self.profit_us = 0.0
           self.profit_per = 0.0
           
           
           for loop in vals['values']:
               self.qty_main_total += loop['qty']
               self.main_total += loop['amount']
               self.amount_us += loop['amount_us']
               self.profit_us += loop['profit_us']
               self.profit_per += loop['profit_per']
           
           vals['total'] = self.qty_main_total
           vals['sum_total'] = self.main_total
           vals['total_amount_us'] = self.amount_us
           vals['total_profit_us'] = self.profit_us
           vals['total_profit_per'] = self.profit_per
           
           
           
           self.total_sum_qty += vals['total']
           self.total_sum_amount += vals['sum_total']
           self.total_amount_us += vals['total_amount_us']
           self.total_profit_us += vals['total_profit_us']
           self.total_profit_per += vals['total_profit_per']
        return result
    
    
report_sxw.report_sxw(
    'report.custom.inv.report',
    'sale.order',
    'addons/customer_invoice_report/report/custom_invoice_report.rml',
    parser=custom_inv_report,
    header="internal landscape"
)


