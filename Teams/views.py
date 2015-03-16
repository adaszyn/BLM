from django.http import Http404
from django.shortcuts import render
from collections import OrderedDict

from Teams.models import Team


def team_page(request, team_name):
    try:
        team = Team.objects.get(full_name=team_name.replace("_", " ").title)
    except Team.DoesNotExist:
        raise Http404

    team_players = team.team_players()

    avg_leaders_fields = [
        ['PPG', 'RPG', 'APG', 'SPG', 'BPG'],
        ['pts', 'reb_all', 'ast', 'stl', 'blk']
    ]

    team_leaders = list()
    for stat, item in zip(avg_leaders_fields[0], avg_leaders_fields[1]):
        player, value = team.team_average_leader(item)
        team_leaders.append({'stat': stat, 'player': player, 'value': value})

    previous_games = team.next_games(-5)
    next_games = team.next_games(5)

    stat_fields = [
        ['MIN', 'PTS', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%',
         'ORB', 'DRG', 'TRB', 'AST', 'STL', 'BLK', 'BA', 'TO', 'PF'],
        ['min', 'pts', 'fgm', 'fga', 'fg_perc', 'three_pm', 'three_pa', 'three_perc', 'ftm', 'fta', 'ft_perc',
         'reb_off', 'reb_def', 'reb_all', 'ast', 'stl', 'blk', 'ba', 'to', 'pf']
    ]

    players_stats = OrderedDict()
    for player in team_players:
        players_stats[player] = list()

        for item in stat_fields[1]:
            players_stats[player].append(player.cat_average(item))

    return render(request, 'Teams/team_page.html',
                  {'team': team, 'team_players': team_players, 'team_leaders': team_leaders,
                   'previous_games': previous_games, 'next_games': next_games,
                   'stat_fields': stat_fields[0], 'players_stats': players_stats})