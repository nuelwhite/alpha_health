from django.shortcuts import render
from .models import TeamMember


def team_list(request):
    members = TeamMember.objects.filter(active=True)
    return render(request, 'team/team_list.html', {'members': members})