from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'account.move'

    installment_ids=fields.One2many('installment.installment', 'account_id',string='installment')



