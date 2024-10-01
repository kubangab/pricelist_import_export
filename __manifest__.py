{
    'name': "Pricelist Import/Export",
    'summary': "Import and export product prices in pricelists",
    'description': """
        This module allows you to import and export product prices in pricelists using Excel files.
    """,
    'version': '2.0.1',
    'category': 'Sales',
    'license': 'AGPL-3',
    'author': "Lasse Larsson",
    'website': "https://kubang.se",
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'security/pricelist_import_export_security.xml',
        'views/menu_views.xml',
        'views/product_pricelist_views.xml',
        'wizard/pricelist_import_export_wizard_view.xml',
    ],
    'installable': True,
}
