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
        })
    def _date_format(self, date):
        if date is not False:
            d = datetime.datetime.strptime(date, '%Y-%m-%d')
            date = d.strftime('%d-%b-%Y')
            return date
        else:
            return ''
        
    def _total_dict(self):
        self.grand_total = dict.fromkeys([cat.id for cat in self.categ], 0)

    def _get_categ(self):
        print"\n\nself=>",self
        cat_pool = self.pool.get('product.category')
        cat_list = []
        print "\ncat_pool.search(self.cr, self.uid, []):==>",cat_pool.search(self.cr, self.uid, [])
        for categ_id in cat_pool.search(self.cr, self.uid, []):
            print "\ncateg_id==>",categ_id
            print "\ncat_pool.browse(self.cr, self.uid, categ_id)",cat_pool.browse(self.cr, self.uid, categ_id)
            cat_list.append(cat_pool.browse(self.cr, self.uid, categ_id))
        self.categ = cat_list
        print "\ncat_list",cat_list
        return cat_list

    def _sale_details(self, obj):
        self.start_date = obj['start_date']
        self.end_date = obj['end_date']                
        self.cr.execute("select ai.id from account_invoice ai "\
                    "WHERE (ai.date_invoice >= %s) AND (ai.date_invoice <= %s) AND ai.type='out_invoice' AND ai.state !='draft' ", (self.start_date, self.end_date,))
        
        objects = []
        for po_id in [po_id[0] for po_id in self.cr.fetchall()]:
            objects.append(self.pool.get('account.invoice').browse(self.cr, self.uid, po_id))
        return objects

    def _categ_price(self, line, cat):
        self.cr.execute("select product_id from account_invoice_line WHERE id = %s", (line.id,))
        product_id = self.cr.fetchall()[0][0]
        if product_id is not None:
            if cat.id == line.product_id.categ_id.id:
                update = self.grand_total[cat.id] + line.price_subtotal
                self.grand_total.update({cat.id : update})
                return line.price_subtotal
            else:
                return ''
        else:
            return ''
    
    def _set_total(self, total):
          self.total += total

    def _get_total(self):
        return self.total
    
    
    def _get_grand_total(self, cat_id): 
        total = self.grand_total[cat_id]
        return total
report_sxw.report_sxw('report.sale.day.book', 'sale.day.book.wizard', 'addons/sale_day_book_report/report/sale_daybook_report.mako', parser=sale_day_book_report, header="internal landscape")
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

