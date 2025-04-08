# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import api, models


class PosConfig(models.Model):
    """Inheriting pos config to get location summary"""
    _inherit = 'pos.config'

    def get_location_summary(self, location_id):
        """Function to get location details"""
        location_quant = self.env['stock.quant'].search(
            [('location_id', '=', int(location_id))])
        location_summary = []
        for quant in location_quant.filtered(
                lambda x: x.product_id.available_in_pos):
            location_summary.append({
                    'product_id': quant.product_id.id,
                    'product': quant.product_id.name,
                    'quantity': quant.available_quantity,
                })
        return location_summary


class PosSession(models.Model):
    """Inheriting pos config to get location summary"""
    _inherit = 'pos.session'

    @api.model
    def _load_pos_data_models(self, config_id):
        data = super()._load_pos_data_models(config_id)
        data += ['stock.location']
        return data


class StockLocation(models.Model):
    """Inheriting pos config to get location summary"""
    _inherit = 'stock.location'

    @api.model
    def _load_pos_data_fields(self, config_id):
        return ['id', 'name']

    def _load_pos_data(self, data):
        fields = self._load_pos_data_fields(data['pos.config']['data'][0]['id'])
        domain = [('usage', '=', 'internal')]
        return {
            'data': self.search_read(domain, fields,
                                     load=False) if domain is not False else [],
            'fields': fields,
        }
