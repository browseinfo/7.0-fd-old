from datetime import datetime, timedelta
import time
import openerp.exceptions
from openerp import netsvc
from openerp import pooler
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
from openerp.osv import fields, osv
from openerp.tools.translate import _

class sales_ledger_report_wizard(osv.osv_memory):
    _name = "sales.ledger.report.wizard"
    _description = "Sales Ledger wizard"
    

    
    _columns = {
       'start_date': fields.date('Issue Date', required=True),
       'end_date': fields.date('To', required=True),
       'branch': fields.many2one('res.branch','Branch',required=True),
    }


    def sales_ledger_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.read(cr, uid, ids)[0]
        
        datas = {
             'ids':[data.get('id')],
             'model': 'account.invoice',
             'form': data
                 }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'sale.ledger.report',
            'datas': datas,
            }

    def sales_amount_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.read(cr, uid, ids)[0]
        datas = {
             'ids':[data.get('id')],
             'model': 'sale.order',
             'form': data
                 }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'sale.amount.report',
            'datas': datas,
            }


sales_ledger_report_wizard()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
