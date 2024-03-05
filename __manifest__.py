# -*- coding: utf-8 -*-

{
    'name': 'Customer Installments',
    'version': '15.0.1.0.0',
    'category': 'Sales',
    'sequence': -20,
    'summary': 'Handle customer_installments_payments',
    'author': ' Mohamed Hussein',
    'license': 'AGPL-3',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'account', 'sale'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/sequnces.xml',
        'views/account_payment_inheret.xml',
        'views/customer_view.xml',
         'views/installment_menu.xml',
         'views/installment_payment_wizard_view.xml',


    ],
    # 'installable': True,
    'application': True,
    'auto_install': False,
}
