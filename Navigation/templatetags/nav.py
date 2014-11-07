from django import template
from django.core.urlresolvers import reverse

from Teams.models import Team

register = template.Library()

@register.inclusion_tag('nav.html', takes_context=True)
def nav(context):
    links = [{'name': 'Home', 'url': reverse('home')},
             {'name': 'Teams', 'url': reverse('team_index')},
             {'name': 'Players', 'url': reverse('player_index')},
             {'name': 'Games', 'url': reverse('game_index')},
             ]

    teams = []
    for team in Team.objects.all():
        team_name = team.full_name.replace(" ", "_")
        teams.append({'name': team.full_name, 'url': reverse('team_page', kwargs={'team_name': team_name})})

    path = context['request'].path

    return {'links': links, 'teams': teams, 'path': path}