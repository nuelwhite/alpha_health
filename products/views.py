from django.shortcuts import render, get_object_or_404
from .models import Product, ProductCategory
from core.models import Organization


def product_list(request):
    products = Product.objects.filter(active=True)
    category_slug = request.GET.get('category')

    if category_slug:
        products = products.filter(category__slug=category_slug)

    categories = ProductCategory.objects.filter(active=True)
    ao = Organization.objects.filter(country='GH').first()

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_slug,
        'ao': ao,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, active=True)
    ao = Organization.objects.filter(country='GH').first()
    return render(request, 'products/product_detail.html', {'product': product, 'ao': ao})