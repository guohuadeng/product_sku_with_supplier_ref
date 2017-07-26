# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Humanytek (<www.humanytek.com>).
#    Manuel Márquez <manuel@humanytek.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    _sql_constraints = [
        ('uniq_default_code',
            'unique(default_code)',
            "The internal reference must be unique!"),
    ]

    @api.model
    def _get_default_code(self, supplier):
        """Returns the "Internal Reference" (SKU) for the product."""

        supplier_ref = supplier.ref
        products_supplier = self.with_context(active_test=False).search([
            ('default_code', 'like', '%s-%%' % (supplier_ref))
            ])

        if not products_supplier:
            sequence = '000001'
        else:
            current_max_sequence = max(
                products_supplier.mapped('default_code'))
            sequence = str(int(current_max_sequence[-6:]) + 1).zfill(6)

        default_code = '%s-%s' % (supplier_ref, sequence)
        return default_code

    @api.model
    def create(self, vals):

        if vals.get('product_tmpl_id'):
            ProductTemplate = self.env['product.template']
            product_template = ProductTemplate.browse(vals['product_tmpl_id'])

            if product_template.seller_ids:
                supplier = product_template.seller_ids[0].name
                if supplier.ref:
                    vals['default_code'] = \
                        self._get_default_code(supplier)

        return super(ProductProduct, self).create(vals)
