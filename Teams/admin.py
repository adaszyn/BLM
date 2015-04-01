from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

from Teams.models import Team, Coach
from Players.models import Player


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    pass


class PlayersFormSet(BaseInlineFormSet):
    def clean(self):
        super(BaseInlineFormSet, self).clean()

        # Catch unique_together = ('team', 'number',) and show as ValidationError
        numbers = list()
        for form in self.forms:
            if not form.is_valid():
                return
            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                number = form.cleaned_data['number']
                if number in numbers:
                    raise ValidationError("Player number must be unique on the team.")
                numbers.append(number)


class PlayersInline(admin.TabularInline):
    model = Player
    extra = 5
    formset = PlayersFormSet


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    view_on_site = True
    list_display = ('pk', 'full_name', 'short_name', 'coach', 'captain', 'count_players', 'games_played',
                    'last_game', 'next_game')
    exclude = ['captain']
    inlines = [PlayersInline]

    @staticmethod
    def last_game(obj):
        try:
            return obj.next_games(-1)[0].short_name
        except IndexError:
            return None

    @staticmethod
    def next_game(obj):
        try:
            return obj.next_games(1)[0].short_name
        except IndexError:
            return None

    # Pass the object to request so it's accessible elsewhere
    def get_form(self, request, obj=None, **kwargs):
        request.obj = obj
        return super(TeamAdmin, self).get_form(request, obj, **kwargs)

    # Show only team players as captain choice
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if request.obj is not None:
            if db_field.name == 'captain':
                kwargs['queryset'] = Player.objects.filter(team=request.obj)
        return super(TeamAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # Captain field and no player fields in change view
    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = []
        self.exclude = []
        return super(TeamAdmin, self).change_view(request, object_id, form_url, extra_context)