from django.shortcuts import render
from .models import Organization
from projects.models import Project
from services.models import Service


def home(request):
    context = {
        'organizations': Organization.objects.filter(active=True),
        'featured_projects': Project.objects.filter(published=True)[:3],
        'services': Service.objects.filter(active=True)[:6],
    }
    return render(request, 'core/home.html', context)


def organization_list(request):
    organizations = Organization.objects.filter(active=True)
    return render(request, 'core/organization_list.html', {'organizations': organizations})