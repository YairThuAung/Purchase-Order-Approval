from odoo import fields, models

class Company(models.Model):
    _inherit = 'res.company'

    steps_id = fields.Boolean('PO Three Step')
    po_first_person_ammount = fields.Monetary("Manager Amount",default=100)
    po_second_person_ammount = fields.Monetary("Finance Amount",default=1000)
    po_third_person_ammount = fields.Monetary("Director Amount",default=1000)
