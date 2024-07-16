from odoo import http
from odoo.http import request
import base64

class PricelistImportExportController(http.Controller):
    @http.route('/web/binary/download_pricelist_export', type='http', auth="user")
    def download_pricelist_export(self, model, id, filename=None):
        record = request.env[model].browse(int(id))
        if not record.exists() or not filename:
            return request.not_found()
        content = base64.b64decode(record.file)
        return request.make_response(content, [
            ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
            ('Content-Disposition', 'attachment; filename=%s;' % filename),
            ('Content-Length', len(content)),
        ])
