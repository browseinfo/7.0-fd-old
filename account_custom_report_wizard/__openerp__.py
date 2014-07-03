# -*- coding: utf-8 -*-
##############################################################################
#
#    Sales and Account Invoice Discount Management
#    Copyright (C) 2013-2014 BrowseInfo(<http://www.browseinfo.in>).
#    $autor:
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
##############################################################################

{
    'name' : "Account Custom Report Wizard",
	'version' : "1.0",
	'author' : "BrowseInfo",
	'description' : 'This module to print CONTOH EKSPOR REPORT and CONTOH IMPOR REPORT ',
	'category' : "Account Custom Report Wizard",
	'depends' : ['account','company_extended', 'report_webkit'],
	'website': 'http://www.browseinfo.in',
	'data' : [
            'webkit_data.xml',
	        'wizard/account_report_wizard_view.xml',
            'account_impor_report.xml',
	         ],
	'demo' : [],
	'installable': True,
	'auto_install': False
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

