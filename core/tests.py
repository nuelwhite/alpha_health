from django.test import TestCase
from .models import Organization, Redirect


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


class RedirectMiddlewareTest(TestCase):
    def test_matching_redirect_returns_301(self):
        Redirect.objects.create(
            old_path='/projects/old-slug/',
            new_path='/projects/new-slug/',
        )
        response = self.client.get('/projects/old-slug/')
        self.assertRedirects(
            response,
            '/projects/new-slug/',
            status_code=301,
            fetch_redirect_response=False,
        )

    def test_no_matching_redirect_returns_404(self):
        response = self.client.get('/projects/genuinely-nonexistent/')
        self.assertEqual(response.status_code, 404)