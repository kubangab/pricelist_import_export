from odoo import api, fields, models, _
from odoo.exceptions import UserError
import base64
import xlsxwriter
import xlrd
from io import BytesIO

class PricelistImportExportWizard(models.Model):
    _name = 'pricelist.import.export.wizard'
    _description = 'Pricelist Import/Export Wizard'

    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', required=True)
    file = fields.Binary(string='File', attachment=False)
    file_name = fields.Char(string='File Name')
    action_type = fields.Selection([
        ('import', 'Import'),
        ('export', 'Export')
    ], string='Action Type', required=True)

    @api.model
    def default_get(self, fields):
        res = super(PricelistImportExportWizard, self).default_get(fields)
        active_id = self.env.context.get('active_id')
        if active_id:
            res['pricelist_id'] = active_id
        return res

    def action_import_export(self):
        self.ensure_one()
        if self.action_type == 'import':
            return self._import_pricelist()
        elif self.action_type == 'export':
            return self._export_pricelist()
        else:
            raise UserError(_("Invalid action type."))

    def _import_pricelist(self):
        if not self.file:
            raise UserError(_('Please select a file to import.'))

        try:
            xlsx_data = base64.b64decode(self.file)
            workbook = xlrd.open_workbook(file_contents=xlsx_data)
            sheet = workbook.sheet_by_index(0)

            for row in range(1, sheet.nrows):  # Start from 1 to skip header
                internal_ref = sheet.cell(row, 0).value
                product_name = sheet.cell(row, 1).value
                variant_name = sheet.cell(row, 2).value
                price = sheet.cell(row, 3).value

                product = self.env['product.product'].search([('default_code', '=', internal_ref)], limit=1)
                if not product:
                    product = self.env['product.template'].search([('default_code', '=', internal_ref)], limit=1)

                if not product:
                    raise UserError(_('Product with internal reference %s not found.') % internal_ref)

                pricelist_item = self.env['product.pricelist.item'].search([
                    ('pricelist_id', '=', self.pricelist_id.id),
                    '|', ('product_id', '=', product.id), ('product_tmpl_id', '=', product.product_tmpl_id.id)
                ], limit=1)

                if pricelist_item:
                    pricelist_item.write({'fixed_price': price})
                else:
                    self.env['product.pricelist.item'].create({
                        'pricelist_id': self.pricelist_id.id,
                        'product_id': product.id if product._name == 'product.product' else False,
                        'product_tmpl_id': product.id if product._name == 'product.template' else product.product_tmpl_id.id,
                        'fixed_price': price,
                    })

            return {'type': 'ir.actions.act_window_close'}

        except Exception as e:
            raise UserError(_('Error importing file: %s') % str(e))

    def _export_pricelist(self):
        self.ensure_one()
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet(self.pricelist_id.name)

        # Skriv rubrikerna
        headers = ['Internal Reference', 'Product', 'Variant', 'Price']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)

        # Skriv prislistans innehåll
        row = 1
        for item in self.pricelist_id.item_ids:
            if item.compute_price != 'fixed':  # Skippa beräknade rader
                continue
            product = item.product_id or item.product_tmpl_id
            if item.product_id:  # Detta är en produktvariant
                worksheet.write(row, 0, item.product_id.default_code or '')
                worksheet.write(row, 1, product.name)
                worksheet.write(row, 2, item.product_id.name)
            else:  # Detta är en produktmall
                worksheet.write(row, 0, product.default_code or '')
                worksheet.write(row, 1, product.name)
                worksheet.write(row, 2, '')
            worksheet.write(row, 3, item.fixed_price)
            row += 1

        workbook.close()
        xlsx_data = output.getvalue()

        # Spara den genererade filen i wizard-posten
        self.write({
            'file': base64.b64encode(xlsx_data),
            'file_name': f"{self.pricelist_id.name}_export.xlsx"
        })

        # Returnera en aktion för att ladda ner filen
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/?model={self._name}&id={self.id}&field=file&filename_field=file_name&download=true',
            'target': 'self',
        }

    def generate_excel(self):
        pricelist = self.pricelist_id
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet(pricelist.name)

        header_style = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#F2F2F2'})

        headers = ['Internal Reference', 'Product Name', 'Price']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_style)

        for row, item in enumerate(pricelist.item_ids, start=1):
            product = item.product_tmpl_id or item.product_id.product_tmpl_id
            worksheet.write(row, 0, product.default_code)
            worksheet.write(row, 1, product.name)
            worksheet.write(row, 2, item.fixed_price)

        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 40)
        worksheet.set_column('C:C', 15)

        workbook.close()
        xlsx_data = output.getvalue()

        self.file = base64.b64encode(xlsx_data)
        self.file_name = f"{pricelist.name}_export.xlsx"

    @api.model
    def action_import_pricelist(self):
        return self._get_action('import')

    @api.model
    def action_export_pricelist(self):
        wizard = self.create({
            'pricelist_id': self.env.context.get('active_id'),
            'action_type': 'export',
        })
        return wizard.export_pricelist()

    def _get_action(self, action_type):
        return {
            'name': _('Import Pricelist') if action_type == 'import' else _('Export Pricelist'),
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_action_type': action_type,
                'default_pricelist_id': self.env.context.get('active_id'),
            },
        }
