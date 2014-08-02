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

from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import datetime
import time

from openerp.report import report_sxw

class account_monthly_report_wizard(osv.osv_memory):
    _name = "account.monthly.report.wizard"
    _columns={
        'start_date': fields.date('Start Period', required=True),
        'end_date': fields.date('End Period', required=True),
        'branch_id':fields.many2one('res.branch','Branch',required=True),
        'company_id':fields.many2one('res.company','Company')
    }
    
    def print_report(self,cr, uid, ids, context=None):
        """
         To get the date and print the report
         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param context: A standard dictionary
         @return: return report
        """
        if context is None:
            context = {}
        data = self.read(cr, uid, ids, [], context=context)[0]
        print "\n\ndata", data
        datas = {
             'ids': [data.get('id')],
             'model': 'account.invoice',
             'form': data
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'account.invoice.month.report',
            'datas': datas,
        }
        
class account_report_wizard(osv.osv_memory):
    _name = "account.report.wizard"
    _columns={
        'start_date': fields.date('Start Period', required=True),
        'end_date': fields.date('End Period', required=True),
        'branch_id':fields.many2one('res.branch','Branch',required=True),
        'authorised_by':fields.char('Authorised By')
    }
    def print_report(self,cr, uid, ids, context=None):
        if context is None:
           context = {}
        data = self.read(cr, uid, ids)[0]
        datas = {
            'ids': context.get('active_ids',[]),
            'model': 'account.report.wizard',
            'form': data
            }
        self_browse = self.browse(cr, uid, ids)
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'account.supplier.invoice.report',
            'datas': datas,
            'name': 'CONTOH IMPOR REPORT' + '(' + self_browse[0].branch_id.branch_code + ')'
            }
class account_ekspor_report_wizard(osv.osv_memory):
    _name = "account.ekspor.report.wizard"
    _columns={
        'start_date': fields.date('Start Date', required=True),
        'end_date': fields.date('End Date', required=True),
        'year':fields.many2one('account.fiscalyear','Fiscal Year'),
        'quater':fields.selection([('1','1'), ('2','2'),('3','3'),('4','4')],'Quater'),
        'branch_id':fields.many2one('res.branch','Branch',required=True),
        'authorised_by':fields.char('Authorised By')
    }
    def print_report(self,cr, uid, ids, context=None):
        if context is None:
           context = {}
        data = self.read(cr, uid, ids)[0]
        datas = {
            'ids': context.get('active_ids',[]),
            'model': 'account.ekspor.report.wizard',
            'form': data
            }
        self_browse = self.browse(cr, uid, ids)
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'account.customer.invoice.report',
            'datas': datas,
            'name': 'CONTOH EKSPOR REPORT' + '(' + self_browse[0].branch_id.branch_code + ')'
            }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
