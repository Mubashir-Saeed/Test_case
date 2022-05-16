from odoo import models, fields, api, _


class HospitalDashboard(models.Model):
    _name = 'hospital.dashboard'
    _description = 'Hospital Dashboard'

    @api.onchange('dashboard_patient_id')
    def set_report_id(self):
        for rec in self:
            reports = self.env['hospital.report'].search([('report_patient_id', '=', rec.dashboard_patient_id.id)])
            print('reports is', reports)
            if rec.dashboard_patient_id:
                rec.dashboard_report_ids = reports
                print(rec.dashboard_report_ids)

    dashboard_patient_id = fields.Many2one('hospital.patient', string='Patient')
    dashboard_report_ids = fields.One2many('hospital.report', 'report_patient_id', string='Report')
