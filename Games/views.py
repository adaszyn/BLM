from django.http import Http404
from django.shortcuts import render


def game_index(request):
    # TODO /game/

    return render(request, 'Games/game_index.html')


def game_page(request, game_date, away_team, home_team):
    # TODO /game/date/away-team_@_home-team

    return render(request, 'Games/game_page.html')