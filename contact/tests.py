from django.test import TestCase
from django.urls import reverse
from .models import ContactInquiry
from products.models import Product, ProductCategory


class ContactViewTest(TestCase):
    def setUp(self):
        self.category = ProductCategory.objects.create(name='PPE', slug='ppe')
        self.product = Product.objects.create(
            name='Nitrile Gloves',
            slug='nitrile-gloves',
            product_code='PPE-001',
            description='Disposable gloves.',
            category=self.category,
            active=True,
        )

    def test_get_form_prefills_product(self):
        response = self.client.get(reverse('contact_view') + f'?product={self.product.id}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nitrile Gloves')

    def test_get_form_invalid_product_returns_404(self):
        response = self.client.get(reverse('contact_view') + '?product=999999')
        self.assertEqual(response.status_code, 404)

    def test_post_valid_form_creates_inquiry(self):
        response = self.client.post(reverse('contact_view'), {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'phone': '',
            'subject': 'Question',
            'message': 'Do you ship internationally?',
            'product': self.product.id,
        })
        self.assertRedirects(response, reverse('contact_success'))
        self.assertEqual(ContactInquiry.objects.count(), 1)
        inquiry = ContactInquiry.objects.first()
        self.assertEqual(inquiry.email, 'jane@example.com')
        self.assertEqual(inquiry.product, self.product)

    def test_post_missing_message_shows_error(self):
        response = self.client.post(reverse('contact_view'), {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'phone': '',
            'subject': 'Question',
            'message': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactInquiry.objects.count(), 0)
        
    def test_get_form_non_numeric_product_returns_404(self):
        response = self.client.get(reverse('contact_view') + '?product=abc')
        self.assertEqual(response.status_code, 404)