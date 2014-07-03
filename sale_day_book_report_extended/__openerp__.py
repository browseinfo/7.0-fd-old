# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-Today BrowseInfo (<http://www.browseinfo.in>).
#
##############################################################################

{
    'name' : "Sales Day Book Report",
	'version' : "7.0",
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

