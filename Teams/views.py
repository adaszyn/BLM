from django.http import Http404
from django.shortcuts import render

from Teams.models import Team
from Players.models import Player


def team_page(request, team_name):
    try:
        team = Team.objects.get(full_name=team_name.replace("_", " ").title)
    except Team.DoesNotExist:
        raise Http404

    team_players = list()

    for player in Player.objects.filter(team=team).order_by('last_name', 'first_name'):
        team_players.append(player)

    return render(request, 'Teams/team_page.html', {'team': team, 'team_players': team_players})