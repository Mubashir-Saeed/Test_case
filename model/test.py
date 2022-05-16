from odoo import models, fields, api, _


class HospitalTest(models.Model):
    _name = 'hospital.test'
    _description = 'Hospital Test'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'test_name'

    @api.model
    def create(self, vals):
        if vals.get('lab_id', _('New')) == _('New'):
            vals['lab_id'] = self.env['ir.sequence'].next_by_code('hospital.test.sequence') or _('New')
        result = super(HospitalTest, self).create(vals)
        return result

    lab_id = fields.Char(string='Test ID', required=True, copy=False, readonly=True,
                         index=True, default=lambda self: _('New'))
    test_name = fields.Char(string='Test Name',  track_visibility='always')
    test_short_name = fields.Char(String='Test Short Name')
    test_duration = fields.Selection([
        ('1', '1 Day'),('2', '2 Day'),('3', '3 Day'),('4', '4 Day'),('5', '5 Day'),
        ('6', '6 Day'), ('7', '7 Day'),('8', '8 Day'), ], default='1', string="Duration Day")
    test_price = fields.Integer(string='Price', track_visibility='always')


