from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestHrHospitalDoctor(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category_intern = cls.env.ref('hr_hospital.doctor_category_intern')
        cls.category_specialist = cls.env.ref('hr_hospital.doctor_category_specialist')

    def test_compute_is_intern_true_for_intern_category(self):
        doctor = self.env['hr.hospital.doctor'].create({
            'name': 'Інтерн Тестовий',
            'category_id': self.category_intern.id,
        })
        self.assertTrue(doctor.is_intern)

    def test_compute_is_intern_false_for_other_category(self):
        doctor = self.env['hr.hospital.doctor'].create({
            'name': 'Спеціаліст Тестовий',
            'category_id': self.category_specialist.id,
        })
        self.assertFalse(doctor.is_intern)

    def test_compute_is_intern_recomputes_on_category_change(self):
        doctor = self.env['hr.hospital.doctor'].create({
            'name': 'Лікар Тестовий',
            'category_id': self.category_specialist.id,
        })
        self.assertFalse(doctor.is_intern)
        doctor.category_id = self.category_intern
        self.assertTrue(doctor.is_intern)

    def test_mentor_cannot_be_intern(self):
        intern = self.env['hr.hospital.doctor'].create({
            'name': 'Інтерн Менторить',
            'category_id': self.category_intern.id,
        })
        with self.assertRaises(ValidationError):
            self.env['hr.hospital.doctor'].create({
                'name': 'Підопічний',
                'mentor_id': intern.id,
            })

    def test_mentor_can_be_non_intern(self):
        specialist = self.env['hr.hospital.doctor'].create({
            'name': 'Спеціаліст Ментор',
            'category_id': self.category_specialist.id,
        })
        intern = self.env['hr.hospital.doctor'].create({
            'name': 'Інтерн Підопічний',
            'category_id': self.category_intern.id,
            'mentor_id': specialist.id,
        })
        self.assertEqual(intern.mentor_id, specialist)
