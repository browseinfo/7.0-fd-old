# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-Today BrowseInfo (<http://www.browseinfo.in>).
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import datetime
import time
from openerp.report import report_sxw

class sales_day_book_wizard(osv.osv_memory):
    _name = "sales.day.book.wizard"
    _columns={
        'start_date': fields.date('Start Period', required=True),
        'end_date': fields.date('End Period', required=True),
    }
    
    def print_report(self,cr, uid, ids, context=None):
        if context is None:
           context = {}
        data = self.read(cr, uid, ids)[0]
        datas = {
            'ids': context.get('active_ids',[]),
            'model': 'sales.day.book.wizard',
            'form': data
            }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'sales.day.book',
            'datas': datas,
            }
sales_day_book_wizard()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
