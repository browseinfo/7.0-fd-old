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


class history_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(history_report, self).__init__(cr, uid, name, context)
        self.count = 0
        self.localcontext.update({  
            'date_format': self.date_format,
            'get_seq': self._get_seq,
        })


    def _get_seq(self):
        self.count += 1
        return self.count
        
        
    def date_format(self, datedetail):
        if datedetail:
            a = time.strptime(datedetail,'%Y-%m-%d')
            b = time.strftime('%d %B %Y', a)
            return b
        else:
            return ''
        
report_sxw.report_sxw('report.history.sale', 'sale.order', 'sale_price_history/report/history_tab.rml', parser=history_report, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

