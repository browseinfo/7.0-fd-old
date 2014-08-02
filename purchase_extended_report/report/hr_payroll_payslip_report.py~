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
from report import report_sxw


class payroll_payslip_all_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(payroll_payslip_all_report, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'get_payslip_lines': self._get_payslip_lines,
            'get_payslip_column': self._get_payslip_column,
            'get_grade': self._get_grade,
        })

    def _get_grade(self, form):
        return form.get('grade_id')[0] 
   
    def _get_payslip_column(self, obj):
        return self._get_payslip_lines(obj, 1)
    def _get_payslip_lines(self, obj, column_flag=0):
        payslip_line = self.pool.get('hr.payslip')
        step = self.pool.get('step')
        payslip_lines = []
        res = []
        result = []
        self.grade = obj.get('grade_id') 
        self.cr.execute("select hps.id, gs.step_id from hr_payslip_line hp "\
                        "LEFT JOIN hr_payslip hps on (hp.slip_id = hps.id) "\
                        "LEFT JOIN hr_employee he on (hp.employee_id = he.id) "\
                        "LEFT JOIN grade_step AS gs on (he.rank_id = gs.id) "\
                        "LEFT JOIN grade AS gr on (gs.grade_id = gr.id) "\
                        "where gr.id = %s", (self.grade[0],))
        payslip_lines_id = self.cr.fetchall()
        payslip_lines = [x[0] for x in payslip_lines_id]
        payslip  = list(set(payslip_lines))
        
        step_line = [x[1] for x in self.cr.fetchall()]
        computation_lines = {}
        for line in payslip_line.browse(self.cr, self.uid, payslip):
            computation_lines = {}
            for l in line.line_ids:
                computation_lines[l.name]= l.total
            res.append({
                            'computation': computation_lines,
                            'step_id': l.employee_id.rank_id.step_id.name,
                            })

        for i in res:
            result.append({
            'step_id': i['step_id'], 
            'annual': i['computation']['Basic']*12,
            'basic': i['computation']['Basic'],
            'domestic_staff': i['computation']['Domestic Staff'],
            'furniture': i['computation']['Furniture'],
            'housing': i['computation']['Housing'],
            'leave_grant': i['computation']['Leave Grant'],
            'meal': i['computation']['Meal'],
            'transport':i['computation']['Transport'],  
            'utilities': i['computation']['Utilities'] })
        return result


report_sxw.report_sxw('report.payroll.payslip.all', 'hr.payslip', 'addons/hr_payroll_payslip_report/report/register.rml', parser=payroll_payslip_all_report, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
