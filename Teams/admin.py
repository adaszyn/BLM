from django.contrib import admin

from Teams.models import Team
from Players.models import Player


class PlayersInline(admin.TabularInline):
    model = Player
    extra = 1


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'short_name', 'count_players')
    view_on_site = True

    fieldsets = [
        ('Team info', {'fields': ['full_name', 'short_name', 'logo', 'description']}),
    ]
    inlines = [PlayersInline]