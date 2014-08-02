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
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP
from datetime import datetime, date
import time
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import netsvc

class stock_move(osv.Model):
    _inherit = 'stock.move'
    
    def _get_stock_move_default_branch(self, cr, uid, ids, context=None):
        user_pool = self.pool.get('res.users')
        branch_id = user_pool.browse(cr, uid, uid, context=context).branch_id and user_pool.browse(cr, uid, uid, context=context).branch_id.id or False
        return branch_id
        
    def create(self, cr, uid, vals, context=None):
        if vals.get('picking_id'):
            current_obj = self.pool.get('stock.picking').browse(cr, uid, [vals.get('picking_id')], context=context)[0]
            vals['branch_id'] = current_obj.branch_id.id
        else:
            vals['branch_id'] = self.pool.get('res.users').browse(cr, uid, uid, context=context).branch_id and user_pool.browse(cr, uid, uid, context=context).branch_id.id or False
        return super(stock_move, self).create(cr, uid, vals, context=context)
    
    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }

    _defaults = {
        'branch_id': _get_stock_move_default_branch,
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
