# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://browseinfo.in>).
#

##############################################################################
import time
import operator
import itertools
from datetime import datetime
from dateutil import relativedelta
from report import report_sxw
from openerp.tools.amount_to_text_en import amount_to_text


class sale_amount_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(sale_amount_report, self).__init__(cr, uid, name, context)
        self.partner_name = ''
        self.partner_list = []
        self.index = 1
        self.line_quantity = 0
        self.brk = False
        self.localcontext.update({  
            'get_amount_data': self._get_amount_data,
            'get_from_date': self.get_from_date,
            'get_end_date': self.get_end_date,
            'get_partner': self.get_partner,
            'get_total_qty': self.get_total_qty,
            'get_subtotal_qty': self.get_subtotal_qty,
            'get_total_amount': self.get_total_amount,
            'date_format': self.date_format,
        })

    def set_context(self, objects, data, ids, report_type=None):
        obj_partner = self.pool.get('res.partner')
        start_date = data['form']['start_date']
        end_date = data['form']['end_date']
        formatter_string = "%Y-%m-%d" 
        datetime_object = datetime.strptime(start_date, formatter_string)
        date_object = datetime_object.date()
        datetime_object_to = datetime.strptime(end_date, formatter_string)
        date_object_to = datetime_object_to.date()
        self.start_date = date_object.strftime("%d-%B-%Y")
        self.end_date = date_object_to.strftime("%d-%B-%Y")
        self.cr.execute(
                "SELECT DISTINCT so.partner_id  FROM sale_order_line AS l "\
                "left join sale_order as so on (l.order_id = so.id)"\
                "WHERE so.state != 'draft' AND (so.date_order >= %s) AND (so.date_order <= %s)"\
                "group by l.id, so.id,so.partner_id", (self.start_date, self.end_date))
        self.partner_ids = [x[0] for x in self.cr.fetchall()]
        objects = obj_partner.browse(self.cr, self.uid, self.partner_ids)
        return super(sale_amount_report, self).set_context(objects, data, self.partner_ids, report_type=report_type)

    def get_from_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def get_total_qty(self):
        return int(self.total_qty)

    def get_subtotal_qty(self):
        return int(self.sub_total_qty)

#     def get_total_qty_cust(self):
#         return int(self.qty)

    def get_total_amount(self):
        return self.total_amount

    def get_partner(self):
        return self.partner_name
    
    def _get_amount_data(self, obj):
        sale_obj = self.pool.get('sale.order')
        line_obj = self.pool.get('sale.order.line')
        self.total_qty = 0
        self.total_amount = 0.0
        self.sub_total_qty = 0
        res = []
        result = []
        line_name = []
        self.cr.execute("select DISTINCT so.id from sale_order_line sol "\
        "left join sale_order as so on (sol.order_id = so.id) "\
        "WHERE (so.state != 'draft') AND (so.date_order >= %s) AND (so.date_order <= %s)"\
        "AND so.partner_id = %s"\
        "group by so.id,so.partner_id", (self.start_date, self.end_date, obj.id,))
        temp = [x[0] for x in self.cr.fetchall()]
        print "temp==========", temp
        if temp:
            for so in sale_obj.browse(self.cr, self.uid, temp):
                self.sub_total_qty = 0
                self.total_amount = self.total_amount + so.amount_untaxed
                self.partner_name = so.partner_id.name
                for line in so.order_line:
                    self.sub_total_qty = self.sub_total_qty + line.product_uom_qty
                    profit = 0.0 
                    profit_percent = 0.0
                    if line.product_id:
                        profit = line.price_subtotal - (line.product_uom_qty * line.product_id.standard_price)
                        profit_percent = (profit * 100) / line.price_subtotal
                    res.append({'date_invoice': self.date_format(so.date_order),
                                'partner_id': so.partner_id.name,
                                'number': so.name,
                                'origin':so.origin,
                                'default_code': line.product_id.default_code,
                                'product_id': line.product_id.name,
                                'quantity': int(line.product_uom_qty),
                                'qty_total': int(self.sub_total_qty),
                                'price_unit': line.price_unit,
                                'price_subtotal': line.price_subtotal,
                                'total_amount': so.amount_untaxed,
                                'profit': profit,
                                'profit_percent': round(profit_percent, 2),
                            })
                    self.total_qty = self.total_qty + line.product_uom_qty
                    self.line_quantity = line.product_uom_qty
            newlist = sorted(res, key=lambda k: k['date_invoice'])
            groups = itertools.groupby(newlist, key=operator.itemgetter('partner_id'))
            result = [{'partner_id':k,'values':[x for x in v]} for k,v in groups]
            self.total_sum_qty = 0
            self.total_sum = 0
            for vals in result:
                self.qty_main_total = 0
                self.main_total = 0
                for loop in vals['values']:
                    self.qty_main_total += loop['quantity']
                    self.main_total += loop['price_subtotal']
                vals['total'] = self.qty_main_total
                vals['sum_total'] = self.main_total
                self.total_sum_qty += vals['total']
                self.total_sum += vals['sum_total']
            return result

#     def new_partner(self,partner):
#         partnerlist = []
#         print "#########partner#########", partner
#         if not partner in partnerlist:
#             print "partner in=============", partner
#             return False
#         else: 
#             return True
#         return False    
    def date_format(self, datedetail):
        if datedetail:
            a = time.strptime(datedetail,'%Y-%m-%d')
            b = time.strftime('%d-%B-%Y', a)
            return b
        else:
            return ''
        
report_sxw.report_sxw('report.sale.amount.report', 'sale.order', 'sales_ledger_report/report/sale_amount.mako', parser=sale_amount_report, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

