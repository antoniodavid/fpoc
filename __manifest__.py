# -*- coding: utf-8 -*-
{
    'name': 'Fiscal Printer on the Cloud',
    'author': 'Moldeo Interactive',
    'category': 'base.module_category_hidden',
    'depends': [],
    'version': '14.0.1.1',
    'description': 'Fiscal Printer on the Cloud',
    'installable': True,
    'license': 'AGPL-3',
    'test': [
        u'test/check_spools.yml',
    ],
    'data': [
        'security/fiscal_printer_group.xml',
        'security/ir.model.access.csv',
        'views/fiscal_printer_view.xml',
        'views/fpoc_menuitem.xml',
    ],

    'website': 'https://github.com/csrocha/odoo_fpoc'
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
