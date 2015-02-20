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


def game_page(request, game_date, away_team_short, home_team_short):
    try:
        home_team = Team.objects.get(short_name=home_team_short)
        away_team = Team.objects.get(short_name=away_team_short)
        game_date = datetime.strptime(game_date, '%Y-%m-%d').date()
        game = Game.objects.get(Q(home_team=home_team), Q(away_team=away_team), Q(date=game_date))
    except (Team.DoesNotExist, Game.DoesNotExist):
        raise Http404

    period_score = list()
    for item in PeriodScore.objects.filter(game=game).order_by('quarter'):
        period_score.append(item)

    final_score = {'home_team': TeamBoxscore.objects.get(Q(game=game), Q(team=home_team)).pts,
                   'away_team': TeamBoxscore.objects.get(Q(game=game), Q(team=away_team)).pts}

    home_team_leaders = TeamBoxscore.objects.get(Q(game=game), Q(team=home_team)).team_game_leaders
    away_team_leaders = TeamBoxscore.objects.get(Q(game=game), Q(team=away_team)).team_game_leaders

    boxscore_fields = ['#', 'Name', 'MIN', 'PTS', 'FGM-A', 'FG%', '3PM-A', '3P%', 'FTM-A', 'FT%', 'ORB', 'DRG', 'TRB',
                       'AST', 'STL', 'BLK', 'BA', 'TO', 'PF']

    home_players_boxscores = TeamBoxscore.objects.get(Q(game=game), Q(team=home_team)).team_players_boxscores
    away_players_boxscores = TeamBoxscore.objects.get(Q(game=game), Q(team=away_team)).team_players_boxscores

    home_team_boxscore = TeamBoxscore.objects.get(Q(game=game), Q(team=home_team)).team_boxscore
    away_team_boxscore = TeamBoxscore.objects.get(Q(game=game), Q(team=away_team)).team_boxscore

    return render(request, 'Games/game_page.html',
                  {'home_team': home_team, 'away_team': away_team, 'game_date': game_date,
                   'period_score': period_score, 'final_score': final_score, 'boxscore_fields': boxscore_fields,
                   'home_team_leaders': home_team_leaders, 'away_team_leaders': away_team_leaders,
                   'home_players_boxscores': home_players_boxscores, 'home_team_boxscore': home_team_boxscore,
                   'away_players_boxscores': away_players_boxscores, 'away_team_boxscore': away_team_boxscore})