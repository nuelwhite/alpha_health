from django.test import TestCase
from .models import Organization


class OrganizationModelTest(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(
            name='The Alpha Health Group',
            slug='the-alpha-health-group',
            country='US',
        )

    def test_str_representation(self):
        self.assertEqual(str(self.org), 'The Alpha Health Group')

    def test_default_active_is_true(self):
        self.assertTrue(self.org.active)
        
    def test_filter_excludes_inactive(self):
        Organization.objects.create(
            name='Inactive Org',
            slug='inactive-org',
            active=False,
        )
        active_orgs = Organization.objects.filter(active=True)
        self.assertEqual(active_orgs.count(), 1)
        self.assertIn(self.org, active_orgs)