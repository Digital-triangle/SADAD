from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import requests

class PaymentAcquirerSadad(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('sadad', 'Sadad')])
    sadad_merchant_id = fields.str('sadadId', required_if_provider='sadad')
    sadad_terminal_id = fields.int('secretKey', required_if_provider='sadad')
    sadad_merchant_id = fields.str('domain', required_if_provider='sadad')
    sadad_username = fields.Char('Sadad Username', required_if_provider='sadad')
    sadad_password = fields.Char('Sadad Password', required_if_provider='sadad')

    def sadad_form_generate_values(self, values):
        self.ensure_one()
        sadad_tx_values = dict(values)
        # Pass the values as per doc
        
        sadad_tx_values.update({
            'clientname': values['name'].name,
            'amount': values['amount'].name,
           # remaining values to be parsed as per doc
        })
        return sadad_tx_values

    def sadad_get_form_action_url(self):
        self.ensure_one()
        return '/payment/sadad/redirect/'

class PaymentTransactionSadad(models.Model):
    _inherit = 'payment.transaction'

    sadad_txn_id = fields.Char('Sadad Transaction ID')

    @api.model
    def _sadad_form_get_tx_from_data(self, data):
        return self.env['payment.transaction'].sudo().search([('reference', '=', data.get('reference'))])

    def _sadad_form_get_invalid_parameters(self, data):
        invalid_parameters = []

        # validation logic to be added based on the response from Sadad
        

        return invalid_parameters

    def _sadad_form_validate(self, data):
        if data.get('status') == 'success':
            self.write({
                'state': 'done',
                'date': fields.Datetime.now(),
                'acquirer_reference': data.get('acquirer_reference'),
                'sadad_txn_id': data.get('sadad_txn_id')
            })
            return True
        elif data.get('status') == 'failure':
            self.write({
                'state': 'error',
                'state_message': data.get('error_message', _('Transaction error')),
            })
            return False
        else:
            self.write({
                'state': 'pending',
                'state_message': _('Received unrecognized status for payment'),
            })
            return False

class PaymentControllerSadad(models.AbstractModel):
    _inherit = 'payment.controller'

    @api.model
    def _sadad_form_validate(self, data):
        # call API validations
        # and return True if the payment is successful, otherwise return False
        return True
