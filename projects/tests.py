from django.test import TestCase
from django.urls import reverse
from .models import Project
from core.models import Organization


class ProjectViewTest(TestCase):
    def setUp(self):
        self.published_project = Project.objects.create(
            title='Published Project',
            slug='published-project',
            published=True,
        )
        self.draft_project = Project.objects.create(
            title='Draft Project',
            slug='draft-project',
            published=False,
        )

    def test_list_view_status_code(self):
        response = self.client.get(reverse('project_list'))
        self.assertEqual(response.status_code, 200)

    def test_list_view_shows_only_published(self):
        response = self.client.get(reverse('project_list'))
        self.assertContains(response, 'Published Project')
        self.assertNotContains(response, 'Draft Project')

    def test_detail_view_published_returns_200(self):
        response = self.client.get(reverse('project_detail', args=['published-project']))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_draft_returns_404(self):
        response = self.client.get(reverse('project_detail', args=['draft-project']))
        self.assertEqual(response.status_code, 404)
        
    def test_detail_view_shows_organization_name(self):
        org = Organization.objects.create(name='Test Org', slug='test-org')
        self.published_project.organization = org
        self.published_project.save()

        response = self.client.get(reverse('project_detail', args=['published-project']))
        self.assertContains(response, 'Test Org')