from odoo import api, fields, models

class RejectionWizard(models.TransientModel):
    _name="rejection.wizard"
    _description="rejection wizard"
    rejection_reason = fields.Text(string="rejection reason",required=True)

    def action_confirm(self):
        active_id = self._context.get('active_id')
        purchase_request = self.env['purchase.request'].browse(active_id)
        purchase_request.write({
            'rejection_reason':self.rejection_reason,
            'status':'rejected'
        })
        # purchase_request.rejection_reason = self.rejection_reason
        # purchase_request.status = 'rejected'
        return {'type': 'ir.actions.act_window_close'}
