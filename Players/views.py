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

    boxscore_fields = [
        ['Date', 'Opp', 'Score', 'MIN', 'PTS', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%',
         'ORB', 'DRG', 'TRB', 'AST', 'STL', 'BLK', 'BA', 'TO', 'PF'],
        ['min', 'pts', 'fgm', 'fga', 'fg_perc', 'three_pm', 'three_pa', 'three_perc', 'ftm', 'fta', 'ft_perc',
         'reb_off', 'reb_def', 'reb_all', 'ast', 'stl', 'blk', 'ba', 'to', 'pf']
    ]

    season_stats = player.season_stats(boxscore_fields[1])

    number_of_games = player.number_of_games()

    average = list()
    for item in boxscore_fields[1]:
        average.append(player.cat_average(item))

    total = list()
    for item in boxscore_fields[1]:
        total.append(player.cat_total(item))

    return render(request, 'Players/player_page.html',
                  {'player': player, 'boxscore_fields': boxscore_fields[0], 'season_stats': season_stats,
                   'number_of_games': number_of_games, 'average': average, 'total': total})