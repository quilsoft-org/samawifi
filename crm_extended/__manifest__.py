##############################################################################
#
#    Copyright (C) 2022  Quilsoft  (http://www.quilsoft.com)
#    All Rights Reserved.
#
##############################################################################

{
    'name': 'crm extended',
    'version': '14.0.1.0.0',
    'category': 'CRM',
    'summary': "Extend fields of lead crm",
    'author': "Quilsoft",
    'license': 'AGPL-3',
    'depends': [
        'crm',
        ],
     'data': [
         'views/view_crm_extended.xml',
     ],

    'installable': True,
}
