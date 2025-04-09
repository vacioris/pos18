# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import email_normalize


class RegisterVendor(models.TransientModel):
    """Vendor Registration"""
    _name = 'register.vendor'
    _description = 'Register Vendors'

    def default_is_registered(self):
        """default value for is registered"""
        if self.env.context.get('active_model') == 'res.partner':
            users = self.env['res.users'].search([(
                'partner_id', '=', self.env.context.get('active_id'))])
            if users:
                return True
        return False

    is_registered = fields.Boolean(default=default_is_registered)

    def action_create_user_portal(self):
        """creating the portal user"""
        if self.env.context.get('active_model') == 'res.partner':
            partner = self.env['res.partner'].browse(
                self.env.context.get('active_id'))
            if not partner.email:
                raise ValidationError(_("Provide Email For Vendor"))
            user = self.env['res.users'].with_context(no_reset_password=True).sudo()._create_user_from_template({
                'email': email_normalize(partner.email),
                'login': email_normalize(partner.email),
                'partner_id': partner.id,
                'company_id': self.env.company.id,
                'company_ids': [(6, 0, self.env.company.ids)],
                'active': True
            })
            self._send_email(user)
            partner.sudo().write({
                'is_registered': True,
            })

    def _send_email(self, user):
        """ send notification email to a new portal user """
        self.ensure_one()
        self.env['portal.wizard'].action_open_wizard()
        return True

    def send_password_reset_portal(self):
        """Send password reset email"""
        if self.env.context.get('active_model') == 'res.partner':
            partner = self.env['res.partner'].browse(
                self.env.context.get('active_id'))
            user = self.env['res.users'].search([
                ('partner_id', '=', partner.id)])
            user.action_reset_password()
