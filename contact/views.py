from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm
from products.models import Product


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_success')
    else:
        initial = {}
        product_id = request.GET.get('product')
        if product_id:
            try:
                product = get_object_or_404(Product, id=product_id, active=True)
            except ValueError:
                raise Http404
            initial = {'product': product}
        form = ContactForm(initial=initial)

    return render(request, 'contact/contact_form.html', {'form': form})


def contact_success(request):
    return render(request, 'contact/contact_success.html')