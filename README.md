# Pricelist Import/Export

## Overview
The Pricelist Import/Export module is an Odoo 16 extension that enhances the functionality of product pricelists by allowing users to easily import and export pricelist data using Excel files. This module streamlines the process of managing large numbers of product prices across different pricelists.

## Features
- **Import Pricelists**: Quickly update product prices by importing Excel files.
- **Export Pricelists**: Generate Excel files containing current pricelist data for easy editing or backup.
- **User-Friendly Interface**: Seamlessly integrated into Odoo's existing pricelist views.
- **Flexible File Handling**: Works with standard Excel file formats for maximum compatibility.

## Installation
1. Copy the `pricelist_import_export` folder to your Odoo addons directory.
2. Update the addons list in your Odoo instance.
3. Install the module through the Odoo Apps menu.

## Configuration
No additional configuration is required. The module will automatically add its features to the product pricelist views.

## Usage
### Importing a Pricelist
1. Navigate to Sales > Configuration > Pricelists.
2. Select a pricelist or create a new one.
3. Click the "Import" button at the top of the pricelist form.
4. Choose your Excel file and click "Import".

### Exporting a Pricelist
1. Navigate to Sales > Configuration > Pricelists.
2. Select the pricelist you want to export.
3. Click the "Export" button at the top of the pricelist form.
4. The system will generate and download an Excel file with the current pricelist data.

## File Format
The Excel file for import/export should have the following columns:
1. Internal Reference (Product Code)
2. Product Name
3. Price

## Dependencies
- `base`
- `sale`

## Author
Lasse Larsson

## Website
https://kubang.se

## License
This module is licensed under the GNU Affero General Public License (AGPL-3.0).

## Support
For support, please contact the author or visit the website mentioned above.

## Contribution
Contributions, issues, and feature requests are welcome. Feel free to check the [issues page](link-to-your-issues-page) if you want to contribute.

## Changelog
- 16.0.2.0.0: Initial release for Odoo 16.