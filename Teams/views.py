from django.http import Http404
from django.shortcuts import render

from Teams.models import Team


def team_page(request, team_name):
    # TODO Polskie znaki

    team_name = team_name.replace("_", " ")

    try:
        team = Team.objects.get(name=team_name)
    except Team.DoesNotExist:
        raise Http404

    return render(request, 'Teams/team_page.html', {'team': team})
