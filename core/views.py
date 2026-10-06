from django.shortcuts import render
from .models import Organization
from projects.models import Project
from services.models import Service


def home(request):
    context = {
        'organization': Organization.objects.filter(active=True).exclude(country='GH').first(),
        'featured_projects': Project.objects.filter(published=True)[:6],
        'featured_services': Service.objects.filter(slug__in=['sterilization', 'public-health'], active=True),
    }
    return render(request, 'core/home.html', context)



def organization_list(request):
    organizations = Organization.objects.filter(active=True)
    return render(request, 'core/organization_list.html', {'organizations': organizations})

def about(request):
    organization = Organization.objects.filter(active=True).first()
    return render(request, 'core/about.html', {'organization': organization})

def ao_landing(request):
    ao = Organization.objects.filter(active=True, country='GH').first()
    return render(request, 'core/ao_landing.html', {'ao': ao})