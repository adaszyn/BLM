from django.contrib import admin

from Games.models import Game, PlayerBoxscore, TeamBoxscore, PeriodScore


class PeriodScoreInline(admin.TabularInline):
    model = PeriodScore
    extra = 4


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


@admin.register(TeamBoxscore)
class TeamBoxscoreAdmin(admin.ModelAdmin):
    # TODO Wyświetlanie w dropdown tylko drużyn z danego meczu, i tylko zawodników z danej drużyny
    list_display = ('game', 'team')
    list_filter = ['game', 'team']
    view_on_site = False

    fieldsets = [
        ('Team info', {'fields': ['game', 'team']}),
    ]
    inlines = [PeriodScoreInline, PlayerBoxscoreInline]