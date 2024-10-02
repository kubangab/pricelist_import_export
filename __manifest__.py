{
    'name': "Pricelist Import/Export",
    'summary': "Import and export product prices in pricelists",
    'description': """
        This module allows you to import and export product prices in pricelists using Excel files.
    """,
    'version': '2.0.2',
    'category': 'Sales',
    'license': 'AGPL-3',
    'author': "Lasse Larsson",
    'website': "https://kubang.se",
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'security/pricelist_import_export_security.xml',
        'wizard/pricelist_import_export_wizard_view.xml',
        'views/menu_views.xml',
        'views/product_pricelist_views.xml',
        'views/pricelist_import_export.xml',
    ],
    'installable': True,
}
