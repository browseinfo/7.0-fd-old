# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-Today BrowseInfo (<http://www.browseinfo.in>).
#
##############################################################################

import time
from datetime import datetime
from openerp.report import report_sxw

class sales_day_book_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        self.ans = 0
        self.res = 0
        self.repeat_dpp = 0
        self.sub_pricetotal = 0
        self.grand_pricetotal = 0
        self.subtotal_currecy_ddpn = 0
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
            'get_product_code':self.get_product_code,
            'get_currency_subtotal': self.get_currency_subtotal,
            'get_currency_subtotal_dpp': self.get_currency_subtotal_dpp,
            'get_dpp_total_curr': self.get_dpp_total_curr,
            
        })
        
    def get_currency_subtotal_dpp(self, o):
        to_datelist= []
        from_datelist= []
        currency_obj = self.pool.get('res.currency')
        cur_obj = self.pool.get('res.currency.rate')
        
        self.cr.execute(" select * from res_currency where name = 'USD' ")
        browse_curency = self.cr.fetchone()
        
        for to_curr_obj in currency_obj.browse(self.cr, self.uid, [browse_curency[0]]):
			for to_rate_obj in to_curr_obj.rate_ids:
				to_datelist.append(to_rate_obj.name)
        to_get_datetime = lambda s: datetime.strptime(s, "%Y-%m-%d")
        to_base = to_get_datetime(o.date_invoice)
        to_later = filter(lambda d: to_get_datetime(d) <= to_base, to_datelist)
        to_closest_date = max(to_later, key = lambda d: to_get_datetime(d))
		
        to_rate_search = cur_obj.search(self.cr, self.uid, [('name', '=', to_closest_date), ('currency_id', '=', browse_curency[0])])[0]
        to_rate_browse = cur_obj.browse(self.cr, self.uid, to_rate_search)
        to_rate = to_rate_browse.rate
        
        for from_curr_obj in currency_obj.browse(self.cr, self.uid, [o.currency_id.id]):
			for from_rate_obj in from_curr_obj.rate_ids:
				from_datelist.append(from_rate_obj.name)
        from_get_datetime = lambda s: datetime.strptime(s, "%Y-%m-%d")
        from_base = from_get_datetime(o.date_invoice)
        from_later = filter(lambda d: from_get_datetime(d) <= from_base, from_datelist)
        from_closest_date = max(from_later, key = lambda d: from_get_datetime(d))
		
        from_rate_search = cur_obj.search(self.cr, self.uid, [('name', '=', from_closest_date), ('currency_id', '=', o.currency_id.id)])[0]
        from_rate_browse = cur_obj.browse(self.cr, self.uid, from_rate_search)
        from_rate = from_rate_browse.rate
        
        rate = round((to_rate / from_rate), 2)
        self.subtotal_currecy_ddpn += (rate * o.amount_untaxed * o.exchange_rate) 
        return (rate * o.amount_untaxed * o.exchange_rate)
    
    def get_dpp_total_curr(self):
        return self.subtotal_currecy_ddpn
    
    def get_currency_subtotal(self, o):
        to_datelist= []
        from_datelist= []
        currency_obj = self.pool.get('res.currency')
        cur_obj = self.pool.get('res.currency.rate')
        
        self.cr.execute(" select * from res_currency where name = 'USD' ")
        browse_curency = self.cr.fetchone()
        
        for to_curr_obj in currency_obj.browse(self.cr, self.uid, [browse_curency[0]]):
			for to_rate_obj in to_curr_obj.rate_ids:
				to_datelist.append(to_rate_obj.name)
        to_get_datetime = lambda s: datetime.strptime(s, "%Y-%m-%d")
        to_base = to_get_datetime(o.date_invoice)
        to_later = filter(lambda d: to_get_datetime(d) <= to_base, to_datelist)
        to_closest_date = max(to_later, key = lambda d: to_get_datetime(d))
		
        to_rate_search = cur_obj.search(self.cr, self.uid, [('name', '=', to_closest_date), ('currency_id', '=', browse_curency[0])])[0]
        to_rate_browse = cur_obj.browse(self.cr, self.uid, to_rate_search)
        to_rate = to_rate_browse.rate
        
        for from_curr_obj in currency_obj.browse(self.cr, self.uid, [o.currency_id.id]):
			for from_rate_obj in from_curr_obj.rate_ids:
				from_datelist.append(from_rate_obj.name)
        from_get_datetime = lambda s: datetime.strptime(s, "%Y-%m-%d")
        from_base = from_get_datetime(o.date_invoice)
        from_later = filter(lambda d: from_get_datetime(d) <= from_base, from_datelist)
        from_closest_date = max(from_later, key = lambda d: from_get_datetime(d))
		
        from_rate_search = cur_obj.search(self.cr, self.uid, [('name', '=', from_closest_date), ('currency_id', '=', o.currency_id.id)])[0]
        from_rate_browse = cur_obj.browse(self.cr, self.uid, from_rate_search)
        from_rate = from_rate_browse.rate
        
        rate = round((to_rate / from_rate), 2)
        return (rate * o.amount_untaxed)

    def get_product_code(self,invoice_line):
        product_code = []
        product_code_string = ''
        for line in invoice_line:
            product_code.append(line.product_id.default_code)
        return product_code
        
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
        d = datetime.strptime(date_invoice, '%Y-%m-%d')
        date = d.strftime('%d-%b')
        return date
    
    def get_month(self,start_date):
        d = datetime.strptime(start_date, '%Y-%m-%d')
        date = d.strftime('%b %Y')
        return date
    
report_sxw.report_sxw('report.sales.day.book', 'sales.day.book.wizard', 'sale_day_book_report_extended/report/sales_daybook_report.mako', parser=sales_day_book_report, header="internal landscape")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

