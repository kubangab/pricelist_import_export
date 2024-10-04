from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import xlrd
import xlsxwriter
from io import BytesIO

class PricelistImportExportWizard(models.TransientModel):
    _name = 'pricelist.import.export.wizard'
    _description = 'Pricelist Import/Export Wizard'

    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', required=True)
    file = fields.Binary(string='File')
    file_name = fields.Char(string='File Name')
    action_type = fields.Selection([
        ('export', 'Export'),
        ('import', 'Import')
    ], string='Action', required=True, default='export')
    import_log = fields.Text(string='Import Log', readonly=True)
    operation_done = fields.Boolean(string='Operation Done', default=False)

    def action_import_export(self):
        if self.action_type == 'export':
            return self.export_pricelist()
        else:
            return self.import_pricelist()

    def export_pricelist(self):
        pricelist_items = self.env['product.pricelist.item'].search([
            ('pricelist_id', '=', self.pricelist_id.id),
            ('compute_price', '=', 'fixed')
        ])

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('Pricelist')

        headers = ['Internal Reference', 'Product', 'Variant', 'Price']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)

        for row, item in enumerate(pricelist_items, start=1):
            product = item.product_id or item.product_tmpl_id
            worksheet.write(row, 0, product.default_code or '')
            worksheet.write(row, 1, product.name)
            worksheet.write(row, 2, item.product_id.name if item.product_id else '')
            worksheet.write(row, 3, item.fixed_price)

        workbook.close()
        export_data = base64.b64encode(output.getvalue())

        filename = f'{self.pricelist_id.name}_Export.xlsx'
        
        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'datas': export_data,
            'type': 'binary',
        })

        # Mark the operation as done
        self.write({'operation_done': True})

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }

    def import_pricelist(self):
        if not self.file:
            raise UserError(_('Please select a file to import.'))

        try:
            workbook = xlrd.open_workbook(file_contents=base64.b64decode(self.file))
            sheet = workbook.sheet_by_index(0)

            error_log = []
            success_count = 0
            error_count = 0

            for row in range(1, sheet.nrows):  # Start from 1 to skip header
                try:
                    internal_ref = str(sheet.cell(row, 0).value).strip()
                    price = sheet.cell(row, 3).value

                    if not internal_ref:
                        error_msg = f"Row {row + 1}: Empty internal reference. Skipping row."
                        error_log.append(error_msg)
                        error_count += 1
                        continue

                    if not price:
                        error_msg = f"Row {row + 1}: Empty price for product '{internal_ref}'. Skipping row."
                        error_log.append(error_msg)
                        error_count += 1
                        continue

                    product = self.env['product.product'].search([('default_code', '=', internal_ref)], limit=1)
                    if not product:
                        error_msg = f"Row {row + 1}: Product with internal reference '{internal_ref}' not found. Skipping row."
                        error_log.append(error_msg)
                        error_count += 1
                        continue

                    pricelist_item = self.env['product.pricelist.item'].search([
                        ('pricelist_id', '=', self.pricelist_id.id),
                        ('product_id', '=', product.id),
                        ('compute_price', '=', 'fixed')
                    ], limit=1)

                    try:
                        price = float(price)
                        if price < 0:
                            raise ValueError("Price cannot be negative")
                    except ValueError as e:
                        error_msg = f"Row {row + 1}: Invalid price '{price}' for product '{internal_ref}'. {str(e)}"
                        error_log.append(error_msg)
                        error_count += 1
                        continue

                    if pricelist_item:
                        old_price = pricelist_item.fixed_price
                        pricelist_item.fixed_price = price
                        success_count += 1
                        if old_price != price:
                            self.env.cr.commit()  # Commit the change immediately
                            self.env.cache.invalidate()  # Invalidate the cache
                    else:
                        error_msg = f"Row {row + 1}: No existing pricelist item found for product '{internal_ref}'. Skipping row."
                        error_log.append(error_msg)
                        error_count += 1

                except Exception as e:
                    error_msg = f"Row {row + 1}: Unexpected error: {str(e)}"
                    error_log.append(error_msg)
                    error_count += 1

            self.write({
                'import_log': "\n".join(error_log) if error_log else "All rows were imported successfully.",
                'operation_done': True
            })
            
            message = f"Import completed. Successful updates: {success_count}, Errors: {error_count}"
            if error_count > 0:
                message += "\nPlease check the error log below for details."
            
            return {
                'type': 'ir.actions.act_window',
                'res_model': self._name,
                'res_id': self.id,
                'view_mode': 'form',
                'target': 'new',
                'context': {'import_result': message}
            }

        except Exception as e:
            raise UserError(_('Error importing file: %s') % str(e))