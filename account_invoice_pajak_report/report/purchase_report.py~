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


class purchase_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(purchase_report, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'get_order_lines': self._get_lines,
            'get_total_sum': self.get_total_sum,
            'get_date_form': self.get_date_form,
            'get_date_to': self.get_date_to,
            'get_total_qty': self.get_total_qty,
            'get_total_amount': self.get_total_amount,
            'get_subtotal_qty': self.get_subtotal_qty,
            
        })

    def set_context(self, objects, data, ids, report_type=None):
        print "\n\n\n===", objects, data, ids, objects.start_date, data['form']['start_date']
        date_from = data['form']['start_date']
        date_to = data['form']['end_date']
        formatter_string = "%Y-%m-%d" 
        datetime_object = datetime.strptime(date_from, formatter_string)
        date_object = datetime_object.date()
        datetime_object_to = datetime.strptime(date_to, formatter_string)
        date_object_to = datetime_object_to.date()
        self.date_from = date_object.strftime("%d-%b-%Y")
        self.date_to = date_object_to.strftime("%d-%b-%Y")
        return super(purchase_report, self).set_context(objects, data, ids, report_type=report_type)

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

    def _get_lines(self, obj):
        purchase_obj = self.pool.get('purchase.order')
        order_line = self.pool.get('purchase.order.line')
        partner_obj = self.pool.get('res.partner')
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
        
        query = ("SELECT * from purchase_order as pl "\
                        "WHERE pl.date_order >= '"+ fromdate + "'" \
                        " AND pl.date_order <= '" + todate + "'" 
                        " ORDER BY pl.date_order"
                        )
        self.cr.execute(query)
        move_lines = [x[0] for x in self.cr.fetchall()]
        
        
        for order in purchase_obj.browse(self.cr, self.uid, move_lines):
            self.sub_total_qty = 0
            self.total_amount = self.total_amount + order.amount_total
            for line in order.order_line:
                self.sub_total_qty = self.sub_total_qty + line.product_qty
                print "\nProduct ID===", line.product_id.id
                res.append({
                    'partner': order.partner_id.name,
                    'ref':order.partner_id.ref,
                    'currency': order.pricelist_id.currency_id.name,
                    'total_amount': order.amount_total,
                    'code': line.product_id.default_code,
                    'qty': int(line.product_qty),
                    'amount': line.price_subtotal,
                    'qty_total': int(self.sub_total_qty),
                })
                self.total_qty = self.total_qty + line.product_qty
        
        newlist = sorted(res, key=lambda k: k['ref'])

        groups = itertools.groupby(newlist, key=operator.itemgetter('ref'))
                    
        result = [{'ref':k, 'values':[x for x in v]} for k,v in groups]
        
        self.total_sum_qty = 0
        self.total_sum_amount = 0
        for vals in result:
           self.qty_main_total = 0
           self.main_total = 0
           for loop in vals['values']:
               self.qty_main_total += loop['qty']
               self.main_total += loop['amount']
           vals['total'] = self.qty_main_total
           vals['sum_total'] = self.main_total
           self.total_sum_qty += vals['total']
           self.total_sum_amount += vals['sum_total']
           
        print "\n\nVALSSS", result

        return result


report_sxw.report_sxw('report.purchase.date.webkit.report', 'purchase.order', 'addons/purchase_extended_webkit_report/report/purchase_report.mako', parser=purchase_report, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
