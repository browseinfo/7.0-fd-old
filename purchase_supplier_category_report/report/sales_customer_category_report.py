#!/usr/bin/env python
#-*- coding:utf-8 -*-

##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    d$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#defined    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
import operator
import itertools
from datetime import datetime
from dateutil import relativedelta
from tools.translate import _
from report import report_sxw
import netsvc
from osv import fields, osv
class sales_customer_category_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(sales_customer_category_report, self).__init__(cr, uid, name, context)
        self.total = 0.0
        self.index = 1
        self.localcontext.update({
            'get_payslip_lines': self._get_payslip_lines,
            'get_categ': self._get_categ,
            'decide_categ': self._decide_categ,
            'total_dict':self._total_dict,
            'get_grand_total_categ':self._get_grand_total_categ,
            'get_grand_total':self._get_grand_total,
            'set_grand_total':self._set_grand_total,
            'get_index':self._get_index,
            
        })
    def _get_index(self):
        return self.index    
    
    def _set_grand_total(self, total):
        self.total += total
        self.index +=1

    def _get_grand_total(self):
        return self.total

    def _get_grand_total_categ(self, categ):
        value = self.grand_total[categ]
        return value

    def _total_dict(self):
        self.grand_total = dict.fromkeys([cat.name for cat in self.categ], 0)

    def _decide_categ(self, categ):
        cat_dict = self.new_list[0]
        ans = 0.00
        for k,v in cat_dict.items():
            for key,value in v.items():
                if categ == key:
                    ans = value
                else:
                    ans = ''
        return ans
    def _get_categ(self):
        cat_pool = self.pool.get('product.category')
        cat_list = []
        for categ_id in cat_pool.search(self.cr, self.uid, []):
            cat_list.append(cat_pool.browse(self.cr, self.uid, categ_id))
        self.categ = cat_list
        return cat_list

    def set_context(self, objects, data, ids, report_type=None):
        period_obj = self.pool.get('account.period')
        period_id = period_obj.search(self.cr,self.uid, [('name', '=', data['form']['period_id'][1] )])
        for period in period_obj.browse(self.cr, self.uid, period_id):
            self.date_from = period.date_start
            self.date_to = period.date_stop
        return super(sales_customer_category_report, self).set_context(objects, data, ids, report_type=report_type)

 
    def _get_payslip_lines(self, obj, column_flag=0):
        purchase_obj = self.pool.get('sale.order')
        currency_obj = self.pool.get('res.currency')
        cur_obj = self.pool.get('res.currency.rate')
        self.total_amount = 0.0
        payslip_lines = []
        res = []
        result = []
        line_ids = []
        value = {}
        
        self.cr.execute("select so.partner_id from sale_order so "\
                    "WHERE (so.date_order >= %s) AND (so.date_order <= %s) group by  so.partner_id", (self.date_from, self.date_to,))
        purchase_line_ids = self.cr.fetchall()
        for a in  purchase_line_ids:
             line_ids.append(a[0])
        purchase_ids = purchase_obj.search(self.cr, self.uid, [('partner_id', 'in', line_ids)])
        partner_list = categ_list = []
        for line in purchase_obj.browse(self.cr, self.uid, purchase_ids):
            
            
            to_datelist= []
            from_datelist= []
            self.sub_total_qty = 0
            self.total_amount = self.total_amount + line.amount_total
            self.cr.execute(" select * from res_currency where name = 'USD' ")
            browse_curency = self.cr.fetchone()
            
            for to_curr_obj in currency_obj.browse(self.cr, self.uid, [browse_curency[0]]):
                for to_rate_obj in to_curr_obj.rate_ids:
                    to_datelist.append(to_rate_obj.name)
            to_get_datetime = lambda s: datetime.strptime(s, "%Y-%m-%d")
            to_base = to_get_datetime(line.date_order)
            to_later = filter(lambda d: to_get_datetime(d) <= to_base, to_datelist)
            to_closest_date = max(to_later, key = lambda d: to_get_datetime(d))
            
            to_rate_search = cur_obj.search(self.cr, self.uid, [('name', '=', to_closest_date), ('currency_id', '=', browse_curency[0])])[0]
            to_rate_browse = cur_obj.browse(self.cr, self.uid, to_rate_search)
            to_rate = to_rate_browse.rate
            
            for from_curr_obj in currency_obj.browse(self.cr, self.uid, [line.pricelist_id.currency_id.id]):
                for from_rate_obj in from_curr_obj.rate_ids:
                    from_datelist.append(from_rate_obj.name)
            from_get_datetime = lambda s: datetime.strptime(s, "%Y-%m-%d")
            from_base = from_get_datetime(line.date_order)
            from_later = filter(lambda d: from_get_datetime(d) <= from_base, from_datelist)
            from_closest_date = max(from_later, key = lambda d: from_get_datetime(d))
            
            from_rate_search = cur_obj.search(self.cr, self.uid, [('name', '=', from_closest_date), ('currency_id', '=', line.pricelist_id.currency_id.id)])[0]
            from_rate_browse = cur_obj.browse(self.cr, self.uid, from_rate_search)
            from_rate = from_rate_browse.rate
            
            rate = round((to_rate / from_rate), 2)
            
            
            
            
            
            
            
            computation_lines = {line.partner_id.name:{}}
            for l in line.order_line:
                    if l.product_id.categ_id.name in computation_lines[line.partner_id.name].keys():
                        total = computation_lines[line.partner_id.name][l.product_id.categ_id.name] +  l.price_subtotal  * rate
                        computation_lines[line.partner_id.name][l.product_id.categ_id.name] = total 
                    else:
                        computation_lines[line.partner_id.name][l.product_id.categ_id.name]= l.price_subtotal * rate
            res.append(computation_lines)
        output = {}
        for d in res:
            for k,v in d.items():
                output.setdefault(k, []).append(v)

        self.new_list = []
        for key, value in output.items():
            out = {}
            total = update = 0.00 
            for d in value:
                for k, v in d.items():
                    if k not in out:
                        out.setdefault(k, v)
                        total += v
                        update = self.grand_total[k] + v
                        self.grand_total.update({k : update})
                    else:
                        out[k] = out[k] + v
                        total += v
                        update = self.grand_total[k] + v
                        self.grand_total.update({k : update})
                out['total'] = total
            self.new_list.append({key: out})
        return self.new_list



report_sxw.report_sxw('report.sales.customer.category.report.all', 'sales.order', 'addons/purchase_supplier_category_report/report/sales_customer_category_report.mako', parser=sales_customer_category_report, header=False)

