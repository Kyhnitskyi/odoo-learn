from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrHospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Вид захворювання'
    _order = 'name'
    _parent_name = 'parent_id'
    _parent_store = True

    name = fields.Char(
        string='Назва захворювання',
        required=True,
    )
    description = fields.Text(
        string='Опис',
    )
    parent_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Батьківське захворювання',
        ondelete='restrict',
        index=True,
    )
    parent_path = fields.Char(
        index=True,
    )
    child_ids = fields.One2many(
        comodel_name='hr.hospital.disease',
        inverse_name='parent_id',
        string='Підвиди захворювання',
    )
    active = fields.Boolean(
        string='Активний',
        default=True,
    )

    @api.constrains('parent_id')
    def _check_parent_recursion(self):
        if not self._check_recursion():
            raise ValidationError(
                'Неможливо встановити батьківське захворювання: '
                'виявлено циклічну залежність.'
            )

    @api.depends('name', 'parent_id')
    def _compute_display_name(self):
        for record in self:
            names = []
            current = record
            visited_ids = set()
            while current and current.id not in visited_ids:
                names.append(current.name)
                visited_ids.add(current.id)
                current = current.parent_id
            record.display_name = ' / '.join(reversed(names))
