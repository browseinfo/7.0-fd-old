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

class sale_day_book_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(sale_day_book_report, self).__init__(cr, uid, name, context=context)
        self.total = 0
        self.grand_total = {}
        self.categ = []
        self.localcontext.update({
            'time': time,
            'get_categ': self._get_categ,
            'sale_details':self._sale_details,
            'categ_price':self._categ_price,
            'set_total': self._set_total,
            'get_total': self._get_total,
            'get_grand_total':self._get_grand_total,
            'total_dict':self._total_dict,
            'date_format':self._date_format,
            'get_product_code':self._get_product_code,
            'branch_code':self._branch_code,
            'get_currency_subtotal': self.get_currency_subtotal
        })
    def _date_format(self, date):
        if date is not False:
            d = datetime.strptime(date, '%Y-%m-%d')
            date = d.strftime('%d-%b-%Y')
            return date
        else:
            return ''

    def _total_dict(self):
        self.grand_total = dict.fromkeys([cat.id for cat in self.categ], 0) 
    
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
        self.total += (rate * o.amount_untaxed) 
        return (rate * o.amount_untaxed)

    def _get_categ(self):
        cat_pool = self.pool.get('product.category')
        cat_list = []
        for categ_id in cat_pool.search(self.cr, self.uid, []):
            cat_list.append(cat_pool.browse(self.cr, self.uid, categ_id))
        self.categ = cat_list
        return cat_list

    def _get_product_code(self,invoice_line):
        product_code = []
        product_code_string = ''
        for line in invoice_line:
            product_code.append(line.product_id.default_code)
        return product_code

    def _sale_details(self, obj):
        self.start_date = obj['start_date']
        self.end_date = obj['end_date']
        self.branch_id = obj['branch_id'][0]
        self.cr.execute("select ai.id from account_invoice ai "\
                    "WHERE (ai.date_invoice >= %s) AND (ai.date_invoice <= %s) AND ai.type='out_invoice' AND ai.state !='draft' AND ai.branch_id = %s ", (self.start_date, self.end_date,self.branch_id))

        objects = []
        for po_id in [po_id[0] for po_id in self.cr.fetchall()]:
            objects.append(self.pool.get('account.invoice').browse(self.cr, self.uid, po_id))
        return objects

    def _categ_price(self, invoice_line, cat):
        for line in invoice_line:
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
            to_base = to_get_datetime(line.invoice_id.date_invoice)
            to_later = filter(lambda d: to_get_datetime(d) <= to_base, to_datelist)
            to_closest_date = max(to_later, key = lambda d: to_get_datetime(d))
		
            to_rate_search = cur_obj.search(self.cr, self.uid, [('name', '=', to_closest_date), ('currency_id', '=', browse_curency[0])])[0]
            to_rate_browse = cur_obj.browse(self.cr, self.uid, to_rate_search)
            to_rate = to_rate_browse.rate
            
            for from_curr_obj in currency_obj.browse(self.cr, self.uid, [line.invoice_id.currency_id.id]):
			    for from_rate_obj in from_curr_obj.rate_ids:
				    from_datelist.append(from_rate_obj.name)
            from_get_datetime = lambda s: datetime.strptime(s, "%Y-%m-%d")
            from_base = from_get_datetime(line.invoice_id.date_invoice)
            from_later = filter(lambda d: from_get_datetime(d) <= from_base, from_datelist)
            from_closest_date = max(from_later, key = lambda d: from_get_datetime(d))
		
            from_rate_search = cur_obj.search(self.cr, self.uid, [('name', '=', from_closest_date), ('currency_id', '=', line.invoice_id.currency_id.id)])[0]
            from_rate_browse = cur_obj.browse(self.cr, self.uid, from_rate_search)
            from_rate = from_rate_browse.rate
            
            rate = round((to_rate / from_rate), 2)
            self.cr.execute("select product_id from account_invoice_line WHERE id = %s", (line.id,))
            product_id = self.cr.fetchall()[0][0]
            if product_id is not None:
                if cat.id == line.product_id.categ_id.id:
                    update = self.grand_total[cat.id] + (line.price_subtotal * rate)
                    self.grand_total.update({cat.id : update})
                    return (line.price_subtotal * rate)
                else:
                    return ''
            else:
                return ''

    def _set_total(self, total):
          self.total += total

    def _get_total(self):
        return self.total

    def _branch_code(self, branch_id):
        return self.pool.get('res.branch').read(self.cr, self.uid, branch_id,['branch_code']).get('branch_code')

    def _get_grand_total(self, cat_id):
        total = self.grand_total[cat_id]
        return total
report_sxw.report_sxw('report.sale.day.book', 'sale.day.book.wizard', 'addons/sale_day_book_report/report/sale_daybook_report.mako', parser=sale_day_book_report, header=False)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

