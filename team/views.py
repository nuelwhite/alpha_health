from django.shortcuts import render
from .models import TeamMember


def team_list(request):
    members = TeamMember.objects.filter(active=True)
    founder = members.first()
    rest = members[1:] if founder else members
    return render(request, 'team/team_list.html', {'founder': founder, 'members': rest})