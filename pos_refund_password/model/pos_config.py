# -*- coding: utf-8 -*-
###############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2025-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Abbas P (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from odoo import api, models, fields


class PosConfig(models.Model):
    """Inherit pos configuration and add new fields."""
    _inherit = 'pos.config'

    refund_security = fields.Integer(string='Refund Security',
                                     help="Refund security password, used for that specified shop")

    @api.model
    def fetch_global_refund_security(self):
        """
        Fetches the global refund security parameter from system settings.

        This method retrieves the value of the configuration parameter
        'pos_refund_password.global_refund_security' stored in the `ir.config_parameter` model.

        Returns:
            str or None: The value of the global refund security parameter if set, otherwise None.
        """
        param = self.env['ir.config_parameter'].sudo().get_param('pos_refund_password.global_refund_security')
        return param
