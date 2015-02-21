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

    leaders_fields = [
        ['PPG', 'RPG', 'APG', 'SPG', 'BPG'],
        ['pts', 'reb_all', 'ast', 'stl', 'blk']
    ]

    team_leaders = list()
    for stat, item in zip(leaders_fields[0], leaders_fields[1]):
        player, value = team.team_average_leader(item)
        # Example: ['PPG', 'Michael Jordan', '/player/Michael_Jordan/', 55]
        team_leaders.append([stat, player.full_name, player.get_absolute_url(), value])

    previous_games = team.next_games(-5, converted=True)
    next_games = team.next_games(5, converted=True)

    return render(request, 'Teams/team_page.html',
                  {'team': team, 'team_players': team_players, 'team_leaders': team_leaders,
                   'previous_games': previous_games, 'next_games': next_games})