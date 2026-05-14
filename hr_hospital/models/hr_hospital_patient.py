from odoo import fields, models


class HrHospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'Пацієнт'
    _order = 'name'

    name = fields.Char(
        string='ПІБ пацієнта',
        required=True,
    )
    birth_date = fields.Date(
        string='Дата народження',
    )
    gender = fields.Selection(
        selection=[
            ('male', 'Чоловіча'),
            ('female', 'Жіноча'),
            ('other', 'Інша'),
        ],
        string='Стать',
    )
    phone = fields.Char(
        string='Телефон',
    )
    email = fields.Char(
        string='Email',
    )
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Лікуючий лікар',
        ondelete='set null',
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
