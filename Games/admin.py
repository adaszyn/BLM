from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import date

from Games.models import Game, PeriodScore, PlayerBoxscore, TeamBoxscore
from Players.models import Player


class PeriodScoresFormSet(BaseInlineFormSet):
    def clean(self):
        super(BaseInlineFormSet, self).clean()

        # Hack to compare it with sum of points form PlayerBoxscores
        global ps_score
        ps_score = score_after_4th = {'away_team': 0, 'home_team': 0}
        q = 1
        for form in self.forms:
            if not form.is_valid():
                return
            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                ps_score['away_team'] += form.cleaned_data['away_team']
                ps_score['home_team'] += form.cleaned_data['home_team']

                if q == 4:
                    score_after_4th = ps_score

                if form.cleaned_data['quarter'] != q:
                    raise ValidationError("Fix quarter values.")
                q += 1

        if q < 4:
            raise ValidationError("Game has to have at least 4 quarters.")

        if ps_score['away_team'] == ps_score['home_team']:
            raise ValidationError("Teams can't have the same number of points.")

        if score_after_4th['away_team'] != score_after_4th['home_team'] and q > 4:
            raise ValidationError("There can't be overtime if teams have different scores after 4 quarters.")


class PeriodScoresInline(admin.TabularInline):
    model = PeriodScore
    extra = 0
    formset = PeriodScoresFormSet


class PlayerBoxscoresFormSet(BaseInlineFormSet):
    def clean(self):
        super(BaseInlineFormSet, self).clean()

        total_starters = 0
        total_minutes = 0
        bx_score = 0
        team = None
        for form in self.forms:
            if not form.is_valid():
                return
            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                if form.cleaned_data['is_starter']:
                    total_starters += 1
                total_minutes += form.cleaned_data['min']
                # Because Team is a field in PlayerBoxscore
                team = form.instance.team = form.cleaned_data['team'] = form.cleaned_data['player'].team
                bx_score += (form.cleaned_data['ftm'] +
                             (form.cleaned_data['fgm'] - form.cleaned_data['three_pm']) * 2 +
                             form.cleaned_data['three_pm'] * 3)

        if total_starters != 5:
            raise ValidationError("There has to be exactly five starters on a team.")

        # TODO: Zmienna minut w kwarcie
        if total_minutes != 240:
            raise ValidationError("Sum of all players minutes must be equal to 240.")

        if team == self.instance.away_team:
            if bx_score != ps_score['away_team']:
                raise ValidationError(("Sum of points in players stats must be equal to "
                                       "sum of points in period scores ({0} != {1}).").format(ps_score['away_team'],
                                                                                              bx_score))
        elif team == self.instance.home_team:
            if bx_score != ps_score['home_team']:
                raise ValidationError(("Sum of points in players stats must be equal to "
                                       "sum of points in period scores ({0} != {1}).").format(ps_score['home_team'],
                                                                                              bx_score))


class AwayPlayerBoxscoresInline(admin.TabularInline):
    model = PlayerBoxscore
    verbose_name_plural = 'Away players'
    exclude = ['team']  # Because Team is a field in PlayerBoxscore
    extra = 5
    formset = PlayerBoxscoresFormSet

    # Show only players from the away team to choose
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if request.obj is not None:
            if db_field.name == 'player':
                kwargs['queryset'] = Player.objects.filter(team=request.obj.away_team)
        return super(AwayPlayerBoxscoresInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # Show only away team players PlayerBoxscore
    def get_queryset(self, request):
        qs = super(AwayPlayerBoxscoresInline, self).get_queryset(request)
        if request.obj is not None:
            return qs.filter(game=request.obj).filter(player__team=request.obj.away_team)
        else:
            return qs

    # Show 5 forms when first changed, then 0
    def get_formset(self, request, obj=None, **kwargs):
        qs = super(AwayPlayerBoxscoresInline, self).get_queryset(request)
        if request.obj is not None:
            new_qs = qs.filter(game=request.obj).filter(player__team=request.obj.away_team)
            kwargs['extra'] = 5 if new_qs.count() == 0 else 0
        return super(AwayPlayerBoxscoresInline, self).get_formset(request, obj, **kwargs)


class HomePlayerBoxscoresInline(admin.TabularInline):
    model = PlayerBoxscore
    verbose_name_plural = 'Home players'
    exclude = ['team']  # Because Team is a field in PlayerBoxscore
    extra = 5
    formset = PlayerBoxscoresFormSet

    # Show only players from the home team to choose
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if request.obj is not None:
            if db_field.name == 'player':
                kwargs['queryset'] = Player.objects.filter(team=request.obj.home_team)
        return super(HomePlayerBoxscoresInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # Show only home team players PlayerBoxscore
    def get_queryset(self, request):
        qs = super(HomePlayerBoxscoresInline, self).get_queryset(request)
        if request.obj is not None:
            return qs.filter(game=request.obj).filter(player__team=request.obj.home_team)
        else:
            return qs

    # Show 5 forms when first changed, then 0
    def get_formset(self, request, obj=None, **kwargs):
        qs = super(HomePlayerBoxscoresInline, self).get_queryset(request)
        if request.obj is not None:
            new_qs = qs.filter(game=request.obj).filter(player__team=request.obj.home_team)
            kwargs['extra'] = 5 if new_qs.count() == 0 else 0
        return super(HomePlayerBoxscoresInline, self).get_formset(request, obj, **kwargs)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    view_on_site = True
    list_display = ('pk', 'away_team', 'home_team', 'date', 'happened', 'winner', 'score', 'overtime')
    list_filter = ['away_team', 'home_team']
    inlines = []

    @staticmethod
    def score(obj):
        return '{away} - {home}'.format(away=obj.final_score['away_team'], home=obj.final_score['home_team'])

    # Pass the object to request so it's accessible elsewhere
    def get_form(self, request, obj=None, **kwargs):
        request.obj = obj
        return super(GameAdmin, self).get_form(request, obj, **kwargs)

    # Show PeriodScores and PlayerBoxscores only in change view of non-future game
    def change_view(self, request, object_id, form_url='', extra_context=None):
        if self.get_object(request, object_id).date <= date.today():
            self.inlines = [PeriodScoresInline, AwayPlayerBoxscoresInline, HomePlayerBoxscoresInline]
        else:
            self.inlines = []
        return super(GameAdmin, self).change_view(request, object_id, form_url, extra_context)

    def save_related(self, request, form, formsets, change):
        super(GameAdmin, self).save_related(request, form, formsets, change)
        game = form.instance

        # Create 4 PeriodScores when first saved
        if PeriodScore.objects.filter(game=game).count() == 0:
            for i in range(1, 5):
                PeriodScore(game=game, quarter=i).save()

        # Create TeamBoxscores when Game is first changed
        if TeamBoxscore.objects.filter(game=game).count() == 0 and change:
            TeamBoxscore(game=game, team=game.away_team).save()
            TeamBoxscore(game=game, team=game.home_team).save()

        # Update TeamBoxscores when everything is saved
        if TeamBoxscore.objects.filter(game=game).count() == 2:
            TeamBoxscore.objects.get(Q(game=game), Q(team=game.away_team)).save(force_update=True)
            TeamBoxscore.objects.get(Q(game=game), Q(team=game.home_team)).save(force_update=True)