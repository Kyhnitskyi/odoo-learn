from odoo import fields, models


class HrHospitalDoctorCategory(models.Model):
    """Кваліфікаційна категорія лікаря (довідник)."""

    _name = 'hr.hospital.doctor.category'
    _description = 'Кваліфікація лікаря'
    _order = 'sequence, name'

    name = fields.Char(
        string='Назва',
        required=True,
    )
    sequence = fields.Integer(
        string='Послідовність',
        default=10,
    )
    doctor_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='category_id',
        string='Лікарі',
    )

    _name_uniq = models.Constraint(
        'UNIQUE(name)',
        'Назва кваліфікації лікаря повинна бути унікальною!',
    )
