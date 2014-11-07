from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from Teams.models import Team


def team_index(request):
    # TODO /team/

    return render(request, 'Teams/team_index.html')


def team_page(request, team_name):
    try:
        team = Team.objects.get(full_name=team_name.replace("_", " ").title)
    except Team.DoesNotExist:
        raise Http404

    team_players = []

    for player in Player.objects.filter(team=team).order_by('last_name', 'first_name'):
        team_players.append(
            {'number': player.number, 'name': player.first_name + ' ' + player.last_name, 'age': player.age(),
             'position': player.position, 'height': player.height, 'weight': player.weight,
             'link': player.first_name + '_' + player.last_name})

    return render(request, 'Teams/team_page.html', {'team': team, 'team_players': team_players})