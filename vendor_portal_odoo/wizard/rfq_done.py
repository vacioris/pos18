# -*- coding: utf-8 -*-

from odoo import fields, models


class RfqDone(models.TransientModel):
    """Done the Quotation"""
    _name = 'rfq.done'
    _description = 'Done RFQs'

    vendor_id = fields.Many2one('vendor.quote.history', string='Vendor',
                                required=True,
                                domain='[("id", "in", quote_ids)]',
                                help="Vendors Who Accepted the Quotes")
    quote_ids = fields.Many2many('vendor.quote.history',
                                 string="Quotes", help="Quotes for the Order")
    quoted_price = fields.Monetary(currency_field='currency_id',
                                   related='vendor_id.quoted_price',
                                   string='Quoted Price',
                                   help="Quoted Price")
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  help="Currency",
                                  required=True,
                                  default=lambda
                                      self: self.env.user.company_id.currency_id,
                                  related='vendor_id.currency_id')
    estimate_date = fields.Date(related='vendor_id.estimate_date',
                                string='Estimate Date',
                                help="Estimated Date")

    def action_done(self):
        """Marking the RFQ as done"""
        rfq = self.env['vendor.rfq'].browse(self._context.get('active_id'))
        template_id = self.env.ref(
            'vendor_portal_odoo.email_template_vendor_rfq_mark_done').id
        context = {
            'name': self.vendor_id.vendor_id.name,
            'lang': self.vendor_id.vendor_id.lang,
            'price': self.vendor_id.quoted_price,
            'delivery_date': self.vendor_id.estimate_date,
            'currency_id': self.vendor_id.currency_id
        }
        email_values = {
            'email_to': self.vendor_id.vendor_id.email,
            'email_from': self.env.user.partner_id.email,
        }
        self.env['mail.template'].browse(template_id).with_context(
            context).send_mail(self.vendor_id.quote_id.id,
                               email_values=email_values,
                               force_send=True)
        rfq.write({
            'approved_vendor_id': self.vendor_id.vendor_id.id,
            'state': 'done'
        })
