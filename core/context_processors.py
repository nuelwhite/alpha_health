from .models import Organization


def site_organization(request):
    org = Organization.objects.filter(active=True).exclude(country='GH').first()
    return {'site_organization': org}