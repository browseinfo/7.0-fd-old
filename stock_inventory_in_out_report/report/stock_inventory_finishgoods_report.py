# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-2013 Serpent Consulting Services (<http://www.serpentcs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################
import time
import datetime
from openerp.report import report_sxw
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.exceptions

class stock_inventory_finishgood_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(stock_inventory_finishgood_report, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
            'get_all_lines': self._get_all_lines,
            'sum_total': self.sum_total,
            'all_total': self.all_total,
            'date_format': self.date_format,
            'get_branch': self._get_branch,
        })
        
    def set_context(self, objects, data, ids, report_type=None):
        self.date_from = data['form'].get('startdtae', time.strftime('%Y-%m-%d'))
        self.date_to = data['form'].get('enddtae', time.strftime('%Y-%m-%d'))
        self.branch = data['form'].get('branch_id')
        return super(stock_inventory_finishgood_report, self).set_context(objects, data, ids, report_type=report_type)

    def sum_total(self):
        return self.regi_total

    def all_total(self):
        return self.all_total

    def date_format(self, datedetail):
        if datedetail:
            date = datetime.datetime.strptime(datedetail, '%Y-%m-%d')
            date = date.strftime('%d-%b-%Y')
            return date
        else:
            return ''

    def _get_branch(self, branch):
        branch_obj = self.pool.get('res.branch')
        if self.branch[0]:
            ob_name = branch_obj.browse(self.cr, self.uid, self.branch[0])
            return ob_name.name
        
    def merge_lists(self,l1, l2, key):
        merged = {}
        for item in l1+l2:
            if item[key] in merged:
                merged[item[key]].update(item)
            else:
                merged[item[key]] = item
        return [val for (_, val) in merged.items()]
    
    def _get_all_lines(self, data):
        res = []
        newres = []
        getres = []
        inv_list = []
        line_list = []
        self.regi_total = 0.0
        self.all_total = 0.0
        new = {}
        self.cr.execute("select sl.id from stock_location sl where scrap_location='True'")
        warehouse_id = self.cr.fetchone()
        if warehouse_id:
            self.cr.execute("select pt.id, pp.default_code,pt.name, sum(sm.product_uos_qty) as in_qty, pu.name as uom from stock_move as sm "\
                    "left join stock_picking as sp on sm.picking_id = sp.id "\
                    "left join product_product as pp on sm.product_id = pp.id "\
                    "left join product_template as pt on pp.product_tmpl_id = pt.id "\
                    "left join product_uom as pu on pt.uom_id = pu.id "\
                    "left join stock_location as lc on sm.location_dest_id = lc.id "\
                    "where sm.location_dest_id= %s "\
                    "and sm.branch_id= %s "\
                    "and pp.finish_goods = 'True'"\
                    "and sm.state = 'done'"\
                    "and sp.type = 'in'"\
                    "and (sm.create_date <= %s)" \
                    "group by pt.id, pp.default_code, pt.name,pt.standard_price, pu.name order by pt.name",
                            ( warehouse_id[0],data.branch_id.id,self.date_to))
            in_stock_lines = self.cr.dictfetchall()
            self.cr.execute("select pt.id, pp.default_code,pt.name, sum(sm.product_uos_qty) as out_qty, pu.name as uom from stock_move as sm "\
                    "left join stock_picking as sp on sm.picking_id = sp.id "\
                    "left join product_product as pp on sm.product_id = pp.id "\
                    "left join product_template as pt on pp.product_tmpl_id = pt.id "\
                    "left join product_uom as pu on pt.uom_id = pu.id "\
                    "left join stock_location as lc on sm.location_id = lc.id "\
                    "where sm.location_id= %s "\
                    "and sm.branch_id= %s "\
                    "and pp.finish_goods = 'True'"\
                    "and sm.state = 'done'"\
                    "and sp.type = 'out'"\
                    "and (sm.create_date <= %s)"\
                    "group by pt.id, pp.default_code,pt.name,pt.standard_price, pu.name  order by pt.name",
                            ( warehouse_id[0],data.branch_id.id,self.date_to))
    
            stock_lines = self.cr.dictfetchall()
            new = self.merge_lists(in_stock_lines, stock_lines, 'id')
            if new:
                for line in new:
                    qty = line.get('in_qty', False) - line.get('out_qty', False)
                    nwqty = abs(qty)
                    newres.append({
                        'code': line.get('default_code', False),
                        'product': line.get('name', False),
                        'uom': line.get('uom', False),
                        'totalqty': nwqty,
                       })
           
            self.cr.execute("select pt.id, pp.default_code,pt.name, sum(sm.product_uos_qty) as in_qty, pu.name as uom from stock_move as sm "\
                    "left join stock_picking as sp on sm.picking_id = sp.id "\
                    "left join product_product as pp on sm.product_id = pp.id "\
                    "left join product_template as pt on pp.product_tmpl_id = pt.id "\
                    "left join product_uom as pu on pt.uom_id = pu.id "\
                    "left join stock_location as lc on sm.location_dest_id = lc.id "\
                    "where sm.location_dest_id= %s "\
                    "and sm.branch_id= %s "\
                    "and pp.finish_goods = 'True'"\
                    "and sm.state = 'done'"\
                    "and sp.type = 'in'"\
                    "and (sm.create_date <= %s) and (sm.create_date >= %s)" \
                    "group by pt.id, pp.default_code, pt.name,pt.standard_price, pu.name order by pt.name",
                            ( warehouse_id[0],data.branch_id.id,self.date_to,self.date_from))
    
            in_lines = self.cr.dictfetchall()
    
            self.cr.execute("select pt.id, pp.default_code,pt.name, sum(sm.product_uos_qty) as out_qty, pu.name as uom from stock_move as sm "\
                    "left join stock_picking as sp on sm.picking_id = sp.id "\
                    "left join product_product as pp on sm.product_id = pp.id "\
                    "left join product_template as pt on pp.product_tmpl_id = pt.id "\
                    "left join product_uom as pu on pt.uom_id = pu.id "\
                    "left join stock_location as lc on sm.location_id = lc.id "\
                    "where sm.location_id= %s "\
                    "and sm.branch_id= %s "\
                    "and pp.finish_goods = 'True'"\
                    "and sm.state = 'done'"\
                    "and sp.type = 'out'"\
                    "and (sm.create_date <= %s) and (sm.create_date >= %s)" \
                    "group by pt.id, pp.default_code,pt.name,pt.standard_price, pu.name  order by pt.name",
                            ( warehouse_id[0],data.branch_id.id,self.date_to,self.date_from))
    
            pick_lines = self.cr.dictfetchall()
            
            
            
            result = self.merge_lists(in_lines, pick_lines, 'id')
            if result:
                for line in in_lines:
                    res.append({
                        'code': line.get('default_code', False),
                        'product': line.get('name', False),
                        'uom': line.get('uom', False),
                        'in_qty': line.get('in_qty', False),
                        'out_qty': line.get('out_qty', False),
                        'totalqty': nwqty,
                       })
                    #self.regi_total = line[2]
                    #self.all_total = total
            get = self.merge_lists(res, newres, 'product')
            if get:
                for line in get:
                    stockinobj = self.pool.get('stock.inventory')
                    if line.get('product'):
                         self.cr.execute("select si.id from stock_inventory si where state='done' and (si.date <= %s) and (si.date >= %s)", (self.date_to, self.date_from,))
                         invids = [ i for i in self.cr.fetchall()[0]]
                         for si in stockinobj.browse(self.cr,self.uid, invids):
                             inv_qty = 0
                             for move in si.move_ids:
                                 productname = move.product_id.name
                                 if productname == line.get('product', False):
                                     inv_qty = move.product_qty
                    last_qty = line.get('totalqty', False) + line.get('in_qty', False) - line.get('out_qty', False)
                    opening_qty = last_qty + inv_qty
                    if inv_qty < 0:
                        katering = 'Selisih Kurang'
                    if inv_qty > 0:
                        katering = 'Selisih lebih'
                    if inv_qty == 0: 
                        katering = 'Sesuai'
                    
                    getres.append({
                        'code': line.get('code', False),
                        'in_qty': line.get('in_qty', False),
                        'out_qty': line.get('out_qty', False),
                        'totalqty': line.get('totalqty', False),
                        'inv_qty' : inv_qty,
                        'last_qty': last_qty,
                        'ope_qty': opening_qty,
                        'selish': inv_qty,
                        'katering': katering,
                       })
            
        return getres


report_sxw.report_sxw('report.stock.inventory.finish.goods.webkit', 'stock.inventory.finish.goods.wizard', 'addons/stock_inventory_in_out_report/report/stock_inventory_finishgoods_report.rml', parser=stock_inventory_finishgood_report,header="internal landscape")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
