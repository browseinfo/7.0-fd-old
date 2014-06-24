# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-Today BrowseInfo (<http://www.browseinfo.in>).
#
##############################################################################

import time
import datetime
from openerp.report import report_sxw

class sales_day_book_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        self.ans = 0
        self.res = 0
        self.repeat_dpp = 0
        self.sub_pricetotal = 0
        self.grand_pricetotal = 0
        self.dpp_total = 0
        self.currency_list = []
        self.currency_dict = {}
        self.rate = {}
        self.customer = {}
        self.currency_total = {}
        self.customer_currency = {}
        self.different_currency = 0
        self.current_obj = '';
        super(sales_day_book_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_invoice_ids':self.get_invoice_ids,
            'get_formate_date':self.get_formate_date,
            'get_month':self.get_month,
            'get_total':self.get_total,
            'get_dpp_total':self.get_dpp_total,
            'get_customer_name':self.get_customer_name,
            'get_keys':self.get_keys,
            'set_exchange_rate':self.set_exchange_rate,
            'get_exchange_rate':self.get_exchange_rate,
            'set_keys_total':self.set_keys_total,
            'get_keys_total':self.get_keys_total,
            'set_dpp':self.set_dpp,
            'get_dpp':self.get_dpp,
            'set_currency_data':self.set_currency_data,
            'get_currency_data':self.get_currency_data,
            'get_currency_total':self.get_currency_total,
            'get_currency':self.get_currency,
            'get_string':self.get_string,
            'check_currency_total':self.check_currency_total,
            
        })
    
    def get_invoice_ids(self,data):
        start_date = data['start_date']
        end_date = data['end_date']
        self.cr.execute("select id from account_invoice ai "\
                   "WHERE (ai.date_invoice >= %s) AND (ai.date_invoice <= %s)", (start_date, end_date))
        invoice_line_ids = self.cr.fetchall()
        account_invoice_ids_list=[i[0] for i in invoice_line_ids]
        account_invoice_obj = self.pool.get('account.invoice')
        account_invoice_ids = account_invoice_obj.search(self.cr, self.uid, ['&',('type','=','out_invoice'),('state', '!=', 'draft')])
        final_list = []
        for val in account_invoice_ids:
            if val in account_invoice_ids_list:
                final_list.append(val)
        obj_list =[]
        for ids in final_list:
            obj_list.append(account_invoice_obj.browse(self.cr, self.uid, ids ))
        return obj_list 
    
    def get_customer_name(self,data):
        start_date = data['start_date']
        end_date = data['end_date']
        self.cr.execute("select id from account_invoice ai "\
                   "WHERE (ai.date_invoice >= %s) AND (ai.date_invoice <= %s)", (start_date, end_date))
        invoice_line_ids = self.cr.fetchall()
        account_invoice_ids_list=[i[0] for i in invoice_line_ids]
        account_invoice_obj = self.pool.get('account.invoice')
        account_invoice_ids = account_invoice_obj.search(self.cr, self.uid, ['&',('type','=','out_invoice'),('state', '!=', 'draft')])
        final_list = []
        for val in account_invoice_ids:
            if val in account_invoice_ids_list:
                final_list.append(val)
        obj_list =[]
        for ids in final_list:
            for obj in account_invoice_obj.browse(self.cr, self.uid, [ids] ):
                obj.partner_id.name
                for line in obj.invoice_line:
                    self.currency_dict[obj.partner_id.name] = obj.currency_id.name
                    if obj.partner_id.name in self.customer.keys():
                        temp = self.customer[obj.partner_id.name]
                        self.customer[obj.partner_id.name] = temp + line.price_subtotal
                    else:
                        self.customer[obj.partner_id.name] = line.price_subtotal
        return self.customer
    
    def set_exchange_rate(self,obj):
        self.rate[obj.partner_id.name] = obj.exchange_rate
        self.customer_currency[obj.partner_id.name] = obj.currency_id.name
        self.current_obj = obj;
        
    def get_currency(self,key):
        return self.customer_currency[str(key)]
    
    def get_exchange_rate(self,key):
        return self.rate[str(key)]
    
    def get_keys(self,k):
        self.sub_pricetotal  = self.customer[str(k)]
        return self.sub_pricetotal
        
    def set_keys_total(self,k):
        self.grand_pricetotal += k
        
    def get_keys_total(self):
        return self.grand_pricetotal
    
    def set_dpp(self,dpp):
        self.dpp_total += dpp
        
    def get_dpp(self):
        return self.dpp_total
    
    def set_currency_data(self,currency,total):
        if currency in self.currency_total.keys():
            cur_total = self.currency_total[currency]
            self.currency_total[currency] = cur_total + total
        else:
            self.currency_total[currency] = total
    
    def get_currency_data(self):
        return self.currency_total
    
    def get_currency_total(self,key):
        return self.currency_total[str(key)]

    def check_currency_total(self,currency,customer_name):
        customer_currency = self.currency_dict[str(customer_name)]
        if customer_currency == currency:
            return self.customer[customer_name]
        else:
            return ''
    
    def get_total(self,data):
        start_date = data['start_date']
        end_date = data['end_date']
        self.cr.execute("select id from account_invoice ai "\
                   "WHERE (ai.date_invoice >= %s) AND (ai.date_invoice <= %s)", (start_date, end_date))
        invoice_line_ids = self.cr.fetchall()
        account_invoice_ids_list=[i[0] for i in invoice_line_ids]
        account_invoice_obj = self.pool.get('account.invoice')        
        account_invoice_ids = account_invoice_obj.search(self.cr, self.uid, ['&',('type','=','out_invoice'),('state', '!=', 'draft')])
        final_list = []
        for val in account_invoice_ids:
            if val in account_invoice_ids_list:
                final_list.append(val)
        obj_list =[]
        for ids in final_list:
            for obj in account_invoice_obj.browse(self.cr, self.uid, [ids] ):
                for line in obj.invoice_line:
                    self.ans = self.ans + line.price_subtotal
        return self.ans
    def get_string(self):
        if self.repeat_dpp != 0:
            return ''
        else:
            return 'TOTAL'
    def get_dpp_total(self,data):
        if self.repeat_dpp != 0:
            return ''
        start_date = data['start_date']
        end_date = data['end_date']
        self.cr.execute("select id from account_invoice ai "\
                   "WHERE (ai.date_invoice >= %s) AND (ai.date_invoice <= %s)", (start_date, end_date))
        invoice_line_ids = self.cr.fetchall()
        account_invoice_ids_list=[i[0] for i in invoice_line_ids]
        account_invoice_obj = self.pool.get('account.invoice')        
        account_invoice_ids = account_invoice_obj.search(self.cr, self.uid, ['&',('type','=','out_invoice'),('state', '!=', 'draft')])
        final_list = []
        for val in account_invoice_ids:
            if val in account_invoice_ids_list:
                final_list.append(val)
        obj_list =[]
        for ids in final_list:
            for obj in account_invoice_obj.browse(self.cr, self.uid, [ids] ):
                rate = obj.exchange_rate
                for line in obj.invoice_line:
                    self.res = self.res + (rate * line.price_subtotal)
        self.repeat_dpp += 1
        return self.res
    
    def get_formate_date(self, date_invoice):
        d = datetime.datetime.strptime(date_invoice, '%Y-%m-%d')
        date = d.strftime('%d-%b')
        return date
    
    def get_month(self,start_date):
        d = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        date = d.strftime('%b %Y')
        return date
    
report_sxw.report_sxw('report.sales.day.book', 'sales.day.book.wizard', 'sale_day_book_report_extended/report/sales_daybook_report.mako', parser=sales_day_book_report, header="internal landscape")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

