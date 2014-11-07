from django.http import Http404
from django.shortcuts import render


def game_index(request):
    # TODO /game/

    return render(request, 'Games/game_index.html')