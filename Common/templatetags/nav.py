from django import template
from django.core.urlresolvers import reverse

from Teams.models import Team

register = template.Library()


@register.inclusion_tag('nav.html', takes_context=True)
def nav(context):
    links = [{'name': 'Home', 'url': reverse('home')},
             {'name': 'Teams', 'url': '/team/'},
             {'name': 'Players', 'url': reverse('player_index')},
             {'name': 'Games', 'url': reverse('game_index')},
             ]

    all_teams = []
    for team in Team.objects.all():
        all_teams.append(team)

    path = context['request'].path

    return {'links': links, 'all_teams': all_teams, 'path': path}