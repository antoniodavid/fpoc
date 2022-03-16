# -*- coding: utf-8 -*-
##############################################################################
#
#    fiscal_printer
#    Copyright (C) 2014 No author.
#    No email
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

import re
from odoo import netsvc
from odoo import osv, fields, models, api
from odoo.tools.translate import _
from odoo.exceptions import UserError

from ..controllers.main import do_event
from datetime import datetime

from odoo.addons.fpoc.controllers.main import DenialService


class FiscalPrinterDisconnected(models.TransientModel):
    """
    Disconnected but published printers.
    """
    _name = 'fpoc.disconnected'
    _description = 'Printers not connected to the server.'

    name = fields.Char(string='Name')
    protocol = fields.Char(string='Protocol')
    model = fields.Char(string='Model')
    serialNumber = fields.Char(string='Serial Number')
    session_id = fields.Char(string='Session')
    user_id = fields.Many2one('res.users', string='Responsable')

    def _update_(self):
        pass

    #     cr.execute('SELECT COUNT(*) FROM %s' % self._table)
    #     count = cr.fetchone()[0]
    #     if not force and count > 0:
    #         return
    #     if count > 0:
    #         cr.execute('DELETE FROM %s' % self._table)
    #     t_fp_obj = self.pool.get('fpoc.fiscal_printer')
    #     R = do_event('list_printers', control=True)
    #     w_wfp_ids = []
    #     i = 0
    #     for resp in R:
    #         if not resp: continue
    #         for p in resp['printers']:
    #             if t_fp_obj.search(cr, uid, [("name", "=", p['name'])]):
    #                 pass
    #             else:
    #                 values = {
    #                     'name': p['name'],
    #                     'protocol': p['protocol'],
    #                     'model': p.get('model', 'undefined'),
    #                     'serialNumber': p.get('serialNumber', 'undefined'),
    #                     'session_id': p['sid'],
    #                     'user_id': p['uid'],
    #                 }
    #                 pid = self.create(cr, uid, values)

    # def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
    #     self._update_(cr, uid, force=True)
    #     return super().search(cr, uid, args, offset=offset, limit=limit, order=order,
    #                                                            context=context, count=count)
    #
    # def read(self):
    #     self._update_(cr, uid, force=False)
    #     return super().read(cr, uid, ids, fields=fields, context=context, load=load)

    def create_fiscal_printer(self):
        pass
    #     """
    #     Create fiscal printers from this temporal printers
    #     """
    #     fp_obj = self.pool.get('fpoc.fiscal_printer')
    #     for pri in self.browse(cr, uid, ids):
    #         # import pdb;pdb.set_trace()
    #         values = {
    #             'name': pri.name,
    #             'protocol': pri.protocol,
    #             'model': pri.model,
    #             'serialNumber': pri.serialNumber,
    #             'session_id': pri.session_id
    #         }
    #         fp_obj.create(cr, uid, values)
    #     return {
    #         'name': _('Fiscal Printers'),
    #         'domain': [],
    #         'res_model': 'fpoc.fiscal_printer',
    #         'type': 'ir.actions.act_window',
    #         'view_id': False,
    #         'view_mode': 'tree,form',
    #         'context': context,
    # }


