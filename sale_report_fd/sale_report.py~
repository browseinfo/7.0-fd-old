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


class sale_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(sale_report, self).__init__(cr, uid, name, context)
        self.localcontext.update({  
#            'get_amount_data': self._get_amount_data,
#            'get_from_date': self.get_from_date,
#            'get_end_date': self.get_end_date,
#            'get_partner': self.get_partner,
#            'get_total_qty': self.get_total_qty,
            #'get_total_qty_cust': self.get_total_qty_cust,
#            'get_subtotal_qty': self.get_subtotal_qty,
#            'get_total_amount': self.get_total_amount,
 #           'get_page_break':self.get_page_break,
            'date_format': self.date_format,
            'get_branch_code':self.get_branch_code,
 #           'new_partner': self.new_partner,
        })

    def get_branch_code(self,branch_id):
        branch_code = self.pool.get('res.branch').browse(self.cr,self.uid,branch_id.id).branch_code
        return branch_code
    
    def date_format(self, datedetail):
        if datedetail:
            a = time.strptime(datedetail,'%Y-%m-%d')
            b = time.strftime('%d-%B-%Y', a)
            return b
        else:
            return ''
        
report_sxw.report_sxw('report.sale.report', 'sale.order', 'sale_report_fd/sale_report.rml', parser=sale_report, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

