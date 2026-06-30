from odoo import fields, models
from odoo.exceptions import UserError


class HrHospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Візит пацієнта'
    _order = 'scheduled_date desc'

    name = fields.Char(
        string='Номер візиту',
        readonly=True,
        default='/',
    )
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
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Хвороба',
        ondelete='set null',
    )
    scheduled_date = fields.Datetime(
        string='Запланована дата та час візиту',
        required=True,
        default=fields.Datetime.now,
    )
    actual_date = fields.Datetime(
        string='Дата та час фактичного візиту',
    )
    summary = fields.Html(
        string='Епікриз',
    )
    notes = fields.Text(
        string='Нотатки лікаря',
    )
    state = fields.Selection(
        selection=[
            ('scheduled', 'Заплановано'),
            ('done', 'Завершено'),
            ('cancelled', 'Скасовано'),
        ],
        string='Статус візиту',
        default='scheduled',
        required=True,
    )
    active = fields.Boolean(
        string='Активний',
        default=True,
    )

    _LOCKED_FIELDS = ('scheduled_date', 'doctor_id', 'actual_date')

    def write(self, vals):
        if any(field_name in vals for field_name in self._LOCKED_FIELDS) or (
            vals.get('active') is False
        ):
            for record in self:
                if record.state == 'done':
                    if vals.get('active') is False:
                        raise UserError(
                            'Неможливо архівувати візит, що вже відбувся.'
                        )
                    raise UserError(
                        'Неможливо змінити дату, час або лікаря візиту, '
                        'що вже відбувся.'
                    )
        return super().write(vals)

    def unlink(self):
        for record in self:
            if record.state == 'done':
                raise UserError('Неможливо видалити візит, що вже відбувся.')
        return super().unlink()
