from odoo import api, fields, models
from odoo.exceptions import UserError


class HrHospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Візит пацієнта'
    _order = 'scheduled_date desc'

    name = fields.Char(
        string='Номер візиту',
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
    visit_same_disease_count = fields.Integer(
        string='Візитів з такою ж хворобою',
        compute='_compute_visit_same_disease_count',
    )

    _LOCKED_FIELDS = ('scheduled_date', 'doctor_id', 'actual_date')

    @api.depends('disease_id')
    def _compute_visit_same_disease_count(self):
        for record in self:
            if record.disease_id:
                record.visit_same_disease_count = self.env[
                    'hr.hospital.visit'
                ].search_count([('disease_id', '=', record.disease_id.id)])
            else:
                record.visit_same_disease_count = 0

    def action_view_same_disease_visits(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Візити: %s' % (self.disease_id.name or ''),
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'domain': [('disease_id', '=', self.disease_id.id)],
            'target': 'current',
        }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'hr.hospital.visit'
                ) or '/'
        return super().create(vals_list)

    def write(self, vals):
        if any(field_name in vals for field_name in self._LOCKED_FIELDS) or (
            vals.get('active') is False
        ):
            for record in self:
                if record.state == 'done':
                    if vals.get('active') is False:
                        raise UserError(
                            self.env._(
                                'Неможливо архівувати візит, що вже відбувся.'
                            )
                        )
                    raise UserError(
                        self.env._(
                            'Неможливо змінити дату, час або лікаря візиту, '
                            'що вже відбувся.'
                        )
                    )
        return super().write(vals)

    def unlink(self):
        for record in self:
            if record.state == 'done':
                raise UserError(
                    self.env._('Неможливо видалити візит, що вже відбувся.')
                )
        return super().unlink()
