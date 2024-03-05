from odoo import models, fields, api

class InstallmentPaymentWizard(models.TransientModel):
    _name = 'installment.payment.wizard'
    _description = 'Installment Payment Wizard'

    installment_id = fields.Many2one('installment.installment', string='Installment')
    amount = fields.Float(string='Payment Amount', required=True)


    def action_confirm_payment(self):
        installment = self.installment_id
        amount_paid = self.amount

        installment.amount_paid = amount_paid

        if installment.amount_paid >= installment.amount:
            installment.state = 'paid'

        return {'type': 'ir.actions.act_window_close'}
