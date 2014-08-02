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
import datetime
from openerp.osv import fields, osv
from openerp.tools.translate import _

class stock_inventory_in_out_wizard(osv.osv_memory):
    _name = 'stock.inventory.in.out.wizard'
    _columns={
        'startdtae':fields.date("Start Date",required=True),
        'enddtae':fields.date("End Date",required=True),
        'branch_id': fields.many2one('res.branch', 'Branch',required=True),
    }	


    def print_report(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, [], context=context)[0]
        datas = {
            'ids': [data.get('id')],
            'model': 'stock.inventory.in.out.wizard',
            'form': data
            }
        self_browse = self.browse(cr, uid, ids)
        date = self_browse[0].startdtae
        d = datetime.datetime.strptime(date, '%Y-%m-%d')
        month = d.strftime('%b')
        year = d.strftime('%y')
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'stock.inventory.in.out.report.webkit',
            'datas': datas,
            'name': 'LAPORAN BULANAN' + ' ' + self_browse[0].branch_id.branch_code + ' ' +month+ '-'+ year+'(MUTASI BRG)'
            }    
    
stock_inventory_in_out_wizard()
    


class stock_inventory_wizard(osv.osv_memory):
    _name = 'stock.inventory.wizard'
    _columns={
        'startdtae':fields.date("Start Date",required=True),
        'enddtae':fields.date("End Date",required=True),
        'branch_id': fields.many2one('res.branch', 'Branch',required=True),
    }	

    def print_asset_report(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, [], context=context)[0]
        datas = {
            'ids': [data.get('id')],
            'model': 'stock.inventory.wizard',
            'form': data
            }
        self_browse = self.browse(cr, uid, ids)
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'stock.inventory.report.webkit',
            'datas': datas,
            'name': 'CNTH LAP 4 BLNAN' + ' '+ self_browse[0].branch_id.branch_code +'(MUTASI MESIN)'
            }    
    
stock_inventory_wizard()




class stock_inventory_scrap_location_wizard(osv.osv_memory):
    _name = 'stock.inventory.scrap.location.wizard'
    _columns={
        'startdtae':fields.date("Start Date",required=True),
        'enddtae':fields.date("End Date",required=True),
        'branch_id': fields.many2one('res.branch', 'Branch',required=True),
    }    


    def print_asset_report(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, [], context=context)[0]
        datas = {
            'ids': [data.get('id')],
            'model': 'stock.inventory.scrap.location.wizard',
            'form': data
            }
        self_browse = self.browse(cr, uid, ids)
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'stock.inventory.scrap.location.webkit',
            'datas': datas,
            'name': 'CNTH LAP 4 BLNAN' + ' '+ self_browse[0].branch_id.branch_code +'(BRG SCRAP)'
            }    
    
stock_inventory_scrap_location_wizard()
    


class stock_inventory_raw_material_wizard(osv.osv_memory):
    _name = 'stock.inventory.raw.material.wizard'
    _columns={
        'startdtae':fields.date("Start Date",required=True),
        'enddtae':fields.date("End Date",required=True),
        'branch_id': fields.many2one('res.branch', 'Branch',required=True),
    }    


    def print_raw_material_report(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, [], context=context)[0]
        datas = {
            'ids': [data.get('id')],
            'model': 'stock.inventory.raw.material.wizard',
            'form': data
            }
        self_browse = self.browse(cr, uid, ids)
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'stock.inventory.raw.material.webkit',
            'datas': datas,
            'name': 'CNTH LAP 4 BLNAN' + ' '+ self_browse[0].branch_id.branch_code +'(BAHAN BAKU)'
            }    
    
stock_inventory_raw_material_wizard()


class stock_inventory_finish_goods_wizard(osv.osv_memory):
    _name = 'stock.inventory.finish.goods.wizard'
    _columns={
        'startdtae':fields.date("Start Date",required=True),
        'enddtae':fields.date("End Date",required=True),
        'branch_id': fields.many2one('res.branch', 'Branch',required=True),
    }    


    def print_raw_material_report(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, [], context=context)[0]
        datas = {
            'ids': [data.get('id')],
            'model': 'stock.inventory.finish.goods.wizard',
            'form': data
            }
        self_browse = self.browse(cr, uid, ids)
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'stock.inventory.finish.goods.webkit',
            'datas': datas,
            'name': 'CNTH LAP 4 BLNAN' + ' '+ self_browse[0].branch_id.branch_code +'(BRG JADI)'
            }    
    
stock_inventory_finish_goods_wizard()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
