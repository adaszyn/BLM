from django.http import Http404
from django.shortcuts import render
from django.db.models import Q

from Players.models import Player


def player_page(request, player_fullname):
    # TODO Zawodnicy z polskimi znakami
    # @wojtek zastanów się jak to zrobić
    # Ja póki co widzę tylko dodanie do modelu pola '*_name_en' które zawiera to samo co '*_name' ale przesiane przez:
    # abc.translate(str.maketrans("ąćęłńóśżźĄĆĘŁŃÓŚŻŹ", "acelnoszzACELNOSZZ"))
    # ^ zamienia w abc polskie znaki an angielskie odpowiedniki
    # ale średnio mi się ten pomysł podoba

    first, last = player_fullname.split("_")
    first = first.title()
    last = last.title()

    try:
        player = Player.objects.get(Q(first_name=first), Q(last_name=last))
    except Player.DoesNotExist:
        raise Http404

    team_name = str(player.team).replace(" ", "_")

    return render(request, 'Players/player_page.html', {'player': player, 'team_name': team_name})
