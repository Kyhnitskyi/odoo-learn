from odoo import api, fields, models


class HrHospitalPatient(models.Model):
    """Пацієнт: контактні дані, персональний лікар, історія та візити."""

    _name = 'hr.hospital.patient'
    _inherit = ['hr.hospital.medic.info']
    _description = 'Пацієнт'
    _order = 'name'

    name = fields.Char(
        string='ПІБ пацієнта',
        required=True,
    )
    phone = fields.Char(
        string='Телефон',
    )
    email = fields.Char(
        string='Email',
    )
    insurance_number = fields.Char(
        string='Номер страхового поліса',
        size=20,
    )
    personal_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Персональний лікар',
        ondelete='set null',
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Користувач',
        ondelete='set null',
        help='Користувач системи, пов’язаний із цим пацієнтом. '
             'Використовується для обмеження доступу пацієнта '
             'лише до власних візитів.',
    )
    doctor_history_ids = fields.One2many(
        comodel_name='hr.hospital.doctor.history',
        inverse_name='patient_id',
        string='Історія персональних лікарів',
    )
    visit_ids = fields.One2many(
        comodel_name='hr.hospital.visit',
        inverse_name='patient_id',
        string='Візити',
    )
    visit_count = fields.Integer(
        string='Кількість візитів',
        compute='_compute_visit_count',
    )
    active = fields.Boolean(
        string='Активний',
        default=True,
    )

    @api.depends('visit_ids')
    def _compute_visit_count(self):
        """Порахувати кількість візитів пацієнта."""
        for record in self:
            record.visit_count = len(record.visit_ids)

    def action_view_visits(self):
        """Відкрити список візитів цього пацієнта."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Візити пацієнта',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
            'target': 'current',
        }

    def action_quick_visit_wizard(self):
        """Відкрити візард швидкого запису пацієнта до лікаря."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Записатись до лікаря',
            'res_model': 'quick.visit.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
                'default_doctor_id': self.personal_doctor_id.id
                if self.personal_doctor_id
                else False,
            },
        }
