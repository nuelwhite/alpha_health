from django.test import TestCase
from django.urls import reverse
from .models import TeamMember


class TeamViewTest(TestCase):
    def setUp(self):
        self.active_member = TeamMember.objects.create(
            name='Jane Smith',
            position='Project Director',
            active=True,
        )
        self.inactive_member = TeamMember.objects.create(
            name='Former Staff',
            position='Consultant',
            active=False,
        )

    def test_list_view_status_code(self):
        response = self.client.get(reverse('team_list'))
        self.assertEqual(response.status_code, 200)

    def test_list_view_shows_only_active(self):
        response = self.client.get(reverse('team_list'))
        self.assertContains(response, 'Jane Smith')
        self.assertNotContains(response, 'Former Staff')

    def test_list_view_shows_position(self):
        response = self.client.get(reverse('team_list'))
        self.assertContains(response, 'Project Director')