from django.http import Http404
from django.shortcuts import render
from Games import models

def game_index(request):
    # TODO /game/

    return render(request, 'Games/game_index.html', {'games': models.Game.objects.all()})


def game_on_date(request, game_date):
    # TODO /game/date/

    return render(request, 'Games/game_on_date.html')


def game_page(request, game_date, away_team, home_team):
    # TODO /game/date/away-team_@_home-team

    return render(request, 'Games/game_page.html')