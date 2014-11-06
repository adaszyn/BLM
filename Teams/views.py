from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from Teams.models import Team


def team_index(request):
    # TODO /team/

    return render(request, 'Teams/team_index.html')


def team_page(request, team_name):
    # TODO Lista zawodników danej drużyny

    team_name = team_name.replace("_", " ")
    team_name = team_name.title()

    try:
        team = Team.objects.get(full_name=team_name)
    except Team.DoesNotExist:
        raise Http404

    return render(request, 'Teams/team_page.html', {'team': team})
def teams_page(request, team_name):
    return HttpResponseRedirect("/team/"+team_name)
def teams_index(request):
    return HttpResponseRedirect("/team/")