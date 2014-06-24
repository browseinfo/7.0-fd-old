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
class purchase_day_book_wizard(osv.osv_memory):
    _name = "purchase.day.book.wizard"
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
             'model': 'purchase.day.book.wizard',
             'form': data
        }
        print "\n\ndatas",datas
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'purchase.day.book',
            'datas': datas,
            }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
