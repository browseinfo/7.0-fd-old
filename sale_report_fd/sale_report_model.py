# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://browseinfo.in>).
#

##############################################################################
from datetime import datetime, timedelta
import time
import openerp.exceptions
from openerp import netsvc
from openerp import pooler
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
from dateutil.relativedelta import relativedelta

class sale_order(osv.osv):
    _inherit = "sale.order"
    _columns = {
        'invoice_no': fields.char('Invoice No'),
        }

class sale_order_line(osv.osv):
    _inherit = "sale.order.line"
    _columns = {
        'customer_po': fields.char('Customer PO'),
        }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

