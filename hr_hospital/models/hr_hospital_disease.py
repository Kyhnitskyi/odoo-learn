from odoo import fields, models


class HrHospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Вид захворювання'
    _order = 'name'

    name = fields.Char(
        string='Назва захворювання',
        required=True,
    )
    description = fields.Text(
        string='Опис',
    )
    active = fields.Boolean(
        string='Активний',
        default=True,
    )
