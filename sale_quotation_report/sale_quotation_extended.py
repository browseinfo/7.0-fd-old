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
from openerp.osv import osv, fields
from openerp.tools.translate import _
import netsvc

class sale_order(osv.Model):
    _inherit = 'sale.order'
    _columns = {
        'delivery_id': fields.many2one('delivery.delivery', "Delivery"),
        'maker_id': fields.many2one('maker.maker', "Maker"),
        'leadtime_id':fields.many2one('lead.time',"Lead Time")
    }
    
    def print_quotation(self, cr, uid, ids, context=None):
        '''
        This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        wf_service = netsvc.LocalService("workflow")
        wf_service.trg_validate(uid, 'sale.order', ids[0], 'quotation_sent', cr)
        datas = {
                 'model': 'sale.order',
                 'ids': ids,
                 'form': self.read(cr, uid, ids[0], context=context),
        }
        return {'type': 'ir.actions.report.xml', 'report_name': 'sale.quotation.report', 'datas': datas, 'nodestroy': True}


class delivery_delivery(osv.Model):
    _name = 'delivery.delivery'
    _columns = {
        'name': fields.char('Name', required=True),
        'code': fields.char('Code', size=252),
    }

class maker_maker(osv.Model):
    _name = 'maker.maker'
    _columns = {
        'name': fields.char('Name', required=True),
        'code': fields.char('Code', size=252),
    }

class lead_time(osv.Model):
    _name = 'lead.time'
    _columns = {
        'name': fields.char('Name', required=True),
        'code': fields.char('Code', size=252),
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
