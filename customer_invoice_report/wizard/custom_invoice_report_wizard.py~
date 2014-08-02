# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014-Today BrowseInfo (<http://www.browseinfo.in>).
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

class custom_invoice_report_wizard(osv.osv_memory):
    _name = "custom.invoice.report.wizard"
    _columns={
              
        'start_date': fields.date('Start Date', required=True),
        'end_date': fields.date('End Date', required=True),
        'branch_id':fields.many2one('res.branch',"Branch",required=True),
        
    }
    def print_report(self,cr, uid, ids, context=None):
        if context is None:
           context = {}
        data = self.read(cr, uid, ids)[0]
        datas = {
            'ids': [data.get('id')],
            'model': 'sale.order',
            'form': data
            }
        self_browse = self.browse(cr, uid, ids)
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'custom.inv.report',
            'datas': datas,
            'name': 'Customer Sale Report ' + '(' + self_browse[0].branch_id.branch_code + ')'
            }
        
        
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
