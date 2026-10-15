import base64
import shutil
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
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

class MobileNavTest(TestCase):
    def test_nav_toggle_hooks_present(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'id="nav-toggle"')
        self.assertContains(response, 'aria-controls="site-nav"')
        self.assertContains(response, 'id="site-nav"')


class AboutPageTest(TestCase):
    def test_value_cards_have_icons_and_centered_grid(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'values--three')
        self.assertContains(response, 'class="value-card__icon"', count=3)


PNG_1X1 = base64.b64decode(
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=='
)


class AboutImageTest(TestCase):
    def test_image_appears_before_story_when_set(self):
        tmp = tempfile.mkdtemp()
        try:
            with override_settings(MEDIA_ROOT=tmp):
                org = Organization.objects.create(name='Alpha', slug='alpha', country='USA')
                org.about_image.save(
                    'team.png',
                    SimpleUploadedFile('team.png', PNG_1X1, content_type='image/png'),
                )
                body = self.client.get(reverse('about')).content.decode()
                self.assertIn('about-image__img', body)
                self.assertLess(body.index('about-image__img'), body.index('Our Story'))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_no_image_markup_when_unset(self):
        Organization.objects.create(name='Alpha', slug='alpha', country='USA')
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'about-image__img')
