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
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import netsvc

class res_branch(osv.Model):
    _name = 'res.branch'

    _columns = {
        'branch_code': fields.char('Branch Code', required=True),
        'name': fields.char('Name', required=True),
        'address': fields.text('Address', size=252),
        'telephone_no':fields.char("Telephone No"),
        'company_id': fields.many2one('res.company', 'Company', required=True),
    }

class res_users(osv.Model):
    _inherit = 'res.users'

    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
        'branch_ids': fields.many2many('res.branch', id1='user_id', id2='branch_id',string='Branch'),
    }


class res_company(osv.Model):
    _inherit = 'res.company'

    _columns = {
        'licence_no': fields.char('Import/Export Licence No.', required=True),
        'date_of_licence':fields.date('Date Of Licence', required=True),
        'npwp': fields.char('NPWP'),
    }


class product_product(osv.Model):
    _inherit='product.product'
    _columns = {
        'hscode':fields.char('HS Code')
    }

class sale_order(osv.Model):
    _inherit='sale.order'
    _columns = {
    }

class purchase_order(osv.Model):
    _inherit='purchase.order'
    _columns = {
    }

class account_voucher(osv.Model):
    _inherit = 'account.voucher'

    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }

class account_invoice(osv.Model):
     _inherit="account.invoice"
     _columns = {
        'destination_port':fields.char('Destination Port'),
        'customer_service_no':fields.char('Customer Service No'),
        'customer_good_export_no':fields.char('Customer Good Export No'),
    }
'''
class account_invoice_refund(osv.Model):
    _inherit = 'account.invoice.refund'

    def _get_invoice_refund_default_branch(self, cr, uid, context=None):
        if context.get('active_id'):
            ids = context.get('active_id')
            user_pool = self.pool.get('account.invoice')
            branch_id = user_pool.browse(cr, uid, ids, context=context).branch_id and user_pool.browse(cr, uid, ids, context=context).branch_id.id or False
            return branch_id

    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }

    _defaults = {
        'branch_id': _get_invoice_refund_default_branch,
    }

'''
class account_invoice_line(osv.Model):
     _inherit="account.invoice.line"
     _columns = {
        'kgm':fields.float('KGM')
    }

class crossovered_budget(osv.Model):
    _inherit = 'crossovered.budget'
    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }

class account_bank_statement(osv.Model):
    _inherit = 'account.bank.statement'
    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }

class sale_shop(osv.Model):
    _inherit = 'sale.shop'
    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch',required=True),
    }

class account_asset_asset(osv.Model):
    _inherit = 'account.asset.asset'
    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }

class procurement_order(osv.Model):
    _inherit = 'procurement.order'
    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }

    def create_procurement_purchase_order(self, cr, uid, procurement, po_vals, line_vals, context=None):
        po_vals.update({'order_line': [(0,0,line_vals)], 'branch_id': procurement.branch_id.id})
        return self.pool.get('purchase.order').create(cr, uid, po_vals, context=context)
        
class mrp_production(osv.Model):
    _inherit = 'mrp.production'
    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }
    
