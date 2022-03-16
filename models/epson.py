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
from odoo import models, api, fields
from odoo.tools.translate import _

from ..controllers.main import do_event
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)
_schema = logging.getLogger(__name__ + '.schema')

_header_lines = ['headerLine 1', 'headerLine 2', 'headerLine 3', 'headerLine 4', 'headerLine 5', 'headerLine 6',
                 'headerLine 7']
_footer_lines = ['footerLine 1', 'footerLine 2', 'footerLine 3', 'footerLine 4', 'footerLine 5', 'footerLine 6',
                 'footerLine 7']


class EpsonFiscalPrinter(models.Model):
    """
    The fiscal printer entity.
    """

    _inherit = 'fpoc.fiscal_printer'

    def _get_field(self):
        pass
        # r = {}
        # for fp in self.browse(cr, uid, ids):
        #     r[fp.id] = {fn: False for fn in field_name}
        #     event_result = do_event('read_attributes', {'name': fp.name},
        #                             session_id=fp.session_id, printer_id=fp.name)
        #     event_result = event_result.pop() if event_result else {}
        #     if event_result and 'attributes' in event_result:
        #         attrs = event_result['attributes']
        #         r[fp.id]['header'] = '\n'.join([attrs[k] for k in _header_lines
        #                                         if k in attrs and attrs[k]])
        #         r[fp.id]['footer'] = '\n'.join([attrs[k] for k in _footer_lines
        #                                         if k in attrs and attrs[k]])
        #         for fn in field_name:
        #             if fn in attrs:
        #                 if fn in ['tasaIVA', 'maxMonto']:
        #                     r[fp.id][fn] = float(attrs[fn]) / 100.
        #                 elif fn in ['fechaFiscalizacion']:
        #                     line = attrs[fn]
        #                     r[fp.id][fn] = "20{2}-{1}-{0}".format(*[line[i:i + 2] for i in range(0, len(line), 2)])
        #                 else:
        #                     r[fp.id][fn] = attrs[fn]
        # return r

    def _put_field(self):
        pass
        # fp = self.browse(cr, uid, ids)
        # data = {'name': fp.name,
        #         'attributes': {}}
        # if (field_name == 'header'):
        #     lines = field_value.split('\n')[:len(_header_lines)] if field_value else []
        #     lines = lines + (len(_header_lines) - len(lines)) * ['']
        #     data['attributes'].update(dict(zip(_header_lines, lines)))
        # if (field_name == 'footer'):
        #     lines = field_value.split('\n')[:len(_footer_lines)] if field_value else []
        #     lines = lines + (len(_footer_lines) - len(lines)) * ['']
        #     data['attributes'].update(dict(zip(_footer_lines, lines)))
        # event_result = do_event('write_attributes', data,
        #                         session_id=fp.session_id, printer_id=fp.name)
        # return True

    header = fields.Text(compute='_get_field', inverse='_put_field', string='Header')
    footer = fields.Text(compute='_get_field', inverse='_put_field', string='Footer')

    razonSocial = fields.Char(compute='_get_field', string='Razon Social')
    cuit = fields.Char(compute='_get_field', string='CUIT')
    caja = fields.Char(compute='_get_field', string='Caja/Punto de Venta')
    ivaResponsabilidad = fields.Char(compute='_get_field', string='Resp. IVA')
    calle = fields.Char(compute='_get_field', string='Calle')
    numero = fields.Char(compute='_get_field', string='Numero')
    piso = fields.Char(compute='_get_field', string='Piso')
    depto = fields.Char(compute='_get_field', string='Depto')
    localidad = fields.Char(compute='_get_field', string='Localidad')
    cpa = fields.Char(compute='_get_field', string='Cod.Pos.')
    provincia = fields.Char(compute='_get_field', string='Provincia')
    tasaIVA = fields.Float(compute='_get_field', string='Tasa IVA')
    maxMonto = fields.Float(compute='_get_field', string='Monto Maximo')
    fechaFiscalizacion = fields.Date(compute='_get_field', string='Fecha Fiscalizacion')


