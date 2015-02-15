from django.http import Http404
from django.shortcuts import render
from Games.models import *
from Teams.models import *
from datetime import datetime, timedelta


def game_index(request):
    # TODO: Do przepisania
    '''
    context_dict = []
    home_points = []
    away_points = []
    #filter games from this week
    for game in Game.objects.filter(date__range = [datetime.now()-timedelta(days=600), datetime.now()]):
        for tbs in TeamBoxscore.objects.filter(game = game):
            for ps in PeriodScore.objects.filter(team_boxscore = tbs):
                #zajebista zlozonosc kurwo
                if (ps.team_boxscore.team == game.away_team):
                    away_points.append(ps.points)
                else:
                    home_points.append(ps.points)
        home_points = [sum(home_points)] + home_points  #temporary solution - teamboxscore.points bug
        away_points = [sum(away_points)] + away_points
        # home_points = TeamBoxscore.objects.get(game=game, is_home=True).points
        # away_points = TeamBoxscore.objects.get(game=game, is_home = False).points
        # print(away_points)
        context_dict.append(
            {'home':game.home_team,
             'away': game.away_team,
             'home_points':home_points,
             'away_points': away_points,
             'ratio' : 20,
             'id' : game.pk
            }
        )

    return render(request, 'Games/game_index.html', {'context': context_dict})
    '''
    return render(request, 'Games/game_index.html')


def game_on_date(request, game_date):
    # TODO /game/date/

    return render(request, 'Games/game_on_date.html')


def game_page(request, game_date, away_team, home_team):
    # TODO /game/date/away-team_@_home-team

    return render(request, 'Games/game_page.html')