class account_invoice_refund(osv.osv_memory):
    _inherit = 'account.invoice.refund'
    _columns = {
    }

    def compute_refund(self, cr, uid, ids, mode='refund', context=None):
        """
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: the account invoice refund’s ID or list of IDs

        """
        inv_obj = self.pool.get('account.invoice')
        reconcile_obj = self.pool.get('account.move.reconcile')
        account_m_line_obj = self.pool.get('account.move.line')
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        wf_service = netsvc.LocalService('workflow')
        inv_tax_obj = self.pool.get('account.invoice.tax')
        inv_line_obj = self.pool.get('account.invoice.line')
        res_users_obj = self.pool.get('res.users')
        if context is None:
            context = {}

        for form in self.browse(cr, uid, ids, context=context):
            created_inv = []
            date = False
            period = False
            description = False
            company = res_users_obj.browse(cr, uid, uid, context=context).company_id
            journal_id = form.journal_id.id
            for inv in inv_obj.browse(cr, uid, context.get('active_ids'), context=context):
                if inv.state in ['draft', 'proforma2', 'cancel']:
                    raise osv.except_osv(_('Error!'), _('Cannot %s draft/proforma/cancel invoice.') % (mode))
                if inv.reconciled and mode in ('cancel', 'modify'):
                    raise osv.except_osv(_('Error!'), _('Cannot %s invoice which is already reconciled, invoice should be unreconciled first. You can only refund this invoice.') % (mode))
                if form.period.id:
                    period = form.period.id
                else:
                    period = inv.period_id and inv.period_id.id or False

                if not journal_id:
                    journal_id = inv.journal_id.id

                if form.date:
                    date = form.date
                    if not form.period.id:
                            cr.execute("select name from ir_model_fields \
                                            where model = 'account.period' \
                                            and name = 'company_id'")
                            result_query = cr.fetchone()
                            if result_query:
                                cr.execute("""select p.id from account_fiscalyear y, account_period p where y.id=p.fiscalyear_id \
                                    and date(%s) between p.date_start AND p.date_stop and y.company_id = %s limit 1""", (date, company.id,))
                            else:
                                cr.execute("""SELECT id
                                        from account_period where date(%s)
                                        between date_start AND  date_stop  \
                                        limit 1 """, (date,))
                            res = cr.fetchone()
                            if res:
                                period = res[0]
                else:
                    date = inv.date_invoice
                if form.description:
                    description = form.description
                else:
                    description = inv.name

                if not period:
                    raise osv.except_osv(_('Insufficient Data!'), \
                                            _('No period found on the invoice.'))

                refund_id = inv_obj.refund(cr, uid, [inv.id], date, period, description, journal_id, context=context)
                refund = inv_obj.browse(cr, uid, refund_id[0], context=context)
                inv_obj.write(cr, uid, [refund.id], {'date_due': date,
                                                'check_total': inv.check_total, 'branch_id': inv.branch_id.id})
                inv_obj.button_compute(cr, uid, refund_id)

                created_inv.append(refund_id[0])
                if mode in ('cancel', 'modify'):
                    movelines = inv.move_id.line_id
                    to_reconcile_ids = {}
                    for line in movelines:
                        if line.account_id.id == inv.account_id.id:
                            to_reconcile_ids.setdefault(line.account_id.id, []).append(line.id)
                        if line.reconcile_id:
                            line.reconcile_id.unlink()
                    wf_service.trg_validate(uid, 'account.invoice', \
                                        refund.id, 'invoice_open', cr)
                    refund = inv_obj.browse(cr, uid, refund_id[0], context=context)
                    for tmpline in  refund.move_id.line_id:
                        if tmpline.account_id.id == inv.account_id.id:
                            to_reconcile_ids[tmpline.account_id.id].append(tmpline.id)
                    for account in to_reconcile_ids:
                        account_m_line_obj.reconcile(cr, uid, to_reconcile_ids[account],
                                        writeoff_period_id=period,
                                        writeoff_journal_id = inv.journal_id.id,
                                        writeoff_acc_id=inv.account_id.id
                                        )
                    if mode == 'modify':
                        invoice = inv_obj.read(cr, uid, [inv.id],
                                    ['name', 'type', 'number', 'reference',
                                    'comment', 'date_due', 'partner_id',
                                    'partner_insite', 'partner_contact',
                                    'partner_ref', 'payment_term', 'account_id',
                                    'currency_id', 'invoice_line', 'tax_line',
                                    'journal_id', 'period_id'], context=context)
                        invoice = invoice[0]
                        del invoice['id']
                        invoice_lines = inv_line_obj.browse(cr, uid, invoice['invoice_line'], context=context)
                        invoice_lines = inv_obj._refund_cleanup_lines(cr, uid, invoice_lines, context=context)
                        tax_lines = inv_tax_obj.browse(cr, uid, invoice['tax_line'], context=context)
                        tax_lines = inv_obj._refund_cleanup_lines(cr, uid, tax_lines, context=context)
                        invoice.update({
                            'type': inv.type,
                            'date_invoice': date,
                            'state': 'draft',
                            'number': False,
                            'invoice_line': invoice_lines,
                            'tax_line': tax_lines,
                            'period_id': period,
                            'name': description
                        })
                        for field in ('partner_id', 'account_id', 'currency_id',
                                         'payment_term', 'journal_id'):
                                invoice[field] = invoice[field] and invoice[field][0]
                        inv_id = inv_obj.create(cr, uid, invoice, {})
                        if inv.payment_term.id:
                            data = inv_obj.onchange_payment_term_date_invoice(cr, uid, [inv_id], inv.payment_term.id, date)
                            if 'value' in data and data['value']:
                                inv_obj.write(cr, uid, [inv_id], data['value'])
                        created_inv.append(inv_id)
            xml_id = (inv.type == 'out_refund') and 'action_invoice_tree1' or \
                     (inv.type == 'in_refund') and 'action_invoice_tree2' or \
                     (inv.type == 'out_invoice') and 'action_invoice_tree3' or \
                     (inv.type == 'in_invoice') and 'action_invoice_tree4'
            result = mod_obj.get_object_reference(cr, uid, 'account', xml_id)
            id = result and result[1] or False
            result = act_obj.read(cr, uid, id, context=context)
            invoice_domain = eval(result['domain'])
            invoice_domain.append(('id', 'in', created_inv))
            result['domain'] = invoice_domain
            return result
    
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
