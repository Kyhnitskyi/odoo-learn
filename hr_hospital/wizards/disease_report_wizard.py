from datetime import datetime, time

from odoo import api, fields, models


class DiseaseReportWizard(models.TransientModel):
    _name = 'disease.report.wizard'
    _description = 'Звіт по хворобах за місяць'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Лікарі',
    )
    disease_ids = fields.Many2many(
        comodel_name='hr.hospital.disease',
        string='Хвороби',
    )
    date_from = fields.Date(
        string='Дата з',
        required=True,
    )
    date_to = fields.Date(
        string='Дата по',
        required=True,
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids', [])
        if active_model == 'hr.hospital.doctor' and active_ids:
            res['doctor_ids'] = [(6, 0, active_ids)]
        return res

    def action_generate_report(self):
        self.ensure_one()
        domain = []
        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))
        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))
        if self.date_from:
            domain.append((
                'scheduled_date', '>=',
                datetime.combine(self.date_from, time.min),
            ))
        if self.date_to:
            domain.append((
                'scheduled_date', '<=',
                datetime.combine(self.date_to, time.max),
            ))
        return {
            'type': 'ir.actions.act_window',
            'name': 'Звіт по хворобах',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'domain': domain,
            'context': {'group_by': 'disease_id'},
            'target': 'current',
        }
