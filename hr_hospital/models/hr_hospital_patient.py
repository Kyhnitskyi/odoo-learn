from odoo import fields, models


class HrHospitalPatient(models.Model):
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
    active = fields.Boolean(
        string='Активний',
        default=True,
    )
