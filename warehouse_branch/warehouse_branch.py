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
from openerp.osv import osv, fields
from openerp.tools.translate import _

class stock_picking(osv.Model):
    _inherit = 'stock.picking'
    
    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }

    def action_invoice_create(self, cr, uid, ids, journal_id=False,
            group=False, type='out_invoice', context=None):
        invoice_obj = self.pool.get('account.invoice')
        picking_obj = self.pool.get('stock.picking')
        invoice_line_obj = self.pool.get('account.invoice.line')
        result = super(stock_picking, self).action_invoice_create(cr, uid,
                ids, journal_id=journal_id, group=group, type=type,
                context=context)
        for picking in picking_obj.browse(cr, uid, result.keys(), context=context):
            invoice = invoice_obj.browse(cr, uid, result[picking.id], context=context)
            invoice.write({'branch_id': picking.branch_id.id })
            invoice_line = self._prepare_shipping_invoice_line(cr, uid, picking, invoice, context=context)
            if invoice_line:
                invoice_line_obj.create(cr, uid, invoice_line)
                invoice_obj.button_compute(cr, uid, [invoice.id], context=context)
        return result
        
class stock_picking_in(osv.Model):
    _inherit = 'stock.picking.in'
    
    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }
    
class stock_picking_out(osv.Model):
    _inherit = 'stock.picking.out'
    
    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }
    
    
class stock_inventory(osv.Model):
    _inherit = 'stock.inventory'
    
    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True)
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
