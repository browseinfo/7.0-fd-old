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
    'name' : "Sales Day Book Report",
	'version' : "1.0",
	'author' : "BrowseInfo",
	'description' : 'This module help to print Sales Day Book Report',
	'depends' : ['sale','company_extended','invoice_custom','report_webkit','sale_day_book_report'],
	'website': 'http://www.browseinfo.in',
	'data' : ['wizard/sales_daybook_report_wizard_view.xml',
	          'report/sales_day_book_report.xml'
	         ],
	'demo' : [],
	'installable': True,
	'auto_install': False
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

