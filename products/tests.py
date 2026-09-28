from django.test import TestCase
from django.urls import reverse
from .models import ProductCategory, Product


class ProductViewTest(TestCase):
    def setUp(self):
        self.category_a = ProductCategory.objects.create(
            name='PPE',
            slug='ppe',
        )
        self.category_b = ProductCategory.objects.create(
            name='Sterilization Monitoring',
            slug='sterilization-monitoring',
        )
        self.product_a = Product.objects.create(
            name='Nitrile Gloves',
            slug='nitrile-gloves',
            product_code='PPE-001',
            description='Disposable gloves.',
            category=self.category_a,
            active=True,
        )
        self.product_b = Product.objects.create(
            name='Sterilization Indicator Strips',
            slug='sterilization-indicator-strips',
            product_code='STM-001',
            description='Indicator strips.',
            category=self.category_b,
            active=True,
        )
        self.inactive_product = Product.objects.create(
            name='Discontinued Item',
            slug='discontinued-item',
            product_code='OLD-001',
            description='No longer sold.',
            category=self.category_a,
            active=False,
        )

    def test_list_view_status_code(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)

    def test_list_view_excludes_inactive(self):
        response = self.client.get(reverse('product_list'))
        self.assertContains(response, 'Nitrile Gloves')
        self.assertNotContains(response, 'Discontinued Item')

    def test_category_filter(self):
        url = reverse('product_list') + '?category=' + self.category_a.slug
        response = self.client.get(url)
        self.assertContains(response, 'Nitrile Gloves')
        self.assertNotContains(response, 'Sterilization Indicator Strips')

    def test_detail_view_active_returns_200(self):
        response = self.client.get(reverse('product_detail', args=['nitrile-gloves']))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_inactive_returns_404(self):
        response = self.client.get(reverse('product_detail', args=['discontinued-item']))
        self.assertEqual(response.status_code, 404)