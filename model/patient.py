from odoo import models, fields, api, _


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'lab_id'

    @api.model
    def create(self, vals):
        if vals.get('lab_id', _('New')) == _('New'):
            vals['lab_id'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient, self).create(vals)
        return result

    def open_hospital_patient(self):
        return {
            'name': _('Reports'),
            'domain': [('report_patient_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'hospital.report',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def get_test_count(self):
        count = self.env['hospital.report'].search_count([('report_patient_id', '=', self.id)])
        self.patient_test_count = count

    name = fields.Char(string='name')
    patient_name = fields.Char(string='Name', track_visibility='always')
    patient_age = fields.Integer(sting='Age', track_visibility='always')
    patient_gender = fields.Selection([
        ('male', 'Male'),
        ('fe_male', 'Female'), ], default='male', string="Gender")
    patient_address = fields.Text(string='Address', track_visibility='always')
    street2 = fields.Text(string='Street 2', track_visibility='always')
    city = fields.Char(string='city', track_visibility='always')
    state_id = fields.Many2one('res.country.state', string='state_id', track_visibility='always')
    zip = fields.Char('zip', track_visibility='always')
    country_id = fields.Many2one('res.country','country_id', track_visibility='always')
    patient_mobile = fields.Char(string='Mobile')
    lab_id = fields.Char(string='Patient ID', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    patient_test_count = fields.Integer(string='Test', compute='get_test_count')



