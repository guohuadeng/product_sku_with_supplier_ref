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
from openerp.exceptions import ValidationError
from openerp.tools.translate import _


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _get_default_code(self, supplier):
        """Returns the "Internal Reference" (SKU) for the product."""

        supplier_ref = supplier.ref
        products_supplier = self.with_context(active_test=False).search([
            ('default_code', 'like', '%s-%%' % (supplier_ref))
            ])

        IrConfigParameter = self.env['ir.config_parameter']
        exists_parameter_number_digits = IrConfigParameter.search([
            ('key', '=', 'product_sku_number_digits')
            ])
        if exists_parameter_number_digits:
            number_digits = int(exists_parameter_number_digits[0].value)
        else:
            raise ValidationError(_(
                'The system parameter product_sku_number_digits	does not exist'))

        if not products_supplier:
            sequence = '1'.zfill(number_digits)
        else:
            current_max_sequence = max(
                products_supplier.mapped('default_code'))
            sequence = str(int(
                current_max_sequence[-number_digits:]) + 1) \
                .zfill(number_digits)

        default_code = '%s-%s' % (supplier_ref, sequence)
        return default_code

    @api.model
    def create(self, vals):

        if vals.get('product_tmpl_id'):
            ProductTemplate = self.env['product.template']
            product_template = ProductTemplate.browse(vals['product_tmpl_id'])
            if not product_template.product_variant_ids:
                if product_template.seller_ids:
                    supplier = product_template.seller_ids[0].name
                    if supplier.ref:
                        vals['default_code'] = \
                            self._get_default_code(supplier)
            else:
                vals['default_code'] = product_template \
                    .product_variant_ids[0].default_code

        return super(ProductProduct, self).create(vals)
