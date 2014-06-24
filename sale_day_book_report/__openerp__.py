# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-Today BrowseInfo (<http://www.browseinfo.in>).
#
##############################################################################

{
    'name' : "Sale Day Book Report",
	'version' : "7.0",
	'author' : "BrowseInfo",
	'depends' : ['sale','report_webkit','account'],
	'website': 'http://www.browseinfo.in',
	'data' : ['wizard/sale_daybook_wizard_view.xml',
	          'report/sale_daybook_report.xml',
	         ],
	'demo' : [],
	'installable': True,
	'auto_install': False
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

