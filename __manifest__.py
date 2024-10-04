{
    'name': 'Pricelist Import/Export',
    'version': '1.0.0',
    'category': 'Sales',
    'summary': 'Import and export pricelist items',
    'description': """
        This module allows you to import and export pricelist items using Excel files.
        It supports exporting all non-computed pricelist items and importing updated prices.
    """,
    'author': 'Lasse Larsson, Kubang AB',
    'website': 'https://www.kubang.eu',
    'license': 'LGPL-3',
    'depends': ['product', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/pricelist_import_export_wizard.xml',
        'views/pricelist_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}