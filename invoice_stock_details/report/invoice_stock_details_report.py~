# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 to now Browseinfo (<http:browseinfo.in>).
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

import time
from datetime import datetime
import itertools
import operator
from openerp.report import report_sxw

class invoice_stock_details(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(invoice_stock_details, self).__init__(cr, uid, name, context=context)
        self.index = 0
        self.product = {}
        self.product_invoice = []
        self.invoice_ids_list = []
        self.invoice_product_list = []
        self.invoice_qty_list = []
        self.invoice_product_code = []
        self.counter =1
        self.quantity = 0
        self.localcontext.update({
            'time': time,
            'get_formate_date':self.get_formate_date,
            'get_index':self.get_index,
            'get_product_id':self.get_product_id,
            'get_uom': self.get_uom,
            'get_quantity': self.get_quantity,
            'get_date': self.get_date,
        })

    def get_product_id(self,data):
        start_date = data['start_date']
        end_date = data['end_date']
        branch_id = data['branch_id'][0]
        product_list = []
        result = {}
        invoice_list = []
        
        account_pool = self.pool.get('account.invoice')
        self.cr.execute("select ai.id from account_invoice ai "\
                   "WHERE ((ai.type = 'out_invoice')) AND ((ai.date_invoice >= %s) AND (ai.date_invoice <= %s) AND (ai.branch_id = %s))  ORDER BY ai.shipment_date", (start_date, end_date, branch_id))
        customer_invoice_line_ids = self.cr.fetchall()
        customer_invoice_line_ids = [line[0] for line in customer_invoice_line_ids]
        
        product_obj = self.pool.get('product.product') 
        product_search_id = product_obj.search(self.cr,self.uid,[])
        
        for invoice in account_pool.browse(self.cr, self.uid, customer_invoice_line_ids):
            customer_shipment_date = invoice.shipment_date
            for invoice_line in invoice.invoice_line:
                flag = False
                if invoice_line.product_id:
                    product_id = product_obj.browse(self.cr, self.uid,[invoice_line.product_id.id])[0]
                    if invoice_line.product_id.qty_available > 0:
                        self.cr.execute("select ai.id from account_invoice ai "\
	                        "where ai.type = 'in_invoice' "\
	                        "and ai.shipment_date <= %s "\
	                        "and branch_id = %s ", (customer_shipment_date, branch_id))
                        supplier_invoice_line_ids = self.cr.fetchall()
                        supplier_invoice_line_ids = [line[0] for line in supplier_invoice_line_ids]
                        
                        for supplier_invoice_line in self.pool.get('account.invoice').browse(self.cr, self.uid, supplier_invoice_line_ids):
                            if supplier_invoice_line.invoice_line:
                                for supplier_line in supplier_invoice_line.invoice_line:
                                    if supplier_line.product_id.id == invoice_line.product_id.id:
                                        if not flag:
                                            invoice_list.append({
                                                'shipment_date': invoice.shipment_date or '',
                                                'default_code': invoice_line.product_id.default_code,
                                                'invoice_product_name': invoice_line.product_id.name,
                                                'invoice_product_uom': invoice_line.uos_id.name or '',
                                                'invoice_qty_available': invoice_line.quantity,
                                                'supplier_default_code': supplier_line.product_id.default_code,
                                                'supplier_invoice_product_name': supplier_line.product_id.name,
                                                'supplier_invoice_product_uom': supplier_line.uos_id.name or '',
                                                'supplier_invoice_qty_available': supplier_line.quantity,
                                            })
                                            flag = True
                                        if flag:
                                            break
                                if flag:
                                    break
                        else:
                            invoice_list.append({
                                'shipment_date': invoice.shipment_date or '',
                                'default_code': invoice_line.product_id.default_code,
                                'invoice_product_name': invoice_line.product_id.name,
                                'invoice_product_uom': invoice_line.uos_id.name or '',
                                'invoice_qty_available': invoice_line.quantity,
                                'supplier_default_code': '',
                                'supplier_invoice_product_name': '',
                                'supplier_invoice_product_uom': '',
                                'supplier_invoice_qty_available': '',
                            })
                        
        groups = itertools.groupby(invoice_list, key=operator.itemgetter('shipment_date'))
        result = [{'shipment_date':k,'values':[x for x in v]} for k, v in groups]

        return result
        
    def get_date(self, date):
        date = datetime.strptime(date, '%Y-%m-%d').strftime("%d-%b-%Y")
        return date

    def get_quantity(self):
        return self.quantity
    
    def get_uom(self, data):
        product_search_id = self.pool.get('product.product').search(self.cr,self.uid,[('name', '=', data)])
        for product in self.pool.get('product.product').browse(self.cr, self.uid, product_search_id):
            self.quantity = product.qty_available
            return product.uom_id.name
                                
        
    def get_formate_date(self, date_invoice):
        d = datetime.datetime.strptime(date_invoice, '%Y-%M-%d')
        date = d.strftime('%d %B %Y')
        return date
    def get_index(self):
        self.index += 1
        return self.index
report_sxw.report_sxw('report.invoice.stock.details', 'account.invoice', '7.0-fd/invoice_stock_details/report/invoice_stock_details.rml', parser=invoice_stock_details, header="internal landscape")


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
