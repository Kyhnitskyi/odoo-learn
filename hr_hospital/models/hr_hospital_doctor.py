from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrHospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _inherit = ['hr.hospital.medic.info']
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
    email = fields.Char()
    supervising_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Лікар, що спостерігає',
        ondelete='set null',
    )
    category_id = fields.Many2one(
        comodel_name='hr.hospital.doctor.category',
        string='Категорія',
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Користувач системи',
    )
    is_intern = fields.Boolean(
        string='Лікар є інтерном',
        compute='_compute_is_intern',
        store=True,
    )
    mentor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Ментор',
        ondelete='set null',
    )
    intern_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='mentor_id',
        string='Інтерни',
    )
    patient_ids = fields.One2many(
        comodel_name='hr.hospital.patient',
        inverse_name='personal_doctor_id',
        string='Пацієнти',
    )
    visit_ids = fields.One2many(
        comodel_name='hr.hospital.visit',
        inverse_name='doctor_id',
        string='Візити',
    )
    intern_names = fields.Char(
        string='Список інтернів',
        compute='_compute_intern_names',
    )
    active = fields.Boolean(
        string='Активний',
        default=True,
    )

    @api.depends('intern_ids.name')
    def _compute_intern_names(self):
        for record in self:
            record.intern_names = ', '.join(record.intern_ids.mapped('name'))

    @api.depends('category_id')
    def _compute_is_intern(self):
        intern_category = self.env.ref(
            'hr_hospital.doctor_category_intern', raise_if_not_found=False
        )
        for record in self:
            record.is_intern = bool(
                intern_category and record.category_id == intern_category
            )

    def action_quick_visit_to_doctor(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Записатись до лікаря',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_doctor_id': self.id},
        }

    @api.constrains('mentor_id')
    def _check_mentor_is_not_intern(self):
        for record in self:
            if record.mentor_id and record.mentor_id.is_intern:
                raise ValidationError(
                    self.env._(
                        'Ментором не може бути лікар, який є інтерном.'
                    )
                )
