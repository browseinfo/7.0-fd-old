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
from openerp.report import report_sxw
from openerp.osv import fields, osv, orm

class sale_quotation_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(sale_quotation_report, self).__init__(cr, uid, name, context=context)
        self.index = 0
        self.localcontext.update({
            'time': time,
            'get_index':self.get_index,
            'get_qty':self.get_qty,
        })
    
    def get_index(self):
        self.index += 1
        return self.index
    
    def get_qty(self,qty):
        qty = int(qty)
        return qty
    
report_sxw.report_sxw(
    'report.sale.quotation.report',
    'sale.order',
    'sale_quotation_report/report/sale_quotation_report.rml',
    parser=sale_quotation_report,
    header="False"
)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

