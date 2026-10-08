from django.urls import reverse
from django.test import TestCase
from .models import Organization, Redirect
from django.contrib.auth.models import Group, User
from django.core.management import call_command


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
        
        

class RolePermissionsTest(TestCase):
    def setUp(self):
        call_command('setup_roles')

    def make_user(self, username, group_name):
        user = User.objects.create_user(username, password='x', is_staff=True)
        user.groups.add(Group.objects.get(name=group_name))
        return user

    def test_product_manager_scope(self):
        user = self.make_user('pm', 'Product Manager')
        self.assertTrue(user.has_perm('products.change_product'))
        self.assertFalse(user.has_perm('projects.change_project'))

    def test_read_only_cannot_change(self):
        user = self.make_user('ro', 'Read Only')
        self.assertTrue(user.has_perm('projects.view_project'))
        self.assertFalse(user.has_perm('projects.change_project'))

    def test_inquiry_handler_cannot_delete(self):
        user = self.make_user('ih', 'Inquiry Handler')
        self.assertTrue(user.has_perm('contact.change_contactinquiry'))
        self.assertFalse(user.has_perm('contact.delete_contactinquiry'))

    def test_admin_blocks_out_of_scope_models(self):
        user = self.make_user('pm2', 'Product Manager')
        self.client.force_login(user)
        self.assertEqual(self.client.get('/admin/projects/project/').status_code, 403)
        self.assertEqual(self.client.get('/admin/products/product/').status_code, 200)
        
class OutputEscapingTest(TestCase):
    def test_home_escapes_short_description(self):
        Organization.objects.create(
            name='Org', slug='org', country='USA',
            short_description='<script>alert(1)</script>',
        )
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, '<script>alert(1)</script>')

    def test_ao_landing_escapes_short_description(self):
        Organization.objects.create(
            name='AO', slug='ao', country='GH',
            short_description='<script>alert(2)</script>',
        )
        response = self.client.get(reverse('ao_landing'))
        self.assertNotContains(response, '<script>alert(2)</script>')