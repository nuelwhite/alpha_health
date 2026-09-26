from django.shortcuts import render
from .models import Organization

# Create your views here.
def organization_list(request):
    organizations = Organization.objects.filter(active=True)
    return render(request, 'core/organization_list.html', {'organizations': organizations})