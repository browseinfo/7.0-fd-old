# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://browseinfo.in>).
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
 #           'new_partner': self.new_partner,
        })


    def date_format(self, datedetail):
        if datedetail:
            a = time.strptime(datedetail,'%Y-%m-%d')
            b = time.strftime('%d-%B-%Y', a)
            return b
        else:
            return ''
        
report_sxw.report_sxw('report.sale.report', 'sale.order', 'sale_report_fd/sale_report.rml', parser=sale_report, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

