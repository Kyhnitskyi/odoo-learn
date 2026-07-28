from odoo import api, fields, models


class HrHospitalDoctorHistory(models.Model):
    """Історія призначень персонального лікаря пацієнту."""

    _name = 'hr.hospital.doctor.history'
    _description = 'Історія персональних лікарів'
    _order = 'assignment_date desc, id desc'

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Пацієнт',
        required=True,
        ondelete='cascade',
    )
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Лікар',
        required=True,
        ondelete='restrict',
    )
    assignment_date = fields.Date(
        string='Дата призначення',
        required=True,
        default=fields.Date.context_today,
    )
    change_date = fields.Date(
        string='Дата зміни лікаря',
    )
    active = fields.Boolean(
        string='Активний',
        default=True,
    )

    @api.onchange('assignment_date', 'change_date')
    def _onchange_dates_check(self):
        """Попередити, якщо дата зміни лікаря раніша за дату призначення."""
        if (
            self.assignment_date
            and self.change_date
            and self.change_date < self.assignment_date
        ):
            return {
                'warning': {
                    'title': 'Попередження',
                    'message': (
                        'Дата зміни лікаря не може бути раніше ніж '
                        'дата призначення'
                    ),
                }
            }

    @api.depends(
        'patient_id.name',
        'doctor_id.name',
        'doctor_id.category_id.name',
        'assignment_date',
    )
    def _compute_display_name(self):
        """Побудувати назву запису як "Пацієнт - Лікар (Категорія) Дата"."""
        for record in self:
            category_name = record.doctor_id.category_id.name or ''
            record.display_name = '%s - %s (%s) %s' % (
                record.patient_id.name or '',
                record.doctor_id.name or '',
                category_name,
                record.assignment_date or '',
            )
