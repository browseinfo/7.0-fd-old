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

import time
import operator
import itertools
from datetime import datetime
from dateutil import relativedelta
from report import report_sxw
from openerp.tools.amount_to_text_en import amount_to_text


class account_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(account_report, self).__init__(cr, uid, name, context)
        self.localcontext.update({  
            'get_total': self._get_total,
            'get_dk': self._get_dk,
            'get_date': self._get_date,
            'get_sign': self._get_sign,
            'get_sign1': self._get_sign1,
            'amount_word': self._amount_word,
        })
        
    def _get_total(self, obj):
        total = 0.0
        for line in obj.line_ids:
            if line.amount:
                total += line.amount 
        return total
        
    def _get_sign(self, obj):
        if obj.journal_id.name == 'Cash':
            return '×'
        
    def _get_sign1(self, obj):
        if obj.journal_id.name == 'Bank':
            return '×'            
        
                
    def _get_dk(self, line):
        if line.type == 'cr':
            return 'K'
        elif line.type == 'dr':
            return 'D'
        else:
            return ''
    
    def _get_date(self, date):
        ds = (datetime.strptime(date, '%Y-%m-%d')).strftime('%d-%b-%y')
        return ds
        
    def _amount_word(self, obj):
        total = self._get_total(obj)
        if total == 0.0:
            return ' '
        else:
            amount = amount_to_text(total)
            word = str(amount) + ' Only'
            return word
        


report_sxw.report_sxw('report.account.voucher.extend.report', 'account.voucher', 'addons/account_voucher_extended_report/report/account_voucher_report.rml', parser=account_report, header=False)




# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
