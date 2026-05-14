from odoo import fields, models


class HrHospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Візит пацієнта'
    _order = 'visit_date desc'

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
        string='Діагноз (вид захворювання)',
        ondelete='set null',
    )
    visit_date = fields.Datetime(
        string='Дата та час візиту',
        required=True,
        default=fields.Datetime.now,
    )
    notes = fields.Text(
        string='Нотатки лікаря',
    )
    state = fields.Selection(
        selection=[
            ('scheduled', 'Заплановано'),
            ('in_progress', 'В процесі'),
            ('done', 'Завершено'),
            ('cancelled', 'Скасовано'),
        ],
        string='Статус',
        default='scheduled',
        required=True,
    )
