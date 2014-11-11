from django.contrib import admin
from django import forms
from django.forms import ModelForm, BaseInlineFormSet
from Games.models import Game, PlayerBoxscore, TeamBoxscore, PeriodScore
from Teams.models import Team
from Players.models import Player
from django.utils.functional import curry

class PeriodScoreInline(admin.TabularInline):
    model = PeriodScore
    extra = 4
    def get_formset(self, request, obj=None, **kwargs):
        initial = []
        if request.method == "GET":
            for i in range(1,7):
                initial.append({
                    'quarter': i,
                })
        formset = super(PeriodScoreInline, self).get_formset(request, obj, **kwargs)
        formset.__init__ = curry(formset.__init__, initial=initial)
        return formset

class PlayerBoxscoreInline(admin.TabularInline):
    model = PlayerBoxscore
    extra = 5
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

        field = super(PlayerBoxscoreInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'player':
            if request._obj_ is not None:
                field.queryset = field.queryset.filter(team__exact = request._obj_.team)
            else:
                field.queryset = field.queryset.none()

        return field


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'who_won', 'date', 'overtime')
    list_filter = ['home_team', 'away_team', 'date', 'overtime']
    view_on_site = True

    fieldsets = [
        ('Team info', {'fields': ['home_team', 'away_team', 'date', 'overtime']}),
    ]

class TeamBoxScoreAdminForm(ModelForm):
    class Meta:
        model = TeamBoxscore

@admin.register(TeamBoxscore)
class TeamBoxscoreAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        return super(TeamBoxscoreAdmin, self).get_form(request, obj, **kwargs)

    list_display = ('team','game')
    list_filter = ['game', 'team']
    view_on_site = False

    exclude = ['game', 'team', 'rebounds_def','rebounds_off','assists','points','steals','blocks','fgm','fga','three_pm', 'ftm', 'fta','three_pa','blocks_against','turnovers','personal_fouls']
    inlines = [PeriodScoreInline, PlayerBoxscoreInline]


@admin.register(PlayerBoxscore)
class PlayerBoxscoreAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Team info', {'fields':['team_boxscore']}),
    ]
