from datetime import datetime, time

from odoo import api, fields, models


class VisitReportWizard(models.TransientModel):
    _name = 'visit.report.wizard'
    _description = 'Звіт по візитах пацієнтів'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Лікарі',
    )
    patient_ids = fields.Many2many(
        comodel_name='hr.hospital.patient',
        string='Пацієнти',
    )
    date_from = fields.Date(
        string='Початок періоду',
    )
    date_to = fields.Date(
        string='Кінець періоду',
    )
    only_done = fields.Boolean(
        string='Лише завершені візити',
    )
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Хвороба',
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids', [])

        if active_model == 'hr.hospital.doctor' and active_ids:
            res['doctor_ids'] = [(6, 0, active_ids)]
        elif active_model == 'hr.hospital.patient' and active_ids:
            res['patient_ids'] = [(6, 0, active_ids)]

        return res

    def action_generate_report(self):
        self.ensure_one()
        domain = []

        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))
        if self.patient_ids:
            domain.append(('patient_id', 'in', self.patient_ids.ids))
        if self.date_from:
            domain.append((
                'scheduled_date', '>=',
                datetime.combine(self.date_from, time.min),
            ))
        if self.date_to:
            domain.append((
                'scheduled_date', '<=',
                datetime.combine(self.date_to, time.max),
            ))
        if self.only_done:
            domain.append(('state', '=', 'done'))
        if self.disease_id:
            domain.append(('disease_id', '=', self.disease_id.id))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Звіт по візитах пацієнтів',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'domain': domain,
            'target': 'current',
        }
