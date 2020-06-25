# -*- coding: utf-8 -*-
{
    'name': "purchase_filter_by_receipt_state",

    'summary': """
    Filter Purchases by receipt state
    """,

    'description': """
    Filter Purchases by receipt state
    """,

    'author': "Glo Networks",
    'website': "https://www.glo.systems/",

    'category': 'Purchases',
    'version': '12.0.1.0.0',
    'depends': [
        'purchase_stock'
    ],

    'data': [
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
    ],
}
