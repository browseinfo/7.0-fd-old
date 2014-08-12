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

from osv import osv,fields
from openerp.tools.translate import _
from datetime import datetime, date
import openerp.addons.decimal_precision as dp

class product_product_price(osv.osv):
	_name = "product.product.price"
	_description = "Product Price"

	def create(self, cr, uid, vals, context=None):
		if not vals.get('date_ext'):
			today_date = datetime.now()
			vals['date_ext'] = today_date
		return super(product_product_price, self).create(cr, uid, vals, context=context)

	_columns = {
        'product_id': fields.many2one('product.product', 'Product'),
		'old_price' : fields.float('Product Old Price', digits_compute=dp.get_precision('Old Price')),
		'pur_price': fields.float('Purchase Price', digits_compute=dp.get_precision('Purchase Price')),
		'new_price': fields.float('Product New Price', digits_compute=dp.get_precision('New Price')),
        'date_ext':fields.date("Modified Date", readonly=True),
        'currency_id': fields.many2one('res.currency', 'Purchase Currency'),
        'product_currency_id': fields.many2one('res.currency', 'Product Currency'),
	}

product_product_price()

class product_product(osv.osv):
	_inherit = 'product.product'
	_columns = {
		'product_price_ids': fields.one2many('product.product.price', 'product_id','Price',readonly=True),
	}

product_product()

