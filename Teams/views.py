from django.http import Http404
from django.shortcuts import render

from Teams.models import Team

# TODO Drużyny z polskimi znakami
# @wojtek zastanów się jak to zrobić
# Ja póki co widzę tylko dodanie do modelu pola '*_name_en' które zawiera to samo co '*_name' ale przesiane przez:
# abc.translate(str.maketrans("ąćęłńóśżźĄĆĘŁŃÓŚŻŹ", "acelnoszzACELNOSZZ"))
# ^ zamienia w abc polskie znaki an angielskie odpowiedniki
# ale średnio mi się ten pomysł podoba


def team_index(request):
    # TODO Wyświetlanie spisu drużyn

    return render(request, 'Teams/team_index.html', {'teams': teams})


def team_page(request, team_name):
    team_name = team_name.replace("_", " ")
    team_name = team_name.title()

    try:
        team = Team.objects.get(full_name=team_name)
    except Team.DoesNotExist:
        raise Http404

    return render(request, 'Teams/team_page.html', {'team': team})