class FiscalPrinter(models.Model):
    """
    The fiscal printer entity.
    """
    _name = 'fpoc.fiscal_printer'
    _description = 'Fiscal Printer'

    name = fields.Char(string='Name', required=True)
    protocol = fields.Char(string='Protocol')
    model = fields.Char(string='Model')
    serialNumber = fields.Char(string='Serial Number (S/N)')
    lastUpdate = fields.Datetime(string='Last Update')
    printerStatus = fields.Char(compute='_compute_get_printer_status', string='Printer status')
    fiscalStatus = fields.Char(compute='_compute_get_printer_status', string='Fiscal status')
    clock = fields.Datetime(compute='_compute_get_printer_status', string='Clock')
    session_id = fields.Char(string='session_id')

    _sql_constraints = [
        ('model_serialNumber_unique', 'unique("model", "serialNumber")',
         'this printer with this model and serial number yet exists')
    ]

    def _compute_get_printer_status(self):
        s = self.get_state()
        for record in self:
            if s[record.id]:
                dt = datetime.strptime(s[record.id]['clock'], "%Y-%m-%d %H:%M:%S")
                self.clock = dt.strftime("%Y-%m-%d %H:%M:%S")
                self.printerStatus = s[record.id]['printerStatus']
                self.fiscalStatus = s[record.id]['fiscalStatus']
            else:
                self.clock = None
                self.printerStatus = 'Offline'
                self.fiscalStatus = 'Offline'

    def update_printers(self):
        pass

    #     r = do_event('info', {})
    #     return True
    #
    def short_test(self):
        pass

    #     for fp in self.browse(cr, uid, ids):
    #         do_event('short_test', {'name': fp.name},
    #                  session_id=fp.session_id, printer_id=fp.name)
    #     return True
    #
    def large_test(self):
        pass

    #     for fp in self.browse(cr, uid, ids):
    #         do_event('large_test', {'name': fp.name},
    #                  session_id=fp.session_id, printer_id=fp.name)
    #     return True
    #
    def advance_paper(self):
        pass

    #     for fp in self.browse(cr, uid, ids):
    #         do_event('advance_paper', {'name': fp.name},
    #                  session_id=fp.session_id, printer_id=fp.name)
    #     return True
    #
    def cut_paper(self):
        pass

    #     for fp in self.browse(cr, uid, ids):
    #         do_event('cut_paper', {'name': fp.name},
    #                  session_id=fp.session_id, printer_id=fp.name)
    #     return True
    #
    def open_fiscal_journal(self):
        pass

    #     for fp in self.browse(cr, uid, ids):
    #         do_event('open_fiscal_journal', {'name': fp.name},
    #                  session_id=fp.session_id, printer_id=fp.name)
    #     return True
    #
    def cancel_fiscal_ticket(self):
        pass

    #     for fp in self.browse(cr, uid, ids):
    #         do_event('cancel_fiscal_ticket', {'name': fp.name},
    #                  session_id=fp.session_id, printer_id=fp.name)
    #     return True
    #
    def close_fiscal_journal(self):
        pass

    #     for fp in self.browse(cr, uid, ids):
    #         do_event('close_fiscal_journal', {'name': fp.name},
    #                  session_id=fp.session_id, printer_id=fp.name)
    #     return True
    #
    def shift_change(self):
        pass

    #     for fp in self.browse(cr, uid, ids):
    #         do_event('shift_change', {'name': fp.name},
    #                  session_id=fp.session_id, printer_id=fp.name)
    #     return True
    #

    def get_state(self):
        r = {}
        for fp in self:
            try:
                event_result = do_event('get_status', {'name': fp.name}, session_id=fp.session_id, printer_id=fp.name)
            except DenialService as m:
                raise UserError(_('Connectivity Error'), m)
            r[fp.id] = event_result.pop() if event_result else False
        return r

    #
    def get_counters(self):
        pass

    #     r = {}
    #     for fp in self.browse(cr, uid, ids):
    #         event_result = do_event('get_counters', {'name': fp.name},
    #                                 session_id=fp.session_id, printer_id=fp.name)
    #         r[fp.id] = event_result.pop() if event_result else False
    #     return r
    #
    def make_fiscal_ticket(self):
        pass

    #     fparms = {}
    #     r = {}
    #     for fp in self.browse(cr, uid, ids):
    #         fparms['name'] = fp.name
    #         fparms['options'] = options
    #         fparms['ticket'] = ticket
    #         # import pdb;pdb.set_trace()
    #         # event_result = do_event('make_fiscal_ticket', fparms,
    #         event_result = do_event('make_ticket_factura', fparms,
    #                                 session_id=fp.session_id, printer_id=fp.name)
    #         r[fp.id] = event_result.pop() if event_result else False
    #     return r
    #
    def make_fiscal_refund_ticket(self):
        pass

    #     fparms = {}
    #     r = {}
    #     for fp in self.browse(cr, uid, ids):
    #         fparms['name'] = fp.name
    #         fparms['options'] = options
    #         fparms['ticket'] = ticket
    #         # import pdb;pdb.set_trace()
    #         # event_result = do_event('make_fiscal_ticket', fparms,
    #         event_result = do_event('make_ticket_notacredito', fparms,
    #                                 session_id=fp.session_id, printer_id=fp.name)
    #         r[fp.id] = event_result.pop() if event_result else False
    #     return r
    #
    def cancel_fiscal_ticket(self):
        pass
    #     fparms = {}
    #     r = {}
    #     for fp in self.browse(cr, uid, ids):
    #         fparms['name'] = fp.name
    #         event_result = do_event('cancel_fiscal_ticket', fparms,
    #                                 session_id=fp.session_id, printer_id=fp.name)
    #         r[fp.id] = event_result.pop() if event_result else False
    #     return r

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
