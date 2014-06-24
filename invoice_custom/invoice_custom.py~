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

from openerp.osv import osv, fields
from openerp.tools.translate import _
import time
import openerp.addons.decimal_precision as dp

class account_invoice(osv.Model):
    _inherit = 'account.invoice'
    
    _columns = {
        'custom_invoice_no': fields.char('Custom Invoice No.'),
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
        'shipment_date': fields.date('Shipment Date'),
        'custom_date': fields.date('Custom Date'),
        'nomor_seri': fields.char('Nomor Seri Faktur Pajak'),
        'exchange_ref': fields.char('Berdasarkan KMK No.'),
        'exchange_date': fields.date('Exchange Date'),
        'exchange_rate': fields.float('Exchange Rate'),
    }
    
    _defaults = {
        'shipment_date': time.strftime('%Y-%m-%d'),
        'custom_date': time.strftime('%Y-%m-%d'),
    }

    def invoice_pay_customer(self, cr, uid, ids, context=None):
        result = super(account_invoice, self).invoice_pay_customer(cr, uid, ids, context=context)
        inv = self.pool.get('account.invoice').browse(cr, uid, ids[0], context=context)
        result.get('context').update({'default_branch_id': inv.branch_id.id})
        return result

#     def invoice_refund(self, cr, uid, ids, context=None):
#         data_refund = self.read(cr, uid, ids, ['filter_refund'],context=context)[0]['filter_refund']
#         return self.compute_refund(cr, uid, ids, data_refund, context=context)
# 
# 
#     def compute_refund(self, cr, uid, ids, mode='refund', context=None):
#         print "in compute refunddddddddddd"
#         inv_obj = self.pool.get('account.invoice')
#         reconcile_obj = self.pool.get('account.move.reconcile')
#         account_m_line_obj = self.pool.get('account.move.line')
#         mod_obj = self.pool.get('ir.model.data')
#         act_obj = self.pool.get('ir.actions.act_window')
#         wf_service = netsvc.LocalService('workflow')
#         inv_tax_obj = self.pool.get('account.invoice.tax')
#         inv_line_obj = self.pool.get('account.invoice.line')
#         res_users_obj = self.pool.get('res.users')
#         if context is None:
#             context = {}
#         for form in self.browse(cr, uid, ids, context=context):
#             created_inv = []
#             date = False
#             period = False
#             description = False
#             company = res_users_obj.browse(cr, uid, uid, context=context).company_id
#             journal_id = form.journal_id.id
#             branch_id = form.branch_id.id
#             print "branch_idbranch_idbranch_idbranch_id", branch_id
#             for inv in inv_obj.browse(cr, uid, context.get('active_ids'), context=context):
#                 if inv.state in ['draft', 'proforma2', 'cancel']:
#                     raise osv.except_osv(_('Error!'), _('Cannot %s draft/proforma/cancel invoice.') % (mode))
#                 if inv.reconciled and mode in ('cancel', 'modify'):
#                     raise osv.except_osv(_('Error!'), _('Cannot %s invoice which is already reconciled, invoice should be unreconciled first. You can only refund this invoice.') % (mode))
#                 if form.period.id:
#                     period = form.period.id
#                 else:
#                     period = inv.period_id and inv.period_id.id or False
#                 if form.branch_id.id:
#                     branch_id = inv.branch_id.id
#                     print "branch_idddddddddddd  of form", branch_id
#                 if not journal_id:
#                     journal_id = inv.journal_id.id
# 
#                 if form.date:
#                     date = form.date
#                     if not form.period.id:
#                             cr.execute("select name from ir_model_fields \
#                                             where model = 'account.period' \
#                                             and name = 'company_id'")
#                             result_query = cr.fetchone()
#                             if result_query:
#                                 cr.execute("""select p.id from account_fiscalyear y, account_period p where y.id=p.fiscalyear_id \
#                                     and date(%s) between p.date_start AND p.date_stop and y.company_id = %s limit 1""", (date, company.id,))
#                             else:
#                                 cr.execute("""SELECT id
#                                         from account_period where date(%s)
#                                         between date_start AND  date_stop  \
#                                         limit 1 """, (date,))
#                             res = cr.fetchone()
#                             if res:
#                                 period = res[0]
#                 else:
#                     date = inv.date_invoice
#                 if form.description:
#                     description = form.description
#                 else:
#                     description = inv.name
# 
#                 if not period:
#                     raise osv.except_osv(_('Insufficient Data!'), \
#                                             _('No period found on the invoice.'))
# 
#                 refund_id = inv_obj.refund(cr, uid, [inv.id], date, period, description, journal_id, branch_id, context=context)
#                 refund = inv_obj.browse(cr, uid, refund_id[0], context=context)
#                 inv_obj.write(cr, uid, [refund.id], {'date_due': date,
#                                                 'check_total': inv.check_total})
#                 inv_obj.button_compute(cr, uid, refund_id)
# 
#                 created_inv.append(refund_id[0])
#                 if mode in ('cancel', 'modify'):
#                     movelines = inv.move_id.line_id
#                     to_reconcile_ids = {}
#                     for line in movelines:
#                         if line.account_id.id == inv.account_id.id:
#                             to_reconcile_ids[line.account_id.id] = [line.id]
#                         if type(line.reconcile_id) != osv.orm.browse_null:
#                             reconcile_obj.unlink(cr, uid, line.reconcile_id.id)
#                     wf_service.trg_validate(uid, 'account.invoice', \
#                                         refund.id, 'invoice_open', cr)
#                     refund = inv_obj.browse(cr, uid, refund_id[0], context=context)
#                     for tmpline in  refund.move_id.line_id:
#                         if tmpline.account_id.id == inv.account_id.id:
#                             to_reconcile_ids[tmpline.account_id.id].append(tmpline.id)
#                     for account in to_reconcile_ids:
#                         account_m_line_obj.reconcile(cr, uid, to_reconcile_ids[account],
#                                         writeoff_period_id=period,
#                                         writeoff_journal_id = inv.journal_id.id,
#                                         writeoff_branch_id = inv.branch_id.id,
#                                         writeoff_acc_id=inv.account_id.id
#                                         )
#                     if mode == 'modify':
#                         invoice = inv_obj.read(cr, uid, [inv.id],
#                                     ['name', 'type', 'number', 'reference',
#                                     'comment', 'date_due', 'partner_id',
#                                     'partner_insite', 'partner_contact',
#                                     'partner_ref', 'payment_term', 'account_id',
#                                     'currency_id', 'invoice_line', 'tax_line',
#                                     'journal_id','branch_id', 'period_id'], context=context)
#                         invoice = invoice[0]
#                         del invoice['id']
#                         invoice_lines = inv_line_obj.browse(cr, uid, invoice['invoice_line'], context=context)
#                         invoice_lines = inv_obj._refund_cleanup_lines(cr, uid, invoice_lines, context=context)
#                         tax_lines = inv_tax_obj.browse(cr, uid, invoice['tax_line'], context=context)
#                         tax_lines = inv_obj._refund_cleanup_lines(cr, uid, tax_lines, context=context)
#                         invoice.update({
#                             'type': inv.type,
#                             'date_invoice': date,
#                             'state': 'draft',
#                             'number': False,
#                             'invoice_line': invoice_lines,
#                             'tax_line': tax_lines,
#                             'period_id': period,
#                             'name': description
#                         })
#                         print "invoice==============", invoice
#                         for field in ('partner_id', 'account_id', 'currency_id',
#                                          'payment_term', 'journal_id', 'branch_id'):
#                                 invoice[field] = invoice[field] and invoice[field][0]
#                         inv_id = inv_obj.create(cr, uid, invoice, {})
#                         if inv.payment_term.id:
#                             data = inv_obj.onchange_payment_term_date_invoice(cr, uid, [inv_id], inv.payment_term.id, date)
#                             if 'value' in data and data['value']:
#                                 inv_obj.write(cr, uid, [inv_id], data['value'])
#                         created_inv.append(inv_id)
#             xml_id = (inv.type == 'out_refund') and 'action_invoice_tree1' or \
#                      (inv.type == 'in_refund') and 'action_invoice_tree2' or \
#                      (inv.type == 'out_invoice') and 'action_invoice_tree3' or \
#                      (inv.type == 'in_invoice') and 'action_invoice_tree4'
#             result = mod_obj.get_object_reference(cr, uid, 'account', xml_id)
#             id = result and result[1] or False
#             result = act_obj.read(cr, uid, id, context=context)
#             invoice_domain = eval(result['domain'])
#             invoice_domain.append(('id', 'in', created_inv))
#             result['domain'] = invoice_domain
#             return result
#  
#  
#     def refund(self, cr, uid, ids, date=None, period_id=None, description=None, journal_id=None, branch_id=None, context=None):
#         new_ids = []
#         for invoice in self.browse(cr, uid, ids, context=context):
#             invoice = self._prepare_refund(cr, uid, invoice,
#                                                 date=date,
#                                                 period_id=period_id,
#                                                 description=description,
#                                                 journal_id=journal_id,
#                                                 branch_id=branch_id,
#                                                 context=context)
#            # create the new invoice
#             new_ids.append(self.create(cr, uid, invoice, context=context))
# 
#         return new_ids
#  
#  
#     def _prepare_refund(self, cr, uid, invoice, date=None, period_id=None, description=None, journal_id=None,branch_id=None, context=None):
#         obj_journal = self.pool.get('account.journal')
#         type_dict = {
#             'out_invoice': 'out_refund', # Customer Invoice
#             'in_invoice': 'in_refund',   # Supplier Invoice
#             'out_refund': 'out_invoice', # Customer Refund
#             'in_refund': 'in_invoice',   # Supplier Refund
#         }
#         invoice_data = {}
#         for field in ['name', 'reference', 'comment', 'date_due', 'partner_id', 'company_id',
#                 'account_id', 'currency_id', 'payment_term', 'user_id', 'fiscal_position']:
#             if invoice._all_columns[field].column._type == 'many2one':
#                 invoice_data[field] = invoice[field].id
#             else:
#                 invoice_data[field] = invoice[field] if invoice[field] else False
# 
#         invoice_lines = self._refund_cleanup_lines(cr, uid, invoice.invoice_line, context=context)
# 
#         tax_lines = filter(lambda l: l['manual'], invoice.tax_line)
#         tax_lines = self._refund_cleanup_lines(cr, uid, tax_lines, context=context)
#         print "valuessssssssssssssssssss", branch_id
#         if branch_id:
#             refund_branch_id = [branch_id]
#             print "refund_branch_id", refund_branch_id, branch_id
#         if journal_id:
#             refund_journal_ids = [journal_id]
#         elif invoice['type'] == 'in_invoice':
#             refund_journal_ids = obj_journal.search(cr, uid, [('type','=','purchase_refund')], context=context)
#         else:
#             refund_journal_ids = obj_journal.search(cr, uid, [('type','=','sale_refund')], context=context)
#         if not date:
#             date = time.strftime('%Y-%m-%d')
#         invoice_data.update({
#                 'type': type_dict[invoice['type']],
#                 'date_invoice': date,
#                 'state': 'draft',
#                 'number': False,
#                 'invoice_line': invoice_lines,
#                 'tax_line': tax_lines,
#                 'journal_id': refund_journal_ids and refund_journal_ids[0] or False,
#                 'branch_id': refund_branch_id and refund_branch_id[0] or False,
#         })
#         if period_id:
#             invoice_data['period_id'] = period_id
#         if description:
#             invoice_data['name'] = description
#         return invoice_data   
     
class res_partner(osv.Model):
    _inherit = 'res.partner'
    
    _columns = {
        'npwp': fields.char('NPWP'),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
