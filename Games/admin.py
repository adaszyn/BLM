from django.contrib import admin

from Games.models import Game, PlayerBoxscore


class PlayerBoxscoreInline(admin.TabularInline):
    model = PlayerBoxscore
    extra = 5


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'who_won', 'date', 'overtime')
    list_filter = ['home_team', 'away_team', 'date', 'overtime']
    view_on_site = True

    fieldsets = [
        ('Team info', {'fields': ['home_team', 'away_team', 'date', 'overtime']}),
    ]
    # inlines = [PlayerBoxscoreInline]
    # TODO Wyświetlanie wszystkich zawodników tylko z podanych drużyn; Kurwa, ale męczarnia