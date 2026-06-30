from odoo import fields, models


class MassReassignDoctorWizard(models.TransientModel):
    _name = 'mass.reassign.doctor.wizard'
    _description = 'Масове перевизначення персонального лікаря'

    new_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Новий лікар',
        required=True,
    )
    change_date = fields.Date(
        string='Дата зміни',
        required=True,
        default=fields.Date.context_today,
    )

    def action_reassign_doctor(self):
        self.ensure_one()
        patient_model = self.env['hr.hospital.patient']
        history_model = self.env['hr.hospital.doctor.history']

        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids', [])
        if active_model != 'hr.hospital.patient' or not active_ids:
            return {'type': 'ir.actions.act_window_close'}

        patients = patient_model.browse(active_ids)
        for patient in patients:
            current_history = history_model.search(
                [
                    ('patient_id', '=', patient.id),
                    ('active', '=', True),
                ],
                limit=1,
            )
            if current_history and current_history.doctor_id != self.new_doctor_id:
                current_history.write({
                    'change_date': self.change_date,
                    'active': False,
                })

            if not current_history or current_history.doctor_id != self.new_doctor_id:
                history_model.create({
                    'patient_id': patient.id,
                    'doctor_id': self.new_doctor_id.id,
                    'assignment_date': self.change_date,
                })

            patient.personal_doctor_id = self.new_doctor_id.id

        return {'type': 'ir.actions.act_window_close'}
