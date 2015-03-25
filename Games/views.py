from django.http import Http404
from django.shortcuts import HttpResponse
from django.shortcuts import render
import json

from Games.models import *
from Teams.models import *


def game_index(request):
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


def game_page(request, game_date, away_team_short, home_team_short):
    try:
        home_team = Team.objects.get(short_name=home_team_short)
        away_team = Team.objects.get(short_name=away_team_short)
        game = Game.objects.get(Q(home_team=home_team), Q(away_team=away_team), Q(date=game_date))
    except (Team.DoesNotExist, Game.DoesNotExist):
        raise Http404

    if game.happened:
        period_score = list()
        for item in PeriodScore.objects.filter(game=game):
            period_score.append({'quarter': item.quarter,
                                 'home_team': item.home_team,
                                 'away_team': item.away_team})

        final_score = game.final_score

        boxscore_fields = [
            ['MIN', 'PTS', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%',
             'ORB', 'DRG', 'TRB', 'AST', 'STL', 'BLK', 'BA', 'TO', 'PF'],
            ['min', 'pts', 'fgm', 'fga', 'fg_perc', 'three_pm', 'three_pa', 'three_perc', 'ftm', 'fta', 'ft_perc',
             'reb_off', 'reb_def', 'reb_all', 'ast', 'stl', 'blk', 'ba', 'to', 'pf']
        ]
        total_leader_fields = [
            ['PTS', 'REB', 'AST', 'STL', 'BLK'],
            ['pts', 'reb_all', 'ast', 'stl', 'blk']
        ]

        home_team_box = TeamBoxscore.objects.get(Q(game=game), Q(team=home_team))
        away_team_box = TeamBoxscore.objects.get(Q(game=game), Q(team=away_team))

        home_game_leaders = list()
        for stat, item in zip(total_leader_fields[0], total_leader_fields[1]):
            player, value = home_team_box.team_game_leader(item)
            if isinstance(player, Player):
                home_game_leaders.append({'stat': stat, 'string': player.full_name, 'link': player.get_absolute_url(),
                                          'value': value})
            else:
                home_game_leaders.append({'stat': stat, 'string': player, 'link': '#', 'value': value})

        away_game_leaders = list()
        for stat, item in zip(total_leader_fields[0], total_leader_fields[1]):
            player, value = away_team_box.team_game_leader(item)
            if isinstance(player, Player):
                away_game_leaders.append({'stat': stat, 'string': player.full_name, 'link': player.get_absolute_url(),
                                          'value': value})
            else:
                away_game_leaders.append({'stat': stat, 'string': player, 'link': '#', 'value': value})

        home_players_boxscores = home_team_box.team_players_boxscores(boxscore_fields[1])
        away_players_boxscores = away_team_box.team_players_boxscores(boxscore_fields[1])

        home_team_boxscore = home_team_box.team_boxscore(boxscore_fields[1])
        away_team_boxscore = away_team_box.team_boxscore(boxscore_fields[1])

        return render(request, 'Games/game_page.html',
                      {'home_team': home_team, 'away_team': away_team, 'game_date': game_date,
                       'period_score': period_score, 'final_score': final_score, 'boxscore_fields': boxscore_fields[0],
                       'home_game_leaders': home_game_leaders, 'away_game_leaders': away_game_leaders,
                       'home_players_boxscores': home_players_boxscores, 'home_team_boxscore': home_team_boxscore,
                       'away_players_boxscores': away_players_boxscores, 'away_team_boxscore': away_team_boxscore})

    else:
        avg_leader_fields = [
            ['PPG', 'RPG', 'APG', 'SPG', 'BPG'],
            ['pts', 'reb_all', 'ast', 'stl', 'blk']
        ]

        home_team_leaders = list()
        for stat, item in zip(avg_leader_fields[0], avg_leader_fields[1]):
            player, value = home_team.team_average_leader(item)
            home_team_leaders.append({'stat': stat, 'player': player, 'value': value})

        away_team_leaders = list()
        for stat, item in zip(avg_leader_fields[0], avg_leader_fields[1]):
            player, value = away_team.team_average_leader(item)
            away_team_leaders.append({'stat': stat, 'player': player, 'value': value})

        return render(request, 'Games/game_page_future.html',
                      {'home_team': home_team, 'away_team': away_team, 'game_date': game_date,
                       'home_team_leaders': home_team_leaders, 'away_team_leaders': away_team_leaders})


def get_games_by_date(request, game_date):
    jsonObj = []
    try:
        games = Game.objects.filter(date=game_date)
        for game in list(games):
            jsonObj.append({
                "date": str(game.date),
                'away_team': game.away_team.full_name,
                'home_team': game.home_team.full_name,
                'home_score': TeamBoxscore.objects.filter(game=game, team=game.home_team).get().pts,
                'away_score': TeamBoxscore.objects.filter(game=game, team=game.away_team).get().pts,
                'url': game.get_absolute_url(),
            })
    except(Game.DoesNotExist):
        raise Http404
    return HttpResponse(json.dumps(jsonObj))


def get_gamesdates(request, game_date, quantity, direction):
    if int(direction) == 1:
        games = Game.objects.filter(date__gt=game_date).order_by('date')
    else:
        games = Game.objects.filter(date__lt=game_date).order_by('-date')
        print(games)
    games_in_days = {}
    jsonObj = {}
    for game in list(games):
        date_string = str(game.date)
        if date_string not in games_in_days:
            if len(games_in_days.keys()) == int(quantity):
                break
            else:
                games_in_days[date_string] = [game]
        else:
            games_in_days[date_string].append(game)
    for key, val in games_in_days.items():
        jsonObj[key] = []
        for game in val:
            jsonObj[key].append({
                'home_team': game.home_team.full_name,
                'away_team': game.away_team.full_name,
                'home_score': TeamBoxscore.objects.filter(game=game, team=game.home_team).get().pts,
                'away_score': TeamBoxscore.objects.filter(game=game, team=game.away_team).get().pts
            })
    return HttpResponse(json.dumps(jsonObj))