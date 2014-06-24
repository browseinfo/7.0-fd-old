# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-Today BrowseInfo (<http://www.browseinfo.in>).
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
		'old_price' : fields.float('Old Price', digits_compute=dp.get_precision('Old Price')),
		'new_price': fields.float('New Price', digits_compute=dp.get_precision('New Price')),
        'date_ext':fields.date("Modified Date", readonly=True),
        'currency_id': fields.many2one('res.currency', 'Currency'),
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
 		if vals.get('product_id'):
 			product = vals.get('product_id')
 			oldprice = product_obj.browse(cr, uid, product, context=context).standard_price
			newprice = vals.get('price_unit')
			order_id = vals.get('order_id')
			current_obj = self.pool.get('purchase.order').browse(cr, uid, [order_id], context=context)[0]
 			price_line = {
		            'product_id': product,
		            'old_price' : oldprice,
		            'new_price' : newprice,
		            'currency_id': current_obj.pricelist_id.currency_id.id,
		        }
	        if vals.get('price_unit') != oldprice:
				product_price.create(cr,uid,price_line, context=context)
				product_obj.write(cr, uid, product, {'standard_price': vals.get('price_unit')})
 		return res

 	def write(self, cr, uid, ids, vals, context=None):
 		res = super(purchase_order_line, self).write(cr, uid, ids, vals, context=context)
 		price_line = {}
 		for line_product in self.pool.get('purchase.order.line').browse(cr, uid, ids, context=context):
 			oldprice = line_product.product_id.standard_price
 			product_obj = self.pool.get('product.product')
 			product_price = self.pool.get('product.product.price')
			order_id = vals.get('order_id')
			line_obj = self.browse(cr, uid, ids, context)
			current_obj = self.pool.get('purchase.order').browse(cr, uid, [line_obj[0].order_id.id], context=context)[0]
			if line_product.product_id and vals.get('price_unit'):
				newprice = vals.get('price_unit')
				price_line = {
					'product_id': line_product.product_id.id,
					'old_price' : oldprice,
					'new_price' : newprice,
					'currency_id': current_obj.pricelist_id.currency_id.id,
				}
				if vals.get('price_unit') != oldprice:
					product_price.create(cr,uid,price_line, context=context)
					product_obj.write(cr, uid, line_product.product_id.id, {'standard_price': vals.get('price_unit')})

 		return res

purchase_order_line()
