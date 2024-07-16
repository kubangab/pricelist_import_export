# Pricelist Import/Export

## Overview
The Pricelist Import/Export module for Odoo 17 allows users to easily import and export product prices in pricelists using Excel files. This module streamlines the process of managing large numbers of product prices across different pricelists.

## Features
- Import product prices to pricelists from Excel files
- Export pricelist data to Excel files
- Supports both creating new pricelist items and updating existing ones
- User-friendly interface integrated into the Odoo Pricelist views
- Handles both product variants and product templates
- Robust error handling and reporting

## Installation
1. Copy this module to your Odoo addons directory.
2. Update your addons list in Odoo.
3. Install the module through the Odoo interface.

## Configuration
No special configuration is needed. The module will add its features to the existing Pricelist functionality.

## Usage

### Importing Pricelists
1. Go to Sales > Configuration > Pricelists
2. Click on the "Import" button at the top of the pricelist tree view
3. Select your Excel file and click "Import"
4. Review any error messages if the import was not successful

### Exporting Pricelists
1. Go to Sales > Configuration > Pricelists
2. Select the pricelist you want to export
3. Click on the "Export" button at the top of the pricelist tree view
4. Save the generated Excel file

### File Format
The Excel file should have the following columns:
1. Internal Reference (Product Code)
2. Product Name
3. Price

## Technical Information
- Version: 16.0.2.0.0
- Depends: base, sale
- Author: Lasse Larsson
- License: AGPL-3

## Support
For bugs or feature requests, please use the [issue tracker](https://github.com/yourusername/pricelist_import_export/issues) on GitHub.

## Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/pricelist_import_export/issues).

## License
This project is licensed under the AGPL-3 License - see the [LICENSE](LICENSE) file for details.