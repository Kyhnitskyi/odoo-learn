from odoo import fields, models


class HrHospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = 'Лікар'
    _order = 'name'

    name = fields.Char(
        string='ПІБ лікаря',
        required=True,
    )
    specialization = fields.Char(
        string='Спеціалізація',
    )
    phone = fields.Char(
        string='Телефон',
    )
    email = fields.Char(
        string='Email',
    )
    supervising_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Лікар, що спостерігає',
        ondelete='set null',
    )
    patient_ids = fields.One2many(
        comodel_name='hr.hospital.patient',
        inverse_name='doctor_id',
        string='Пацієнти',
    )
    active = fields.Boolean(
        string='Активний',
        default=True,
    )
