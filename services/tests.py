from django.test import TestCase
from django.urls import reverse
from .models import Service
from core.models import Organization


class ServiceViewTest(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='Test Org', slug='test-org')
        self.active_service = Service.objects.create(
            name='Sterilization',
            slug='sterilization',
            short_description='SPD training and consultancy.',
            organization=self.org,
            active=True,
        )
        self.inactive_service = Service.objects.create(
            name='Retired Service',
            slug='retired-service',
            active=False,
        )

    def test_list_view_status_code(self):
        response = self.client.get(reverse('service_list'))
        self.assertEqual(response.status_code, 200)

    def test_list_view_shows_only_active(self):
        response = self.client.get(reverse('service_list'))
        self.assertContains(response, 'Sterilization')
        self.assertNotContains(response, 'Retired Service')

    def test_detail_view_active_returns_200(self):
        response = self.client.get(reverse('service_detail', args=['sterilization']))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_inactive_returns_404(self):
        response = self.client.get(reverse('service_detail', args=['retired-service']))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_shows_organization_name(self):
        response = self.client.get(reverse('service_detail', args=['sterilization']))
        self.assertContains(response, 'Test Org')