#!/usr/bin/env python
#-*- coding:utf-8 -*-

##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    d$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

import time
import operator
import itertools
from datetime import datetime
from dateutil import relativedelta
from tools.translate import _
from report import report_sxw
import netsvc
from osv import fields, osv

class account_month_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(account_month_report, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'call_date_from': self._call_date_from,
            'call_date_to': self._call_date_to,
        })
        
    def _call_date_from(self, obj):
        date = datetime.strptime(self.date_from, '%Y-%m-%d')
        return (str(date.day) + '/' + str(date.month) + '/' + str(date.year))
        
    def _call_date_to(self, obj):
        date = datetime.strptime(self.date_to, '%Y-%m-%d')
        return (str(date.day) + '/' + str(date.month) + '/' + str(date.year))
        
    def set_context(self, objects, data, ids, report_type=None):
        '''period_obj = self.pool.get('account.period')
        period_id = period_obj.search(self.cr,self.uid, [('name', '=', data['form']['start_date'][1] )])
        for period in period_obj.browse(self.cr, self.uid, period_id):
            self.date_from = period.date_start
            self.date_to = period.date_stop'''
        
        return super(account_month_report, self).set_context(objects, data, ids, report_type=report_type)

report_sxw.report_sxw('report.account.invoice.month.report', 'account.invoice', 'addons/bank_report/report/bank_payroll_consolidate_report.mako', parser=account_month_report, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
