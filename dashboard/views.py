from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.models import Organization, Redirect
from projects.models import Project
from services.models import Service
from team.models import TeamMember
from products.models import Product, ProductCategory
from contact.models import ContactInquiry


@login_required
def dashboard_home(request):
    context = {
        'counts': {
            'Organizations': Organization.objects.count(),
            'Projects': Project.objects.count(),
            'Services': Service.objects.count(),
            'Team Members': TeamMember.objects.count(),
            'Products': Product.objects.count(),
            'Inquiries': ContactInquiry.objects.count(),
        },
        'recent_inquiries': ContactInquiry.objects.all()[:5],
    }
    return render(request, 'dashboard/home.html', context)