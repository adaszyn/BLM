from django.http import Http404
from django.shortcuts import render
from django.db.models import Q

from Players.models import Player


def player_page(request, player_fullname):
    # TODO Polskie znaki

    first, last = player_fullname.split("_")

    try:
        player = Player.objects.get(Q(first_name=first), Q(last_name=last))
    except Player.DoesNotExist:
        raise Http404

    return render(request, 'Players/player_page.html', {'player': player})
