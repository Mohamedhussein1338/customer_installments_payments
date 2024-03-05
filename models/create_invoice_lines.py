from odoo import models, fields, api


class CreareInvoiceLines(models.Model):
    _name = 'create.invoice.lines'
    _description = 'create invoice Line'

    product_id = fields.Many2one('product.product', string='Product')
    account_id = fields.Many2one('account.move', string='account name')
    quantity = fields.Float(string='Quantity')
    price_id = fields.Integer(string="Price")
    installment_id = fields.Many2one('installment.installment', string='installment')