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

class sale_day_book_wizard(osv.osv_memory):
    _name = "sale.day.book.wizard"
    _columns={
        'start_date': fields.date('Start Period', required=True),
        'end_date': fields.date('End Period', required=True),
    }

    def print_report(self,cr, uid, ids, context=None):
        if context is None:
           context = {}
        data = self.read(cr, uid, ids, [], context=context)[0]
        
        datas = {
             'ids': [data.get('id')],
             'model': 'sale.day.book.wizard',
             'form': data
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'sale.day.book',
            'datas': datas,
            }

sale_day_book_wizard()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
