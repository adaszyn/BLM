from django.http import Http404
from django.shortcuts import render
from django.db.models import Q
from django.utils.datetime_safe import date
from Teams import models as teamModels
from Players.models import Player

def player_index(request):
    # TODO /player/
    teams_dict = {}
    all_teams = teamModels.Team.objects.all()
    for team in all_teams:
        teams_dict[team.full_name] = []    #list for each entry in dictionary

    all_players = Player.objects.all()
    for player in all_players:
        teams_dict[player.team.full_name].append(player)   #append player to ones appropriate list
    for team in teams_dict:
        teams_dict[team].sort(key=lambda player: player.last_name)
        print (teams_dict[team])

    return render(request, 'Players/player_index.html', {'teams_dict' : teams_dict, "players" : all_players})


def player_page(request, player_fullname):
    first, last = player_fullname.split("_")
    first = first.title()
    last = last.title()

    try:
        player = Player.objects.get(Q(first_name=first), Q(last_name=last))
    except Player.DoesNotExist:
        raise Http404

    # For team page link
    team_name = str(player.team).replace(" ", "_")

    def calculate_age(born):
        today = date.today()
        try:
            birthday = born.replace(year=today.year)
        except ValueError:  # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year, month=born.month+1, day=1)
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

    age = calculate_age(player.birth_date)
    birth_date = player.birth_date.strftime("%d.%m.%Y")

    return render(request, 'Players/player_page.html', {'player': player, 'team_name': team_name, 'birth_date': birth_date, 'age': age})
