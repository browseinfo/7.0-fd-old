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
from openerp.osv import osv, fields
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class sales_forecast(osv.Model):
    _inherit = ['mail.thread', 'ir.needaction_mixin']       
    _name = 'sales.forecast'
    
    _columns = {
        'name': fields.char('Order Reference'),
        'prerid_from': fields.date('Period From', states={'draft': [('readonly', False)], 'confirm': [('readonly', True)]}),
        'prerid_to': fields.date('Period To', states={'draft': [('readonly', False)], 'confirm': [('readonly', True)]}),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('confirm', 'Confirmed'),
            ('cancel', 'Cancel')], 'Status'),
        'order_line': fields.one2many('sales.forecast.line', 'order_id', 'Order Lines', states={'draft': [('readonly', False)], 'confirm': [('readonly', True)]}),
        'branch_id': fields.many2one('res.branch', 'Branch', states={'draft': [('readonly', False)], 'confirm': [('readonly', True)]}),
        'company_id': fields.related('shop_id','company_id',type='many2one',relation='res.company',string='Company',store=True,readonly=True),
        'shop_id': fields.many2one('sale.shop', 'Shop', required=True, states={'draft': [('readonly', False)], 'confirm': [('readonly', True)]}),
    }   
    
    _defaults = {
        'state': 'draft',
    }
    
    def create(self, cr, uid, vals, context=None):
        vals['name'] = 'Order Reference/' + self.pool.get('ir.sequence').get(cr, uid, 'sales.forecast')
        return super(sales_forecast, self).create(cr, uid, vals, context=context)
        
    def action_button_confirm(self, cr, uid, ids, context=None):
        for current_obj in self.browse(cr, uid, ids, context=context):
            if current_obj.order_line:
                for line in current_obj.order_line:
                    if line.state == 'draft':
                        raise osv.except_osv(_('Please send quotation'), _('You cannot confirm because some of Quotation remain to send.'))
            else:
                raise osv.except_osv(_('Please create quotation'), _('You need to create at least one Quotation.'))
                    
            return current_obj.write({'state': 'confirm'})
        
    def action_button_cancel(self, cr, uid, ids, context=None):
        current_obj = self.browse(cr, uid, ids, context=context)[0]
        current_obj.write({'state': 'cancel'})
        return True
        
    def action_button_redraft(self, cr, uid, ids, context=None):
        current_obj = self.browse(cr, uid, ids, context=context)[0]
        current_obj.write({'state': 'draft'})
        return True
        
    def forecast_to_sale_view(self, cr, uid, ids, context=None):
       view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'sale', 'view_order_tree')
       view_id = view_ref and view_ref[1] or False,
       domain = [
           ('forecast_id', '=', ids[0])
       ]
       
       return {
           'type': 'ir.actions.act_window',
           'domain': domain,
           'name': _('Sales Order'),
           'res_model': 'sale.order',
           'view_type': 'form',
           'view_mode': 'tree,form',
           'target': 'current',
           'nodestroy': True,
       }

class sales_forecast_line(osv.Model):       
    _name = 'sales.forecast.line'
    
    _columns = {
        'product_id': fields.many2one('product.product', 'Product', required=True),
        'date': fields.date('Date', required=True),
        'customer_id': fields.many2one('res.partner', 'Customer', domain=[('customer', '=', True)], required=True),
        'product_qty': fields.float('Quantity', digits_compute= dp.get_precision('Product UoS'), required=True),
        'product_uom': fields.many2one('product.uom', 'Unit of Measure ', required=True),
        'order_id': fields.many2one('sales.forecast', 'Order Reference'),
        'dummy_button': fields.boolean('Dummy'),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('confirm', 'Draft Quotation')], 'Status'),
    }
    
    _defaults = {
        'product_qty': 1,
        'dummy_button': False,
        'state': 'draft',
    }
    
    def product_id_change(self, cr, uid, ids, product_id, context=None):
        vals = {}
        product_uom_obj = self.pool.get('product.uom')
        product_obj = self.pool.get('product.product')
        
        product_browse = product_obj.browse(cr, uid, [product_id], context=context)[0]
        
        if product_browse.uom_id.id:
            vals['product_uom'] = product_browse.uom_id.id
            vals['date'] = time.strftime('%Y-%m-%d')
            
        return {'value': vals}
        
    def sales_forecast_confirm(self, cr, uid, ids, context=None):
        vals = {}
        current_obj = self.browse(cr, uid, ids, context=context)[0]
        vals = {
            'partner_id': current_obj.customer_id.id,
            'date_order': current_obj.date,
            'order_line': [(0,0, {
                        'product_id': current_obj.product_id.id,   
                        'name': '[' + current_obj.product_id.default_code + '] ' + current_obj.product_id.name,
                        'product_uom_qty': current_obj.product_qty,
                        'product_uom': current_obj.product_uom.id,
                        'price_unit': current_obj.product_id.list_price,
             })],
             'pricelist_id': current_obj.customer_id.property_product_pricelist.id,
             'partner_invoice_id': current_obj.customer_id.id,
             'partner_shipping_id': current_obj.customer_id.id,
             'forecast_id': current_obj.order_id.id,
             'date_ext': current_obj.date,
             'branch_id': current_obj.order_id.branch_id.id,
             'client_order_ref': current_obj.customer_id.ref or '',
             'shop_id': current_obj.order_id.shop_id.id,
             'company_id': current_obj.order_id.company_id.id,
        }
        
        self.pool.get('sale.order').create(cr, uid, vals, context=context)
        current_obj.write({'dummy_button': True, 'state': 'confirm'})
        return True
        
class sale_order(osv.Model):
    _inherit = 'sale.order'
    _columns = {
        'forecast_id': fields.many2one('sales.forecast', 'Sales Forecast',),
    }
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
