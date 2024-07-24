from odoo import api, fields, models

class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Purchase Request'
    # _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age')
    requested_by = fields.Many2one(
        'res.users',
        string='Requested By',
        # required=True,
        # default=lambda self: self.env.user
    )
    Start_date = fields.Date(string='Start Date')
    End_date = fields.Date(string='End Date')
    rejection_reason = fields.Text(string="rejection reason")
    orderlines = fields.One2many(
        'purchase.request.line',
        'request_id',
        string='Order Lines'
    )
    status = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'To be Approved'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft')

    def action_submit_for_approval(self):
        print("approve")
        self.status = 'to_approve'
    def action_cancel (self):
        self.status = 'cancelled'
    def action_reset_to_draft(self):
        self.status = 'draft'
    def action_approve(self):
        self.status = 'approved'
        temp=self.env.ref('purchase_enhancement.email_temp_name')
        group_purchase_manager = self.env.ref('purchase.group_purchase_manager')
        managers = group_purchase_manager.users
        for user in managers:
                if user.email:
                    temp.send_mail(self.id, email_values={'email_to': user.email}, force_send=True)

class PurchaseRequestLine(models.Model):
        _name = 'purchase.request.line'
        _description = 'Purchase Request Line'

        request_id = fields.Many2one(
            'purchase.request',
            string='Purchase Request',
        )
        product_id = fields.Many2one(
            'product.product',
            string='Product',
            required=True
        )

        description = fields.Char(
            string='Description',
            related='product_id.name',
            readonly=True
        )

        quantity = fields.Float(
            string='Quantity',
            default=1
        )

        cost_price = fields.Float(
            string='Cost Price',
            related='product_id.standard_price',
            readonly=True
        )

        total = fields.Float(
            string='Total',
            compute='_compute_total',
            readonly=True
        )
        def _compute_total(self):
            for rec in self:
                rec.total = rec.quantity * rec.cost_price