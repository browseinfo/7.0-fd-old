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

from dateutil.relativedelta import relativedelta
import time
from tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from tools.float_utils import float_compare
from osv.orm import browse_record, browse_null
from osv import fields, osv
from tools.translate import _
import netsvc

class delivery_order_merge(osv.osv_memory):
    _name = "delivery.order.merge"
    _description = "Merge Delivery Order"
    
    _columns = {
        'shipment_ids' : fields.many2many('stock.picking.out',  'merge_delivery_rel', 'merge_id', 'picking_id', 'Deliveries',  domain=[('type', '=', 'out'),('state', '!=', 'done')]),
    }

#    def view_init(self, cr , uid , fields_list, context=None):
#        obj_pick = self.pool.get('stock.picking')
#        if context is None:
#            context = {}
#        if context.get('active_id',False):
#            if obj_pick.browse(cr, uid, context['active_id']).state == 'done':
#                raise osv.except_osv(_('Error'), _('Merging is Not allowed on Done Orders!'))
#            pass

    def default_get(self, cr, uid, fields, context=None):
        """
        This function gets default values
        """
        record_ids = context and context.get('active_ids', False) or False
        res = super(delivery_order_merge, self).default_get(cr, uid, fields, context=context)

        if record_ids:
            pick_ids = []
            picks = self.pool.get('stock.picking.out').browse(cr, uid, record_ids, context=context)
            for pick in picks:
                if pick.state in ('draft', 'confirmed', 'assigned'):
                    pick_ids.append(pick.id)
            if 'shipment_ids' in fields:
                res.update({'shipment_ids': pick_ids})
        return res
        

    def do_merge(self, cr, uid, ids, context=None):
        """
             To merge similar type of delivery orders.

             @param self: The object pointer.
             @param cr: A database cursor
             @param uid: ID of the user currently logged in
             @param ids: the ID or list of IDs
             @param context: A standard dictionary

             @return: delivery order view

        """
        pick_obj = self.pool.get('stock.picking')
        mod_obj =self.pool.get('ir.model.data')
        move_obj = self.pool.get('stock.move')
        if context is None:
            context = {}
        
        result = mod_obj._get_id(cr, uid, 'stock', 'view_picking_form')
        id = pick_obj.read(cr, uid, result, ['res_id'])
        record = self.browse(cr, uid, ids[0], context=context)
        shipments = record.shipment_ids
        invoice = []
        state = []
        pick_ids = []
        branch = []
        partner = []
        moves_product = []
        origin = ''
        if len(shipments) < 2:
            raise osv.except_osv(_('Warning'),
                _('Please select multiple order to merge in the list view.'))
        
        new_pick = self.pool.get('stock.picking.out').create(cr, uid,{'type': 'out','state': 'draft',}, context=context)
        pick_data = pick_obj.browse(cr,uid,new_pick,context=context)
        pick_name = pick_data.pick_name
        
        for line in shipments:
            origin += line.name
            state.append(line.state)
            invoice.append(line.invoice_state)
            branch.append(line.branch_id.id)
            partner.append(line.partner_id.id)
            if not partner[1:] == partner[:-1]:
                 raise osv.except_osv(_('Warning!'),
                                         _('Merging is only allowed on same Partner'))            
            if not state[1:] == state[:-1]:
                 raise osv.except_osv(_('Warning!'),
                                         _('Merging is only allowed on same state'))
            if not invoice[1:] == invoice[:-1]:
                 raise osv.except_osv(_('Warning!'),
                                         _('Merging is only allowed on same Invoice state'))
            if not branch[1:] == branch[:-1]:
                 raise osv.except_osv(_('Warning!'),
                                         _('Merging is only allowed on same branch'))
            if line.state in ('done'):
                raise osv.except_osv(_('Warning!'),
                         _('Merging is Not allowed on Done Orders.'))
            
            for move in line.move_lines:
            	if  move.product_id.id in moves_product:
            		cr.execute("select sum(product_qty) from stock_move where picking_id=%s and product_id=%s", (new_pick, move.product_id.id))
            		product_qty = cr.fetchone()
            		new_qty = product_qty[0] + move.product_qty
            		cr.execute("update stock_move set product_qty = %s where picking_id=%s and product_id=%s", (new_qty,new_pick, move.product_id.id))
            	else:
	            	move_obj.create(cr, uid,{
				            'name': move.name or '',
				            'product_id': move.product_id and move.product_id.id or False,
				            'product_qty': move.product_qty,
				            'product_uos_qty': move.product_uos_qty,
				            'product_uom': move.product_uom and move.product_uom.id or False,
				            'product_uos': move.product_uos and move.product_uos.id or False,
				            'date': move.date,
				            'date_expected': move.date_expected,
				            'location_id':move.location_id and move.location_id.id or False,
				            'location_dest_id':move.location_dest_id and move.location_dest_id.id or False,
				            'picking_id': new_pick,
				            'partner_id': move.partner_id and move.partner_id.id or False,
				            'move_dest_id': move.move_dest_id and move.move_dest_id.id or False,
				            'state': move.state,
				            'type':move.type,
				            'company_id': move.company_id.id,
				            'price_unit': move.price_unit,
	        			}, context=context)
	            	moves_product.append(move.product_id.id)
                
                #move_obj.write(cr, uid, [move.id], {'picking_id':new_pick, 'origin':origin}, context=context)
            pick_obj.write(cr, uid, [new_pick], {'invoice_state': line.invoice_state, 'state': line.state, 'partner_id': line.partner_id and line.partner_id.id or False,'origin':origin, 'branch_id': line.branch_id.id}, context=context)
            origin += '-'
            if pick_ids:
                new_id = line.id
                pick_ids.append(new_id)
            else:
                 pick_ids.append(line.id)
            pick_obj.write(cr, uid, [new_pick], {'pick_name': pick_ids}, context=context)
            wf_service = netsvc.LocalService("workflow")
            for pick in pick_ids:
            	wf_service.trg_validate(uid, 'stock.picking', pick, 'button_cancel', cr)
        return {
                'name': _('Delivery Order'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'stock.picking.out',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'context': {'type' : 'out', 'active_id': [new_pick]}
            }

delivery_order_merge()

class incoming_shipment_merge(osv.osv_memory):
    _name = "incoming.shipment.merge"
    _description = "Merge Incoming Shipment"
    
    _columns = {
        'shipment_ids' : fields.many2many('stock.picking.in',  'merge_incoming_rel', 'merge_id', 'picking_id', 'Incoming',  domain=[('type', '=', 'in'),('state', '!=', 'done')]),
    }

#    def view_init(self, cr , uid , fields_list, context=None):
#        obj_pick = self.pool.get('stock.picking')
#        if context is None:
#            context = {}
#        if context.get('active_id',False):
#            if obj_pick.browse(cr, uid, context['active_id']).state == 'done':
#                raise osv.except_osv(_('Error'), _('Merging is Not allowed on Done Orders!'))
#            pass

    def default_get(self, cr, uid, fields, context=None):
        """
        This function gets default values
        """
        record_ids = context and context.get('active_ids', False) or False
        res = super(incoming_shipment_merge, self).default_get(cr, uid, fields, context=context)

        if record_ids:
            pick_ids = []
            picks = self.pool.get('stock.picking.in').browse(cr, uid, record_ids, context=context)
            for pick in picks:
                if pick.state in ('draft', 'confirmed', 'assigned'):
                    pick_ids.append(pick.id)
            if 'shipment_ids' in fields:
                res.update({'shipment_ids': pick_ids})
        return res
        

    def do_merge(self, cr, uid, ids, context=None):
        """
             To merge similar type of delivery orders.

             @param self: The object pointer.
             @param cr: A database cursor
             @param uid: ID of the user currently logged in
             @param ids: the ID or list of IDs
             @param context: A standard dictionary

             @return: delivery order view

        """
        pick_obj = self.pool.get('stock.picking')
        mod_obj =self.pool.get('ir.model.data')
        move_obj = self.pool.get('stock.move')
        if context is None:
            context = {}
        
        result = mod_obj._get_id(cr, uid, 'stock', 'view_picking_form')
        id = pick_obj.read(cr, uid, result, ['res_id'])
        record = self.browse(cr, uid, ids[0], context=context)
        shipments = record.shipment_ids
        invoice = []
        state = []
        pick_ids = []
        if len(shipments) < 2:
            raise osv.except_osv(_('Warning'),
                _('Please select multiple order to merge in the list view.'))
        
        new_pick = self.pool.get('stock.picking.in').create(cr, uid,{'type': 'in','state': 'draft',}, context=context)
        pick_data = pick_obj.browse(cr,uid,new_pick,context=context)
        pick_name = pick_data.pick_name
        
        for line in shipments:
            origin += line.name
            state.append(line.state)
            invoice.append(line.invoice_state)
            branch.append(line.branch_id.id)
            partner.append(line.partner_id.id)
            if not partner[1:] == partner[:-1]:
                 raise osv.except_osv(_('Warning!'),
                                         _('Merging is only allowed on same Partner'))            
            if not state[1:] == state[:-1]:
                 raise osv.except_osv(_('Warning!'),
                                         _('Merging is only allowed on same state'))
            if not invoice[1:] == invoice[:-1]:
                 raise osv.except_osv(_('Warning!'),
                                         _('Merging is only allowed on same Invoice state'))
            if not branch[1:] == branch[:-1]:
                 raise osv.except_osv(_('Warning!'),
                                         _('Merging is only allowed on same branch'))
            if line.state in ('done'):
                raise osv.except_osv(_('Warning!'),
                         _('Merging is Not allowed on Done Orders.'))
            
            for move in line.move_lines:
            	if  move.product_id.id in moves_product:
            		cr.execute("select sum(product_qty) from stock_move where picking_id=%s and product_id=%s", (new_pick, move.product_id.id))
            		product_qty = cr.fetchone()
            		new_qty = product_qty[0] + move.product_qty
            		cr.execute("update stock_move set product_qty = %s where picking_id=%s and product_id=%s", (new_qty,new_pick, move.product_id.id))
            	else:
	            	move_obj.create(cr, uid,{
				            'name': move.name or '',
				            'product_id': move.product_id and move.product_id.id or False,
				            'product_qty': move.product_qty,
				            'product_uos_qty': move.product_uos_qty,
				            'product_uom': move.product_uom and move.product_uom.id or False,
				            'product_uos': move.product_uos and move.product_uos.id or False,
				            'date': move.date,
				            'date_expected': move.date_expected,
				            'location_id':move.location_id and move.location_id.id or False,
				            'location_dest_id':move.location_dest_id and move.location_dest_id.id or False,
				            'picking_id': new_pick,
				            'partner_id': move.partner_id and move.partner_id.id or False,
				            'move_dest_id': move.move_dest_id and move.move_dest_id.id or False,
				            'state': move.state,
				            'type':move.type,
				            'company_id': move.company_id.id,
				            'price_unit': move.price_unit,
	        			}, context=context)
	            	moves_product.append(move.product_id.id)
                
                #move_obj.write(cr, uid, [move.id], {'picking_id':new_pick, 'origin':origin}, context=context)
            pick_obj.write(cr, uid, [new_pick], {'invoice_state': line.invoice_state, 'state': line.state, 'partner_id': line.partner_id and line.partner_id.id or False,'origin':origin, 'branch_id': line.branch_id.id}, context=context)
            origin += '-'
            if pick_ids:
                new_id = line.id
                pick_ids.append(new_id)
            else:
                 pick_ids.append(line.id)
            pick_obj.write(cr, uid, [new_pick], {'pick_name': pick_ids}, context=context)
            wf_service = netsvc.LocalService("workflow")
            for pick in pick_ids:
            	wf_service.trg_validate(uid, 'stock.picking', pick, 'button_cancel', cr)
        return {
                'name': _('Delivery Order'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'stock.picking.out',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'context': {'type' : 'out', 'active_id': [new_pick]}
            }

incoming_shipment_merge()


class stock_move(osv.osv):
    _inherit = "stock.move"
    _columns = {
        'picking_id': fields.many2one('stock.picking', 'Reference', select=True,states={'done': [('readonly', True)]}),
        'origin': fields.related('picking_id','origin',type='char', size=64, relation="stock.picking", string="Origin", store=True),
    }


stock_move()

class stock_picking(osv.osv):
    _inherit = "stock.picking"
    _columns = {
        'pick_name': fields.char('old picking', size=250),
    }

stock_picking()

class stock_partial_picking_line(osv.osv_memory):
    _inherit = "stock.partial.picking.line"
    _columns = {
        #'picking_id': fields.many2one('stock.picking', 'Picking', required=True, ondelete='CASCADE'),
        'picking_id': fields.many2one('stock.picking', 'Reference', select=True,states={'done': [('readonly', True)]}),
        'origin': fields.related('picking_id','origin',type='char', size=64, relation="stock.picking", string="Origin", store=True),
    }
    
stock_partial_picking_line()


class stock_partial_picking(osv.osv_memory):
    _inherit = "stock.partial.picking"

    def default_get(self, cr, uid, fields, context=None):
        if context is None: context = {}
        res = super(stock_partial_picking, self).default_get(cr, uid, fields, context=context)
        picking_ids = context.get('active_ids', [])
        if not picking_ids or (not context.get('active_model') == 'stock.picking') \
            or len(picking_ids) != 1:
            return res
        picking_id, = picking_ids
        if 'picking_id' in fields:
            res.update(picking_id=picking_id)
        if 'move_ids' in fields:
            picking = self.pool.get('stock.picking').browse(cr, uid, picking_id, context=context)
            moves = [self._partial_move_for(cr, uid, m) for m in picking.move_lines if m.state not in ('done','cancel')]
            res.update(move_ids=moves)
        if 'date' in fields:
            res.update(date=time.strftime(DEFAULT_SERVER_DATETIME_FORMAT))
        return res
        
    def do_partial(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'Partial picking processing may only be done one at a time'
        stock_picking = self.pool.get('stock.picking')
        stock_move = self.pool.get('stock.move')
        uom_obj = self.pool.get('product.uom')
        partial = self.browse(cr, uid, ids[0], context=context)
        partial_data = {
            'delivery_date' : partial.date
        }
        picking_type = partial.picking_id.type
        for wizard_line in partial.move_ids:
            line_uom = wizard_line.product_uom
            move_id = wizard_line.move_id.id

            #Quantiny must be Positive
            if wizard_line.quantity < 0:
                raise osv.except_osv(_('Warning!'), _('Please provide Proper Quantity !'))

            #Compute the quantity for respective wizard_line in the line uom (this jsut do the rounding if necessary)
            qty_in_line_uom = uom_obj._compute_qty(cr, uid, line_uom.id, wizard_line.quantity, line_uom.id)

            if line_uom.factor and line_uom.factor <> 0:
                if float_compare(qty_in_line_uom, wizard_line.quantity, precision_rounding=line_uom.rounding) != 0:
                    raise osv.except_osv(_('Warning'), _('The uom rounding does not allow you to ship "%s %s", only roundings of "%s %s" is accepted by the uom.') % (wizard_line.quantity, line_uom.name, line_uom.rounding, line_uom.name))
            if move_id:
                #Check rounding Quantity.ex.
                #picking: 1kg, uom kg rounding = 0.01 (rounding to 10g), 
                #partial delivery: 253g
                #=> result= refused, as the qty left on picking would be 0.747kg and only 0.75 is accepted by the uom.
                initial_uom = wizard_line.move_id.product_uom
                #Compute the quantity for respective wizard_line in the initial uom
                qty_in_initial_uom = uom_obj._compute_qty(cr, uid, line_uom.id, wizard_line.quantity, initial_uom.id)
                without_rounding_qty = (wizard_line.quantity / line_uom.factor) * initial_uom.factor
                if float_compare(qty_in_initial_uom, without_rounding_qty, precision_rounding=initial_uom.rounding) != 0:
                    raise osv.except_osv(_('Warning'), _('The rounding of the initial uom does not allow you to ship "%s %s", as it would let a quantity of "%s %s" to ship and only roundings of "%s %s" is accepted by the uom.') % (wizard_line.quantity, line_uom.name, wizard_line.move_id.product_qty - without_rounding_qty, initial_uom.name, initial_uom.rounding, initial_uom.name))
            else:
                seq_obj_name =  'stock.picking.out' + picking_type
                move_id = stock_move.create(cr,uid,{'name' : self.pool.get('ir.sequence').get(cr, uid, seq_obj_name),
                                                    'product_id': wizard_line.product_id.id,
                                                    'product_qty': wizard_line.quantity,
                                                    'product_uom': wizard_line.product_uom.id,
                                                    'prodlot_id': wizard_line.prodlot_id.id,
                                                    'location_id' : wizard_line.location_id.id,
                                                    'location_dest_id' : wizard_line.location_dest_id.id,
                                                    'picking_id': partial.picking_id.id
                                                    },context=context)
                stock_move.action_confirm(cr, uid, [move_id], context)
            partial_data['move%s' % (move_id)] = {
                'product_id': wizard_line.product_id.id,
                'product_qty': wizard_line.quantity,
                'product_uom': wizard_line.product_uom.id,
                'prodlot_id': wizard_line.prodlot_id.id,
            }
            if (picking_type == 'out') and (wizard_line.product_id.cost_method == 'average'):
                partial_data['move%s' % (wizard_line.move_id.id)].update(product_price=wizard_line.cost,
                                                                  product_currency=wizard_line.currency.id)
       #try to done old picking
        pick_data= stock_picking.browse(cr, uid, [partial.picking_id.id], context=context)
        line_data = []
        for line in stock_picking.browse(cr, uid, [partial.picking_id.id], context=context):
            if line.pick_name:
                line_data.append(a1)
                b1 =  line.pick_name[5:7]
                line_data.append(b1)
                for li in line_data:
                    wf_service = netsvc.LocalService("workflow")
                    wf_service.trg_validate(uid, 'stock.picking', li, 'button_done', cr)
            
        stock_picking.do_partial(cr, uid, [partial.picking_id.id], partial_data, context=context)
        
        return {'type': 'ir.actions.act_window_close'}
stock_partial_picking()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
