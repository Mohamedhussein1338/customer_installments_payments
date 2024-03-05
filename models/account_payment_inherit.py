from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'account.payment'

    installments_id = fields.Many2one('installment.installment', string='Installments ')
