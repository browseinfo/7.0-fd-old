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
{
	'name' : "Stock Inventory in-out Report",
	'version' : "1.0",
	'author' : "BrowseInfo",
	'description' : 'Stock Inventory in-out Report',
	'category' : "Stock",
	'depends' : ['product','stock', 'report_webkit','product_extended','company_extended','account'],
	'website': 'http://www.browseinfo.in',
	'data' : ['wizard/stock_inventory_in_out_wizard_view.xml',
				'stock_inventory_in_out_report.xml',
			],
	'demo' : [],
	'installable': True,
	'auto_install': False
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
