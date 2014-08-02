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

from datetime import datetime
import time
from openerp.report import report_sxw

class account_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(account_report, self).__init__(cr, uid, name, context=context)
        self.count = 0
        self.localcontext.update({
            'time': time,
            'get_amount': self._get_amount,
            'get_tanngal_date': self._get_tanngal_date,
            'get_seq': self._get_seq,
        })
        
    def _get_amount(self, amount):
        return ((amount * 10) / 100)
        
    def _get_tanngal_date(self, date):
        date = datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')
        if date:
            return date
        
    def _get_seq(self):
        self.count += 1
        return self.count
            
report_sxw.report_sxw(
    'report.account.invoice.pajak',
    'account.invoice',
    'addons/account_invoice_pajak_report/report/account_invoice_pajak.rml',
    header=False,
    parser=account_report
)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
