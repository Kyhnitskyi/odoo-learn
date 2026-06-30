from datetime import date

from odoo import api, fields, models


class HrHospitalMedicInfo(models.AbstractModel):
    _name = 'hr.hospital.medic.info'
    _description = 'Загальна медична інформація'

    blood_type = fields.Selection(
        selection=[
            ('o_plus', 'O (I) Rh+'),
            ('o_minus', 'O (I) Rh-'),
            ('a_plus', 'A (II) Rh+'),
            ('a_minus', 'A (II) Rh-'),
            ('b_plus', 'B (III) Rh+'),
            ('b_minus', 'B (III) Rh-'),
            ('ab_plus', 'AB (IV) Rh+'),
            ('ab_minus', 'AB (IV) Rh-'),
        ],
        string='Група крові',
    )
    gender = fields.Selection(
        selection=[
            ('male', 'Чоловіча'),
            ('female', 'Жіноча'),
        ],
        string='Стать',
    )
    birth_date = fields.Date(
        string='Дата народження',
    )
    age = fields.Integer(
        string='Вік',
        compute='_compute_age',
    )

    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.birth_date:
                years = today.year - record.birth_date.year
                if (today.month, today.day) < (record.birth_date.month, record.birth_date.day):
                    years -= 1
                record.age = years
            else:
                record.age = 0
