from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
        'approved': [('readonly', True)],
    }

    STATE_SELECTION = [ ('draft', 'RFQ'), ('sent', 'RFQ Sent'), ('to approve', 'Waiting PO Manager Approval'),
                      ('to approve finance', 'Waiting Finance Approval'), ('to approve director', 'Waiting Director Approval'), ('purchase', 'Purchase Order'), 
                      ('done', 'Locked'), ('cancel', 'Cancelled')]

    # Update the readonly states:
    origin = fields.Char(states=READONLY_STATES)
    date_order = fields.Datetime(states=READONLY_STATES)
    partner_id = fields.Many2one(states=READONLY_STATES)
    dest_address_id = fields.Many2one(states=READONLY_STATES)
    currency_id = fields.Many2one(states=READONLY_STATES)
    order_line = fields.One2many(states=READONLY_STATES)
    company_id = fields.Many2one(states=READONLY_STATES)
    picking_type_id = fields.Many2one(states=READONLY_STATES)
    state = fields.Selection(STATE_SELECTION, string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')

    @api.multi
    def action_confirm(self):
        self.write({'state': 'purchase', 'date_approve': fields.Date.context_today(self)})
        self._create_picking()
        self.filtered(
            lambda p: p.company_id.po_lock == 'lock').write({'state': 'done'})
        return {}

    @api.multi
    def button_approve(self, force=False):
        for order in self:
            order._add_supplier_to_product()
            if order.amount_total < self.env.user.company_id.po_first_person_ammount:
                order.action_confirm()
            elif self.env.user.company_id.po_first_person_ammount < order.amount_total < self.env.user.company_id.po_second_person_ammount\
                    :
                order.write({'state': 'to approve finance'})
            else:
                order.write({'state': 'to approve finance'})

    @api.multi
    def button_finance_approve(self, force=False):
        for order in self:
            if order.amount_total > self.env.user.company_id.po_third_person_ammount:
                order.write({'state':'to approve director'})
            else:
                order.action_confirm()

    @api.multi
    def button_director_approve(self, force=False):
        for order in self:
            order.action_confirm()

    @api.multi
    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()
            if order.company_id.steps_id == True:
                if order.amount_total < self.env.user.company_id.po_first_person_ammount\
                        and not order.user_has_groups('purchase.group_purchase_manager'):
                    order.write({'state': 'to approve'})
                elif self.env.user.company_id.po_first_person_ammount < order.amount_total < self.env.user.company_id.po_second_person_ammount\
                        :
                    order.write({'state': 'to approve'})
                else:
                    order.write({'state': 'to approve'})
            else:
                if order.company_id.po_double_validation == 'one_step'\
                        or (order.company_id.po_double_validation == 'two_step'\
                            and order.amount_total < self.env.user.company_id.currency_id.compute(order.company_id.po_double_validation_amount, order.currency_id))\
                        or order.user_has_groups('purchase.group_purchase_manager'):
                    order.action_confirm()
                else:
                    order.write({'state': 'to approve'})
        return True