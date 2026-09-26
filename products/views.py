from django.shortcuts import render, get_object_or_404
from .models import Product, ProductCategory


def product_list(request):
    products = Product.objects.filter(active=True)
    category_slug = request.GET.get('category')

    if category_slug:
        products = products.filter(category__slug=category_slug)

    categories = ProductCategory.objects.filter(active=True)

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_slug,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, active=True)
    return render(request, 'products/product_detail.html', {'product': product})