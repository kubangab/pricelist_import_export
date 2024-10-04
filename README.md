# Pricelist Import/Export

## Overview
The Pricelist Import/Export module for Odoo 16 provides a simple and efficient way to manage product pricelists. It allows users to export existing pricelist items to an Excel file and import updated prices back into the system.

## Features
- Export pricelist items to Excel (.xlsx) format
- Import updated prices from Excel files
- User-friendly wizard interface
- Supports fixed price items in pricelists
- Automatic file download upon export
- Error logging for import issues

## Installation
1. Copy the `pricelist_import_export` folder to your Odoo addons directory.
2. Update the addons list in your Odoo instance.
3. Install the "Pricelist Import/Export" module from the Odoo Apps menu.

## Usage

### Exporting a Pricelist
1. Navigate to Sales > Configuration > Pricelists.
2. Select the pricelist you want to export.
3. Click on the "Import/Export" button in the form view.
4. In the wizard, select "Export" as the action type.
5. Click "Execute". An Excel file will be automatically downloaded containing the pricelist items.

### Importing Updated Prices
1. Navigate to Sales > Configuration > Pricelists.
2. Select the pricelist you want to update.
3. Click on the "Import/Export" button in the form view.
4. In the wizard, select "Import" as the action type.
5. Upload the Excel file containing the updated prices.
6. Click "Execute". The system will process the file and update the pricelist items.
7. Check the import log for any errors or warnings.

## File Format
The Excel file used for import/export should have the following columns:
1. Internal Reference
2. Product
3. Variant
4. Price

## Note
- Only fixed price items in the pricelist will be exported and can be imported.
- Ensure that the "Internal Reference" in the import file matches the product's internal reference in Odoo for successful updates.

## Support
For any issues or feature requests, please contact your Odoo support team or the module maintainer.

## Contributors
- Lasse Larsson, Kubang AB

## License
This module is licensed under LGPL-3.

---

We hope this module helps streamline your pricelist management process in Odoo 16!