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


def game_page(request, game_date, away_team_short, home_team_short):
    game_date = datetime.strptime(game_date, '%Y-%m-%d').date()

    try:
        home_team = Team.objects.get(short_name=home_team_short)
        away_team = Team.objects.get(short_name=away_team_short)
        game = Game.objects.get(Q(home_team=home_team), Q(away_team=away_team), Q(date=game_date))
    except (Team.DoesNotExist, Game.DoesNotExist):
        raise Http404

    if game.happened:
        period_score = list()
        for item in PeriodScore.objects.filter(game=game).order_by('quarter'):
            period_score.append(item)

        final_score = game.final_score

        boxscore_fields = [
            ['#', 'Name', 'MIN', 'PTS', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%',
             'ORB', 'DRG', 'TRB', 'AST', 'STL', 'BLK', 'BA', 'TO', 'PF'],
            ['min', 'pts', 'fgm', 'fga', 'fg_perc', 'three_pm', 'three_pa', 'three_perc', 'ftm', 'fta', 'ft_perc',
             'reb_off', 'reb_def', 'reb_all', 'ast', 'stl', 'blk', 'ba', 'to', 'pf']
        ]
        leaders_fields = [
            ['PTS', 'REB', 'AST', 'STL', 'BLK'],
            ['pts', 'reb_all', 'ast', 'stl', 'blk']
        ]

        home_team_box = TeamBoxscore.objects.get(Q(game=game), Q(team=home_team))
        away_team_box = TeamBoxscore.objects.get(Q(game=game), Q(team=away_team))

        home_game_leaders = list()
        away_game_leaders = list()
        for team in [[home_team_box, home_game_leaders], [away_team_box, away_game_leaders]]:
            for stat, item in zip(leaders_fields[0], leaders_fields[1]):
                player, value = team[0].team_game_leader(item)
                if isinstance(player, Player):
                    # Example: ['PTS', 'Michael Jordan', '/player/Michael_Jordan/', 55]
                    team[1].append([stat, player.full_name, player.get_absolute_url(), value])
                else:
                    # Example: ['PTS', '2 players', '#', 55]
                    team[1].append([stat, player, '#', value])

        home_players_boxscores = home_team_box.team_players_boxscores(boxscore_fields[1])
        away_players_boxscores = away_team_box.team_players_boxscores(boxscore_fields[1])

        home_team_boxscore = home_team_box.team_boxscore(boxscore_fields[1])
        away_team_boxscore = away_team_box.team_boxscore(boxscore_fields[1])

        return render(request, 'Games/game_page.html',
                      {'home_team': home_team, 'away_team': away_team, 'game_date': game_date,
                       'period_score': period_score, 'final_score': final_score,
                       'boxscore_fields': boxscore_fields[0], 'leaders_fields': leaders_fields[0],
                       'home_game_leaders': home_game_leaders, 'away_game_leaders': away_game_leaders,
                       'home_players_boxscores': home_players_boxscores, 'home_team_boxscore': home_team_boxscore,
                       'away_players_boxscores': away_players_boxscores, 'away_team_boxscore': away_team_boxscore})

    else:
        leaders_fields = [
            ['PPG', 'RPG', 'APG', 'SPG', 'BPG'],
            ['pts', 'reb_all', 'ast', 'stl', 'blk']
        ]

        home_team_leaders = list()
        away_team_leaders = list()
        for team in [[home_team, home_team_leaders], [away_team, away_team_leaders]]:
            for stat, item in zip(leaders_fields[0], leaders_fields[1]):
                player, value = team[0].team_average_leader(item)
                # Example: ['PPG', 'Michael Jordan', '/player/Michael_Jordan/', 55]
                team[1].append([stat, player.full_name, player.get_absolute_url(), value])

        return render(request, 'Games/game_page_future.html',
                      {'home_team': home_team, 'away_team': away_team, 'game_date': game_date,
                       'home_team_leaders': home_team_leaders, 'away_team_leaders': away_team_leaders})