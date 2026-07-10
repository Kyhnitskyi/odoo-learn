from odoo import fields, models


class QuickVisitWizard(models.TransientModel):
    _name = 'quick.visit.wizard'
    _description = 'Швидкий запис на прийом'

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Пацієнт',
        required=True,
    )
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Лікар',
        required=True,
    )
    scheduled_date = fields.Datetime(
        string='Дата та час',
        required=True,
        default=fields.Datetime.now,
    )
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Хвороба',
    )
    notes = fields.Text(
        string='Нотатки',
    )

    def action_create_visit(self):
        self.ensure_one()
        visit = self.env['hr.hospital.visit'].create({
            'patient_id': self.patient_id.id,
            'doctor_id': self.doctor_id.id,
            'scheduled_date': self.scheduled_date,
            'disease_id': self.disease_id.id if self.disease_id else False,
            'notes': self.notes,
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Візит',
            'res_model': 'hr.hospital.visit',
            'res_id': visit.id,
            'view_mode': 'form',
            'target': 'current',
        }
