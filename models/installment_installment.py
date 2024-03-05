from odoo import models, fields, api,_
from odoo.exceptions import ValidationError


class InstallmentInstallment(models.Model):
    _name = 'installment.installment'
    _description = 'Customer Installments and Payments'

    name = fields.Char(string='Name', )
    reference = fields.Char(string='Reference',readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('open', 'Open'), ('paid', 'Paid')],  string='State')
    date = fields.Date(string='Date', default=fields.Date.context_today)
    customer = fields.Many2one('res.partner', string='Customer', required=True)
    journal = fields.Many2one('account.journal', string='Journal', required=True)
    account = fields.Many2one('account.account', string='Account', required=True)
    analytic_account = fields.Many2one('account.analytic.account', string='Analytic Account')
    analytic_tags = fields.Many2many('account.analytic.tag', string='Analytic Tags')
    amount = fields.Float(string=' Total Amount', )
    notes = fields.Text(string='Notes')
    payment_ids = fields.One2many('installment.payment', 'installment_id', string='Payments')
    payments_id=fields.One2many('account.payment' ,  'installments_id' , string='payment account')
    account_id=fields.Many2one('account.move',string='account name')
    invoice_lines_ids=fields.One2many('create.invoice.lines','installment_id')
    amount_paid = fields.Float(string='Amount Paid',  store=True)

    # create sequence like INS/24/03/05/0001
    @api.model
    def create(self, vals):
        res = super(InstallmentInstallment, self).create(vals)
        ir_sequence = self.env['ir.sequence'].sudo().create({
            'name': _("Installment_customer"),
            'padding': 4,
            'code': 'seq.installment',
            'number_next': 1,
            'number_increment': 1,
            'use_date_range': True,
            'prefix': 'INS/%(y)s/%(month)s/%(day)s/',
        })
        res.reference = ir_sequence.next_by_code('seq.installment')
        return res
    # 	- Delete and edit is only allowed in "draft" State.
    def write(self, vals):
        # Check if state is 'draft' before allowing the write operation
        for installment in self:
            if installment.state != 'draft':
                raise ValueError("You can only edit installments in 'draft' state.")
        return super(InstallmentInstallment, self).write(vals)

    def unlink(self):
        # Check if state is 'draft' before allowing the unlink operation
        for installment in self:
            if installment.state != 'draft':
                raise ValueError("You can only delete installments in 'draft' state.")
        return super(InstallmentInstallment, self).unlink()



    def action_open_payments(self):
        return {
            'name': '  payments created',
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.payments_id.ids)]

        }


    # Creates a customer invoice
    def action_create_invoice(self):
            invoice_lines = []
            for invoice in self.invoice_lines_ids:
                invoice_lines.append(
                    (0, 0, {
                        'product_id': invoice.product_id.id,
                        'product_uom_qty': invoice.quantity,
                        'price_unit': invoice.price_id,
                        'account_id': invoice.account_id,
                        # 'product_uom_qty': 1,

                    })
                )
            account_id = self.env['account.move'].create({
                'partner_id': self.customer.id,
                'journal_id': self.journal.id,
                'move_type': 'out_invoice',

                'ref': self.reference,
                'invoice_date': self.date,
                'amount_total': self.amount,
                # 'date_order': self.date_id,
                'invoice_line_ids': invoice_lines,

            })
            self.account_id = account_id.id
    # Creates a customer invoice2
    def action_create_customer_invoice(self):
        for rec in self:
            if rec.state == 'open':
                rec.name = self.env['ir.sequence'].next_by_code('installment.installment') or '/'

                # Prepare data for creating the invoice
                invoice_lines = []
                for invoice_line in rec.invoice_lines_ids:
                    invoice_lines.append((0, 0, {
                        'product_id': invoice_line.product_id.id,
                        'quantity': invoice_line.quantity,
                        'price_unit': invoice_line.price_id,
                        'account_id': invoice_line.account_id.id,
                        # Add other line fields as needed
                    }))

                invoice_data = {
                    'partner_id': rec.customer.id,
                    'journal_id': rec.journal.id,
                    'ref': rec.reference,
                    'invoice_date': rec.date,
                    'amount_total': rec.amount,
                    'invoice_line_ids': invoice_lines,
                }

                # Create the invoice
                invoice = self.env['account.move'].create(invoice_data)

                # Update the installment's state to 'paid'
                rec.write({'state': 'paid', 'account_id': invoice.id})


    # Payment: in wizared
    def action_open_payment_wizard(self):
        return {
            'name': 'Installment Payment Wizard',
            'type': 'ir.actions.act_window',
            'res_model': 'installment.payment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_installment_id': self.id},
        }


    def action_view_invoices(self):
        """Opens a list view of invoices related to the installment."""
        self.ensure_one()
        return {
            'name': _('Invoices'),
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('account_id ', '=', self.id)],
            'type': 'ir.actions.act_window',
        }


