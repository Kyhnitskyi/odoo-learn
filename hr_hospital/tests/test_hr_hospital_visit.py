from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestHrHospitalVisit(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.doctor = cls.env['hr.hospital.doctor'].create({
            'name': 'Лікар Тестовий',
        })
        cls.patient = cls.env['hr.hospital.patient'].create({
            'name': 'Пацієнт Тестовий',
        })

    def _create_visit(self, **extra_vals):
        vals = {
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
        }
        vals.update(extra_vals)
        return self.env['hr.hospital.visit'].create(vals)

    def test_create_assigns_sequence_name(self):
        """create() must auto-assign a sequence-based name when none is given."""
        visit = self._create_visit()
        self.assertTrue(visit.name)
        self.assertTrue(visit.name.startswith('VISIT/'))

    def test_create_keeps_explicit_name(self):
        visit = self._create_visit(name='CUSTOM-NAME')
        self.assertEqual(visit.name, 'CUSTOM-NAME')

    def test_write_blocks_locked_fields_when_done(self):
        """Once a visit is done, scheduled_date/doctor_id/actual_date cannot change."""
        visit = self._create_visit()
        visit.write({'state': 'done'})
        with self.assertRaises(UserError):
            visit.write({'scheduled_date': '2030-01-01 10:00:00'})

    def test_write_blocks_archiving_when_done(self):
        visit = self._create_visit()
        visit.write({'state': 'done'})
        with self.assertRaises(UserError):
            visit.write({'active': False})

    def test_write_allows_locked_fields_when_not_done(self):
        visit = self._create_visit()
        visit.write({'scheduled_date': '2030-01-01 10:00:00'})
        self.assertEqual(str(visit.scheduled_date), '2030-01-01 10:00:00')

    def test_unlink_blocks_done_visit(self):
        visit = self._create_visit()
        visit.write({'state': 'done'})
        with self.assertRaises(UserError):
            visit.unlink()

    def test_unlink_allows_non_done_visit(self):
        visit = self._create_visit()
        visit.unlink()
        self.assertFalse(visit.exists())
