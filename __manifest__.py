{
    'name': "Hospital Management",

    'summary': """
        Module for managing the Hospital""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Hospital method",
    'website': "http://www.hospital.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['mail'],

    # always loaded
    'data': [
        'views/patient.xml',
        'views/test.xml',
        'views/report.xml',
        'views/dashboard.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        # 'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
    'installable': True,
    'applications': True,
    'auto_install': False,
}
