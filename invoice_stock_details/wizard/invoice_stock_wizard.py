# -*- coding: utf-8 -*-
##############################################################################
#
#    Sales and Account Invoice Discount Management
#    Copyright (C) 2013-2014 BrowseInfo(<http://www.browseinfo.in>).
#    $autor:
#   
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import datetime
import time

from openerp.report import report_sxw

class invoice_stock_details_wizard(osv.osv_memory):
    _name = "invoice.stock.details.wizard"
    _columns={
        'start_date': fields.date('Start Period', required=True),
        'end_date': fields.date('End Period', required=True),
        'branch_id':fields.many2one('res.branch','Branch',required=True),
        'company_id':fields.many2one('res.company','Company'),
        'printed_by':fields.char('Printed By'),
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
        datas = {
             'ids': [data.get('id')],
             'model': 'account.invoice',
             'form': data
        }
        self_browse = self.browse(cr, uid, ids)
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'invoice.stock.details',
            'datas': datas,
            'name': 'LAPORAN POSISI BARANG ' + '(' + self_browse[0].branch_id.branch_code + ')'
        }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