class purchase_order_line(osv.osv):
	_inherit = 'purchase.order.line'

 	def create(self, cr, uid, vals, context=None):
 		res = super(purchase_order_line, self).create(cr, uid, vals, context=context)
  		product_obj = self.pool.get('product.product')
 		product_price = self.pool.get('product.product.price')
 		res_currency = self.pool.get('res.currency')
 		cur_obj = self.pool.get('res.currency.rate')
 		if vals.get('product_id'):
 			from_datelist= []
 			to_datelist= []
 			product = vals.get('product_id')
 			product_id = product_obj.browse(cr, uid, product, context=context)
 			oldprice = product_id.standard_price
			newprice = vals.get('price_unit')
			order_id = vals.get('order_id')
			purchase_obj = self.pool.get('purchase.order').browse(cr, uid, [order_id], context=context)[0]

 			for from_curr_obj in res_currency.browse(cr, uid, [purchase_obj.pricelist_id.currency_id.id]):
				for from_rate_obj in from_curr_obj.rate_ids:
					from_datelist.append(from_rate_obj.name)
 			from_get_datetime = lambda s: datetime.strptime(s, "%Y-%m-%d")
 			from_base = from_get_datetime(purchase_obj.date_order)
 			from_later = filter(lambda d: from_get_datetime(d) <= from_base, from_datelist)
 			from_closest_date = max(from_later, key = lambda d: from_get_datetime(d))
            
 			from_rate_search = cur_obj.search(cr, uid, [('name', '=', from_closest_date), ('currency_id', '=', purchase_obj.pricelist_id.currency_id.id)])[0]
 			from_rate_browse = cur_obj.browse(cr, uid, from_rate_search)
 			from_rate = from_rate_browse.rate    
 			
 			for to_curr_obj in res_currency.browse(cr, uid, [product_id.pur_cur_id.id]):
				for to_rate_obj in to_curr_obj.rate_ids:
					to_datelist.append(to_rate_obj.name)
 			to_get_datetime = lambda s: datetime.strptime(s, "%Y-%m-%d")
 			to_base = to_get_datetime(purchase_obj.date_order)
 			to_later = filter(lambda d: to_get_datetime(d) <= to_base, to_datelist)
 			to_closest_date = max(to_later, key = lambda d: to_get_datetime(d))
			
 			to_rate_search = cur_obj.search(cr, uid, [('name', '=', to_closest_date), ('currency_id', '=', product_id.pur_cur_id.id)])[0]
 			to_rate_browse = cur_obj.browse(cr, uid, to_rate_search)
 			to_rate = to_rate_browse.rate

			if product_id.pur_cur_id != purchase_obj.pricelist_id.currency_id:
 				if product_id.pur_cur_id != purchase_obj.company_id.currency_id: #product currency not company currency rate
 					if from_rate > to_rate:
	 					if product_id.standard_price != round(((vals.get('price_unit') / from_rate) * to_rate), 2):
	 						product_obj.write(cr, uid, product, {'standard_price': vals.get('price_unit') / from_rate})
				 			price_line = {
								'product_id': product,
								'old_price' : oldprice,
								'new_price' : vals.get('price_unit') / from_rate,
								'pur_price' : newprice,
								'currency_id': purchase_obj.pricelist_id.currency_id.id,
								'product_currency_id': product_id.pur_cur_id.id,
							}
							product_price.create(cr,uid,price_line, context=context)
					elif to_rate > from_rate:
						value = round(((vals.get('price_unit') / from_rate) * to_rate),2)
						if product_id.standard_price != round(value):
							product_obj.write(cr, uid, product, {'standard_price': vals.get('price_unit') / from_rate})
							price_line = {
								'product_id': product,
								'old_price' : oldprice,
								'new_price' : vals.get('price_unit') / from_rate,
								'pur_price' : newprice,
								'currency_id': purchase_obj.pricelist_id.currency_id.id,
								'product_currency_id': product_id.pur_cur_id.id,
							}
							product_price.create(cr,uid,price_line, context=context)
				else:
					if from_rate > to_rate:
	 					if product_id.standard_price != round(((vals.get('price_unit') / from_rate) * to_rate), 2):
	 						product_obj.write(cr, uid, product, {'standard_price': vals.get('price_unit') / from_rate})
	 						price_line = {
								'product_id': product,
								'old_price' : oldprice,
								'new_price' : vals.get('price_unit') / from_rate,
								'pur_price' : newprice,
								'currency_id': purchase_obj.pricelist_id.currency_id.id,
								'product_currency_id': product_id.pur_cur_id.id,
							}
							product_price.create(cr,uid,price_line, context=context)
					elif to_rate > from_rate:
						value = round(((vals.get('price_unit') / from_rate) * to_rate),2)
						if product_id.standard_price != round(value):
							product_obj.write(cr, uid, product, {'standard_price': vals.get('price_unit') / from_rate})
							price_line = {
								'product_id': product,
								'old_price' : oldprice,
								'new_price' : vals.get('price_unit') / from_rate,
								'pur_price' : newprice,
								'currency_id': purchase_obj.pricelist_id.currency_id.id,
								'product_currency_id': product_id.pur_cur_id.id,
							}
							product_price.create(cr,uid,price_line, context=context)

 		return res
 		

 	def write(self, cr, uid, ids, vals, context=None):
 		res = super(purchase_order_line, self).write(cr, uid, ids, vals, context=context)
  		product_obj = self.pool.get('product.product')
 		product_price = self.pool.get('product.product.price')
 		res_currency = self.pool.get('res.currency')
 		cur_obj = self.pool.get('res.currency.rate')
 		
 		purchase_line_obj = self.browse(cr, uid, ids[0], context=context)
 		
 		if purchase_line_obj.product_id:
 			from_datelist= []
 			to_datelist= []
 			product = purchase_line_obj.product_id.id
 			product_id = product_obj.browse(cr, uid, [product][0], context=context)
 			oldprice = product_id.standard_price
			newprice = purchase_line_obj.price_unit
			order_id = purchase_line_obj.order_id.id
			purchase_obj = self.pool.get('purchase.order').browse(cr, uid, [order_id], context=context)[0]
 			
 			for from_curr_obj in res_currency.browse(cr, uid, [purchase_obj.pricelist_id.currency_id.id]):
				for from_rate_obj in from_curr_obj.rate_ids:
					from_datelist.append(from_rate_obj.name)
 			from_get_datetime = lambda s: datetime.strptime(s, "%Y-%m-%d")
 			from_base = from_get_datetime(purchase_obj.date_order)
 			from_later = filter(lambda d: from_get_datetime(d) <= from_base, from_datelist)
 			from_closest_date = max(from_later, key = lambda d: from_get_datetime(d))
            
 			from_rate_search = cur_obj.search(cr, uid, [('name', '=', from_closest_date), ('currency_id', '=', purchase_obj.pricelist_id.currency_id.id)])[0]
 			from_rate_browse = cur_obj.browse(cr, uid, from_rate_search)
 			from_rate = from_rate_browse.rate    
 			
 			for to_curr_obj in res_currency.browse(cr, uid, [product_id.pur_cur_id.id]):
				for to_rate_obj in to_curr_obj.rate_ids:
					to_datelist.append(to_rate_obj.name)
 			to_get_datetime = lambda s: datetime.strptime(s, "%Y-%m-%d")
 			to_base = to_get_datetime(purchase_obj.date_order)
 			to_later = filter(lambda d: to_get_datetime(d) <= to_base, to_datelist)
 			to_closest_date = max(to_later, key = lambda d: to_get_datetime(d))
			
 			to_rate_search = cur_obj.search(cr, uid, [('name', '=', to_closest_date), ('currency_id', '=', product_id.pur_cur_id.id)])[0]
 			to_rate_browse = cur_obj.browse(cr, uid, to_rate_search)
 			to_rate = to_rate_browse.rate

			if product_id.pur_cur_id != purchase_obj.pricelist_id.currency_id:
 				if product_id.pur_cur_id != purchase_obj.company_id.currency_id: #product currency not company currency rate
 					if from_rate > to_rate:
	 					if product_id.standard_price != round(((vals.get('price_unit') / from_rate) * to_rate), 2):
	 						product_obj.write(cr, uid, product, {'standard_price': vals.get('price_unit') / from_rate})
	 						price_line = {
								'product_id': product,
								'old_price' : oldprice,
								'new_price' : vals.get('price_unit') / from_rate,
								'pur_price' : newprice,
								'currency_id': purchase_obj.pricelist_id.currency_id.id,
								'product_currency_id': product_id.pur_cur_id.id,
							}
							product_price.create(cr,uid,price_line, context=context)
					elif to_rate > from_rate:
						value = round(((vals.get('price_unit') / from_rate) * to_rate),2)
						if product_id.standard_price != round(value):
							product_obj.write(cr, uid, product, {'standard_price': vals.get('price_unit') / from_rate})
							price_line = {
								'product_id': product,
								'old_price' : oldprice,
								'new_price' : vals.get('price_unit') / from_rate,
								'pur_price' : newprice,
								'currency_id': purchase_obj.pricelist_id.currency_id.id,
								'product_currency_id': product_id.pur_cur_id.id,
							}
							product_price.create(cr,uid,price_line, context=context)
				else:
					if from_rate > to_rate:
	 					if product_id.standard_price != round(((vals.get('price_unit') / from_rate) * to_rate), 2):
	 						product_obj.write(cr, uid, product, {'standard_price': vals.get('price_unit') / from_rate})
	 						price_line = {
								'product_id': product,
								'old_price' : oldprice,
								'new_price' : vals.get('price_unit') / from_rate,
								'pur_price' : newprice,
								'currency_id': purchase_obj.pricelist_id.currency_id.id,
								'product_currency_id': product_id.pur_cur_id.id,
							}
							product_price.create(cr,uid,price_line, context=context)
					elif to_rate > from_rate:
						value = round(((vals.get('price_unit') / from_rate) * to_rate),2)
						if product_id.standard_price != round(value):
							product_obj.write(cr, uid, product, {'standard_price': vals.get('price_unit') / from_rate})
							price_line = {
								'product_id': product,
								'old_price' : oldprice,
								'new_price' : vals.get('price_unit') / from_rate,
								'pur_price' : newprice,
								'currency_id': purchase_obj.pricelist_id.currency_id.id,
								'product_currency_id': product_id.pur_cur_id.id,
							}
							product_price.create(cr,uid,price_line, context=context)

 		return res



purchase_order_line()
