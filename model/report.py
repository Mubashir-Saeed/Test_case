from odoo import models, fields, api, _
from datetime import datetime
from time import gmtime, strftime
from datetime import timedelta


class HospitalReport(models.Model):
    _name = 'hospital.report'
    _description = 'Hospital Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'lab_id'

    @api.model
    def create(self, vals):
        if vals.get('lab_id', _('New')) == _('New'):
            vals['lab_id'] = self.env['ir.sequence'].next_by_code('hospital.report.sequence') or _('New')
        result = super(HospitalReport, self).create(vals)
        return result

    def delete_lines(self):
        for rec in self:
            rec.state = 'delete'
            # print('rec', rec)
            # rec.appointment_lines = [(5, 0, 0)]

    def action_process(self):
        for rec in self:
            rec.state = 'process'

    def action_deliver(self):
        for rec in self:
            rec.state = 'deliver'

    @api.depends('report_test_id.test_price')
    def get_price(self):
        for rec in self:
            if rec.report_test_id:
                i = 0
                for test in rec.report_test_id:
                    i += test.test_price
                rec.update({
                    'report_total_price': i
                })

    @api.onchange('report_type')
    def set_price(self):
        for rec in self:
            if rec.report_type == 'urgent':
                rec.report_total_price = rec.report_total_price + 300

    @api.onchange('report_test_id')
    def get_date(self):
        for rec in self:
            current_date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            date_1 = datetime.strptime(current_date, "%Y-%m-%d %H:%M:%S")
            highest = 0
            for duration in rec.report_test_id:
                if int(duration.test_duration) > highest:
                    highest = int(duration.test_duration)
            new_date = date_1 + timedelta(days=highest)
            rec.report_delivery_date = new_date

    lab_id = fields.Char(string='Report ID', required=True, copy=False, readonly=True,
                         index=True, default=lambda self: _('New'))
    report_patient_id = fields.Many2one('hospital.patient', string='Patient ID')
    report_date = fields.Date(string='Date', default=datetime.today(), required=True)
    report_delivery_date = fields.Date(string='Report Deliver Date', required=True, compute='get_date')
    report_test_id = fields.One2many('hospital.report.lines','patient_report', string='Test ID')
    report_total_price = fields.Integer(string='Total Price', compute='get_price', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('process', 'In-process'),
        ('deliver', 'Delivered'),
        ('delete', 'Canceled')
    ], string='Status', readonly=True, default='draft')
    report_type = fields.Selection([
        ('casual', 'Casual'),
        ('urgent', 'Urgent'), ], default='casual', string="Report Type")


class HospitalReportLines(models.Model):
    _name = 'hospital.report.lines'
    _description = 'Report Lines'

    patient_report = fields.Many2one('hospital.report', string='Patient Report')
    patient_test = fields.Many2one('hospital.test', string='Patient Test')
    patient_test_name = fields.Char(string='Test Name', related='patient_test.test_short_name')
    test_price = fields.Integer(string='Test Price', related='patient_test.test_price')
    test_duration = fields.Selection(String='Test Duration', related='patient_test.test_duration')