class EpsonArFiscaltfPrinterConfiguration(models.Model):
    """
    Configuracion necesaria para documentos fiscales Ticket-Facturas/Nota de Debito
    """

    _inherit = 'fpoc.configuration'
    _description = 'Configuracion de TF/TND para Epson Argentina'

    epson_type_paper_status = {
        'epson_ar_receipt': ('receiptState', {
            0: 'ok',
            1: 'low',
            2: 'none',
            3: 'unknown',
        }),
        'epson_ar_journal': ('journalState', {
            0: 'ok',
            1: 'low',
            2: 'none',
            3: 'unknown',
        }),
        'epson_ar_slip': ('slipHasPaper', {
            0: 'ok',
            1: 'low',
            2: 'none',
            3: 'unknown',
        }),
    }

    def solve_status(self):
        pass
        # r = super(epson_ar_fiscal_tf_printer_configuration, self).solve_status(cr, uid, ids, status, context=context)
        # for conf in self.browse(cr, uid, ids):
        #     if conf.type not in ['epson_ar_receipt', 'epson_ar_journal', 'epson_ar_slip']:
        #         continue
        #     for stat in r.values():
        #         _logger.debug(stat)
        #         if not stat:
        #             continue
        #         if 'paper_state' not in stat:
        #             key, rule = self.epson_type_paper_status.get(conf.type, (False, False))
        #             stat['paper_state'] = rule.get(stat.get(key, 'unknown'), 'unknown')
        #         if 'fiscal_state' not in stat:
        #             stat['fiscal_state'] = 'open' if stat['inFiscalJournal'] else 'close'
        #         if 'printer_state' not in stat:
        #             stat['printer_state'] = [v for v in ['deviceopen' if stat['isPrinterOpen'] else False,
        #                                                  'onerror' if stat['inError'] else False,
        #                                                  'offline' if stat['isOffline'] else False,
        #                                                  'nomemory' if stat['memStatus'] else False,
        #                                                  'nopaper' if stat['slipHasPaper'] else False,
        #                                                  'printing' if stat['documentInProgress'] else False,
        #                                                  'ready'] if v][0]
        # return r

    def _get_type(self):
        return []
        # r = super(epson_ar_fiscal_tf_printer_configuration, self)._get_type(cr, uid, context=context)
        # return r + [
        #     ('epson_ar_receipt', _('Receipt Epson Arg.')),
        #     ('epson_ar_journal', _('Journal Epson Arg.')),
        #     ('epson_ar_slip', _('Slip station Epson Arg.')),
        # ]

    type = fields.Selection(selection=_get_type, string='Type')
    triplicated = fields.Boolean('Imprimir en triplicado')
    store_description = fields.Boolean('Almacenar descripciones de items')
    keep_description_attributes = fields.Boolean('Conservar atributos de impresion de las descripciones')
    store_extra_description = fields.Boolean('Almacenar solo primer descripcion extra')
    cut_paper = fields.Boolean('Cortar papel')
    electronic_answer = fields.Boolean('Devuelve respuesta electronica')
    print_return_attribute = fields.Boolean('Imprime "Su Vuelto" con atributos')
    current_account_automatic_pay = fields.Boolean('Utiliza pago automatico como cuenta corriente')
    print_quantities = fields.Boolean('Imprimir Cantidad de unidades')
    tail = fields.Text('Modificaciones en el pie del ticket')

    @api.onchange('type')
    def onchange_type(self):
        r = super().onchange_type()
        if (self.type == "epson_ar_tf"):
            r['value']['protocol'] = 'epson_ar'
        return r

    def toDict(self):
        r = super().toDict()
        # fields = self._columns.keys()
        # fields.remove('user_ids')
        # for conf in self.read(cr, uid, ids, fields, context=context):
        #     if (conf['type'] == "epson_ar_tf"):
        #         conf_id = conf['id']
        #         del conf['type']
        #         del conf['name']
        #         del conf['protocol']
        #         del conf['id']
        #         del conf['tail']  # Proceso especial.
        #         r[conf_id] = conf
        return r

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
