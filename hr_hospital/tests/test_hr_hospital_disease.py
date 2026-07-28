from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestHrHospitalDisease(TransactionCase):

    def test_parent_recursion_is_blocked(self):
        """A disease cannot become an ancestor of itself.

        The ORM's own parent_path guard and our _check_parent_recursion
        constraint both reject this; either raises a UserError subclass.
        """
        parent = self.env['hr.hospital.disease'].create({'name': 'ГРВІ'})
        child = self.env['hr.hospital.disease'].create({
            'name': 'Грип',
            'parent_id': parent.id,
        })
        with self.assertRaises(UserError):
            parent.parent_id = child.id

    def test_valid_hierarchy_is_allowed(self):
        parent = self.env['hr.hospital.disease'].create({'name': 'Інфекційні хвороби'})
        child = self.env['hr.hospital.disease'].create({
            'name': 'ГРВІ',
            'parent_id': parent.id,
        })
        self.assertEqual(child.parent_id, parent)
        self.assertIn(child, parent.child_ids)

    def test_display_name_reflects_hierarchy(self):
        parent = self.env['hr.hospital.disease'].create({'name': 'Інфекційні хвороби'})
        child = self.env['hr.hospital.disease'].create({
            'name': 'ГРВІ',
            'parent_id': parent.id,
        })
        self.assertEqual(child.display_name, 'Інфекційні хвороби / ГРВІ')
