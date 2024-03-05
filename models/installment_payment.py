from odoo import models, fields, api

class InstallmentPayment(models.Model):
    _name = 'installment.payment'
    _description = 'Installment Payments'

    installment_id = fields.Many2one('installment.installment', string='Installment')
    payment_date = fields.Date(string='Payment Date', default=fields.Date.context_today)
    payment_amount = fields.Float(string='Payment Amount', required=True, digits=(16, 2))
