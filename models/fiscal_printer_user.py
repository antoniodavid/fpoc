# -*- coding: utf-8 -*-
from odoo import netsvc
from odoo import osv, fields, api, models
from odoo.tools.translate import _


class FiscalPrinterConfiguration(models.Model):
    """
    This configuration is independent of the printer, is related to point of sale.

    Must be used as entry for diferent calls:

    open_fiscal_ticket
    add_fiscal_item
    close_fiscal_ticket
    """

    _name = 'fpoc.configuration'
    _description = 'Fiscal printer configuration'

    def _get_type(self):
        return []

    def _get_protocol(self):
        return []

    name = fields.Char(string='Name')
    type = fields.Selection(selection=_get_type, string='Type')
    protocol = fields.Char('Protocol')
    user_ids = fields.One2many('fpoc.user', 'fiscal_printer_configuration_id', 'User entities')

    _sql_constraints = [
        ('unique_name', 'UNIQUE (name)', 'Name has to be unique!')
    ]

    @api.onchange('type')
    def onchange_type(self):
        return {'value': {'protocol': None}}

    def toDict(self):
        return {id: {} for id in self.ids}

    def solve_status(self, status):
        """
        This function compute paper_state, fiscal_state and printer_state for this configuration type.
        """
        return status


class FiscalPrinterUser(models.AbstractModel):
    """
    Fiscal printer user is a Abstract class to be used by the owner of the fiscal printer.
    The entity responsable to print tickets must inheret this class.
    """

    def _get_fp_state(self):
        pass

    #     context = self.env.context or {}
    #     r = {}
    #     for fpu in self:
    #         r[fpu.id] = dict(zip(fields_name, ['unknown'] * len(fields_name)))
    #         # import pdb;pdb.set_trace()
    #
    #         if not fpu.fiscal_printer_id:
    #             continue
    #
    #         res = fpu.fiscal_printer_id.get_state()
    #         res = fpu.fiscal_printer_configuration_id.solve_status(res)[fpu.fiscal_printer_id.id]
    #
    #         if res:
    #             r[fpu.id]['fiscal_printer_paper_state'] = res['paper_state'] if 'paper_state' in res else 'unknown'
    #             r[fpu.id]['fiscal_printer_fiscal_state'] = res['fiscal_state'] if 'fiscal_state' in res else 'unknown'
    #             r[fpu.id]['fiscal_printer_state'] = res['printer_state'] if 'printer_state' in res else 'unknown'
    #
    #     return r

    _name = 'fpoc.user'
    _description = 'Fiscal printer user'

    fiscal_printer_id = fields.Many2one('fpoc.fiscal_printer', 'Fiscal Printer')
    fiscal_printer_configuration_id = fields.Many2one('fpoc.configuration', 'Configuration')
    fiscal_printer_anon_partner_id = fields.Many2one('res.partner', 'Anonymous partner')
    fiscal_printer_fiscal_state = fields.Selection(
        compute='_get_fp_state', string='Printer Fiscal State',
        selection=[('open', 'Open'), ('close', 'Closed'), ('unknown', 'Unknown'),
                   ], help="Fiscal state of the printer"
    )
    fiscal_printer_paper_state = fields.Selection(
        compute='_get_fp_state', string='Printer Paper State',
        selection=[
            ('ok', 'Ok'),
            ('low', 'Low Paper'),
            ('none', 'No Paper'),
            ('unknown', 'Unknown'),
        ], help="Page state of the printer"
    )
    fiscal_printer_state = fields.Selection(
        compute='_get_fp_state', string='Printer State',
        selection=[
            ('ready', 'Ready'),
            ('deviceopen', 'Printer Open'),
            ('onerror', 'On Error'),
            ('offline', 'Offline'),
            ('nomemory', 'No memory'),
            ('printing', 'Printing'),
            ('disabled', 'Disabled'),
            ('unknown', 'Unknown'),
        ], help="Check printer status."
    )

    def make_fiscal_ticket(self):
        """
        Create Fiscal Ticket.
        """
        pass
        # fp_obj = self.pool.get('fpoc.fiscal_printer')
        # context = context or {}
        # r = {}
        # for usr in self.browse(cr, uid, ids, context):
        #     if not usr.fiscal_printer_id:
        #         raise osv.except_osv(_('Error!'),
        #                              _('Selected journal has not printer associated.'))
        #     if not usr.fiscal_printer_configuration_id:
        #         raise osv.except_osv(_('Error!'),
        #                              _('Selected journal has not configuration associated.'))
        #     if not usr.fiscal_printer_fiscal_state == 'open':
        #         raise osv.except_osv(_('Error!'),
        #                              _('Need open fiscal status to print a '
        #                                'ticket. Actual status is %s') % usr.fiscal_printer_fiscal_state)
        #     options = usr.fiscal_printer_configuration_id.toDict()[usr.fiscal_printer_configuration_id.id]
        #     fp_id = usr.fiscal_printer_id.id
        #     r[usr.id] = fp_obj.make_fiscal_ticket(cr, uid, [fp_id],
        #                                           options=options, ticket=ticket,
        #                                           context=context)[fp_id]
        #     if isinstance(r[usr.id], RuntimeError) and r[usr.id].message == "Timeout":
        #         raise osv.except_osv(_('Error!'),
        #                              _('Timeout happen!!'))
        # return r

    def make_fiscal_refund_ticket(self):
        """
        Create Fiscal Ticket.
        """
        pass
        # fp_obj = self.pool.get('fpoc.fiscal_printer')
        # context = context or {}
        # r = {}
        # for usr in self.browse(cr, uid, ids, context):
        #     if not usr.fiscal_printer_id:
        #         raise osv.except_osv(_('Error!'),
        #                              _('Selected journal has not printer associated.'))
        #     if not usr.fiscal_printer_configuration_id:
        #         raise osv.except_osv(_('Error!'),
        #                              _('Selected journal has not configuration associated.'))
        #     if not usr.fiscal_printer_fiscal_state == 'open':
        #         raise osv.except_osv(_('Error!'),
        #                              _('Need open fiscal status to print a '
        #                                'ticket. Actual status is %s') % usr.fiscal_printer_fiscal_state)
        #     options = usr.fiscal_printer_configuration_id.toDict()[usr.fiscal_printer_configuration_id.id]
        #     fp_id = usr.fiscal_printer_id.id
        #     r[usr.id] = fp_obj.make_fiscal_refund_ticket(cr, uid, [fp_id],
        #                                                  options=options, ticket=ticket,
        #                                                  context=context)[fp_id]
        #     if isinstance(r[usr.id], RuntimeError) and r[usr.id].message == "Timeout":
        #         raise osv.except_osv(_('Error!'),
        #                              _('Timeout happen!!'))
        # return r

    def cancel_fiscal_ticket(self):
        """
        """
        pass
        # fp_obj = self.pool.get('fpoc.fiscal_printer')
        # context = context or {}
        # r = {}
        # for usr in self.browse(cr, uid, ids, context):
        #     fp_id = usr.fiscal_printer_id.id
        #     r[usr.id] = fp_obj.cancel_fiscal_ticket(cr, uid, fp_id,
        #                                             context=context)[fp_id]
        # return r

    def open_fiscal_journal(self):
        pass
        # context = context or {}
        # r = {}
        # for usr in self.browse(cr, uid, ids, context):
        #     if not usr.fiscal_printer_state in ['ready']:
        #         raise osv.except_osv(_('Error!'), _('Printer is not ready to open.'))
        #     if not usr.fiscal_printer_fiscal_state in ['close']:
        #         raise osv.except_osv(_('Error!'), _('You can\'t open a printer already open.'))
        #     r[usr.id] = usr.fiscal_printer_id.open_fiscal_journal()
        # return r

    def close_fiscal_journal(self):
        pass
        # context = context or {}
        # r = {}
        # for usr in self.browse(cr, uid, ids, context):
        #     if not usr.fiscal_printer_state in ['ready']:
        #         raise osv.except_osv(_('Error!'), _('Printer is not ready to close.'))
        #     if not usr.fiscal_printer_fiscal_state in ['open']:
        #         raise osv.except_osv(_('Error!'), _('You can\'t close a closed printer.'))
        #     # if not usr.fiscal_printer_paper_state in ['ok']:
        #     #    raise osv.except_osv(_('Error!'), _('You can\'t close a printer with low quantity of paper.'))
        #     r[usr.id] = usr.fiscal_printer_id.close_fiscal_journal()
        # return r

    def shift_change(self):
        pass
        # context = context or {}
        # r = {}
        # for usr in self.browse(cr, uid, ids, context):
        #     if not usr.fiscal_printer_state in ['ready']:
        #         raise osv.except_osv(_('Error!'), _('Printer is not ready to close.'))
        #     if not usr.fiscal_printer_fiscal_state in ['open']:
        #         raise osv.except_osv(_('Error!'), _('You can\'t shift a closed printer.'))
        #     if not usr.fiscal_printer_paper_state in ['ok']:
        #         raise osv.except_osv(_('Error!'), _('You can\'t shift a printer with low quantity of paper.'))
        #     r[usr.id] = usr.fiscal_printer_id.shift_change()
        # return r

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
