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
        self.count = 0
        self.localcontext.update({  
            'qty_total': self._qty_total,
            'get_order_date': self._get_order_date,
            'get_delivery_date': self._get_delivery_date,
            'get_seq': self._get_seq,
        })
        
    def _qty_total(self, obj):
        total = 0.0
        for line in obj.order_line:
            if line.product_qty:
                total += line.product_qty 
        return total
                
    def _get_order_date(self, date):
        ds = (datetime.strptime(date, '%Y-%m-%d')).strftime('%d-%b-%Y')
        return ds
    
    def _get_delivery_date(self, date):
        ds = (datetime.strptime(date, '%Y-%m-%d')).strftime('%d-%b-%Y')
        return ds
        
    def _get_seq(self):
        self.count += 1
        return self.count
        


report_sxw.report_sxw('report.purhcase.order.report', 'purchase.order', 'addons/purchase_extended_report/report/purchase_order_report.rml', parser=purchase_report, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
