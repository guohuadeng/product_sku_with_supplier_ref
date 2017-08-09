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

{
    'name': "product_sku_with_supplier_ref",
    'summary': """Addon for odoo that generates a SKU code for the products in
    field "Internal Reference".""",
    'description': """
        Addon for odoo that generates a SKU code for the products in field
        "Internal Reference". This SKU code has the following format:
        &lt;supplier_ref>-&lt;sequence_by_supplier>
    """,
    'author': "Humanytek",
    'website': "http://www.humanytek.com",
    'category': 'Purchases',
    'version': '0.1.0',
    'depends': ['product', ],
    'data': [
        'data/ir_config_parameter.xml',
        'views/product_view.xml',
    ],
    'demo': [
    ],
}
