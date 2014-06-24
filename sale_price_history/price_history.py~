# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://browseinfo.in>).
#
##############################################################################
import time

from openerp import netsvc
from openerp.osv import osv, fields
from datetime import datetime
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp


class sale_order(osv.osv):
    _inherit = 'sale.order'
    
    _columns = {
        'sale_history_ids': fields.one2many('sale.order.line.history', 'order_id', 'History Lines', readonly=True),
    }
    
sale_order()

class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'
    
    def create(self, cr, uid, vals, context=None):
        res = super(sale_order_line, self).create(cr, uid, vals, context=context)
        product_obj = self.pool.get('product.product')
        history_obj = self.pool.get('sale.order.line.history')
        if vals.get('price_unit'):
                
                code_line = {
                              'product_id': vals.get('product_id') or False,
                              'product_qty': vals.get('product_uom_qty') or False,
                              'product_uom': vals.get('product_uom') or False or False,
                              'price_unit' : vals.get('price_unit'),
                              'price_unit_old': 0.0,
                              'order_id': vals.get('order_id') or False,
                              'line_id': res,
                   }     
                history_obj.create(cr,uid,code_line, context=context) 
        return res

    
    def write(self, cr, uid, ids, vals, context=None):
        sale_obj=self.pool.get('sale.order')
        product_obj=self.pool.get('product.product')
        sale_line_history_obj=self.pool.get('sale.order.line.history')
        result = super(sale_order_line, self).write(cr, uid, ids, vals, context=context)
        history_ids = sale_line_history_obj.search(cr, uid, [], context=context)
        hist= []
        today = time.strftime('%Y-%m-%d')
        if vals.get('price_unit'):
            for line in self.browse(cr, uid, ids, context):
                for history in sale_line_history_obj.browse(cr, uid, history_ids, context):
                    if history:
                        if history.line_id == line and history.product_id == line.product_id:
                            print "#######################"
                            sale_line_history_obj.write(cr, uid, [history.id], {'price_unit': line.price_unit,'price_unit_old': history.price_unit})
                            hist.append(history.id)
        return result
sale_order_line()

class prepurchase_order_line_history(osv.osv):
    _name = 'sale.order.line.history'
    

    _columns = {
        'product_id': fields.many2one('product.product', 'Product', domain=[('purchase_ok','=',True)], change_default=True),
        'product_qty': fields.float('Quantity', digits_compute=dp.get_precision('Product Unit of Measure'), required=True),
        'product_uom': fields.many2one('product.uom', 'Product Unit of Measure', required=True),
        'price_unit': fields.float('New Price', required=True, digits_compute= dp.get_precision('Product Price')),
        'price_unit_old': fields.float('Old Price', required=True, digits_compute= dp.get_precision('Product Price')),
        'taxes_id': fields.many2many('account.tax', 'purchase_order_taxe', 'ord_id', 'tax_id', 'Taxes'),
        'order_id': fields.many2one('sale.order', 'Order Reference', select=True, required=True, ondelete='cascade'),
        'company_id': fields.related('order_id','company_id',type='many2one',relation='res.company',string='Company', store=True, readonly=True),
        'partner_id': fields.related('order_id','partner_id',string='Partner',readonly=True,type="many2one", relation="res.partner", store=True),
        'state': fields.selection([('draft', 'Draft')], 'Status', readonly=True,
                                  help=' * The \'Draft\' status is set automatically when purchase order in draft status.'),
        'line_id': fields.many2one('sale.order.line', 'Sale Order line'),
    }
    
    _defaults = {
        'product_qty': lambda *a: 1.0,
        'state': lambda *args: 'draft',
    }
prepurchase_order_line_history()



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
