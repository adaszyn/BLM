from django.http import Http404
from django.shortcuts import render
from django.db.models import Q

from Teams import models as teamModels
from Players.models import Player


def player_index(request):
    teams_dict = {}
    all_teams = teamModels.Team.objects.all()
    for team in all_teams:
        teams_dict[team] = []    #list for each entry in dictionary

    all_players = Player.objects.all()
    for player in all_players:
        teams_dict[player.team].append(player)   #append player to ones appropriate list
    for team in teams_dict:
        teams_dict[team].sort(key=lambda player: player.last_name)
        # print(teams_dict[team])

    return render(request, 'Players/player_index.html', {'teams_dict': teams_dict, "players": all_players})


def player_page(request, player_fullname):
    first, last = player_fullname.split("_")

    try:
        player = Player.objects.get(Q(first_name=first.title()), Q(last_name=last.title()))
    except Player.DoesNotExist:
        raise Http404

    birth_date = player.birth_date.strftime("%d.%m.%Y")

    return render(request, 'Players/player_page.html',
                  {'player': player, 'birth_date': birth_date})