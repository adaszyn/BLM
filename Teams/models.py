from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property
from django.core.exceptions import ValidationError
from datetime import date


class Coach(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    birth_date = models.DateField()

    @cached_property
    def full_name(self):
        """Example: Phil Jackson"""
        return '{first_name} {last_name}'.format(first_name=self.first_name,
                                                 last_name=self.last_name)

    def __str__(self):
        """Example: Phil Jackson (Chicago Bulls) / Phil Jackson"""
        try:
            return '{first_name} {last_name} ({team})'.format(first_name=self.first_name,
                                                              last_name=self.last_name,
                                                              team=self.team.full_name)
        except Team.DoesNotExist:
            return self.full_name

    def clean(self):
        if self.birth_date >= date.today():
            raise ValidationError({'birth_date': "Coach can't be born in the future."})


class Team(models.Model):
    full_name = models.CharField(max_length=64)
    short_name = models.CharField(max_length=5)
    logo = models.ImageField(default='team_logos/default.png', upload_to='team_logos')
    description = models.TextField(max_length=1024, blank=True, default='')
    coach = models.OneToOneField(Coach)
    captain = models.ForeignKey('Players.Player', blank=True, null=True, related_name='team_captain',
                                on_delete=models.SET_NULL)

    class Meta:
        ordering = ['full_name']

    @cached_property
    def count_players(self):
        """Returns the number of players on the team"""
        from Players.models import Player

        return Player.objects.filter(team=self).count()
    count_players.short_description = 'Number of players'

    def team_players(self):
        """Returns the list of players in the team"""
        from Players.models import Player

        team_players = list()
        for player in Player.objects.filter(team=self):
            team_players.append(player)

        return team_players

    def games_played(self):
        """Returns the number of games the team played"""
        from Games.models import TeamBoxscore

        today = date.today()

        return TeamBoxscore.objects.filter(team=self).filter(game__date__lte=today).count()

    def team_average_leader(self, stat):
        # TODO: Poprawić z sortowaniem po stronie bazy (.extra)
        # TODO: Wiele graczy może mieć tą samą średnią
        # https://docs.djangoproject.com/en/dev/ref/models/querysets/#django.db.models.query.QuerySet.extra
        """Returns the player (and value) with best average in given statistic"""
        from Players.models import Player

        top_player = Player.objects.filter(team=self)[0]
        top_value = top_player.cat_average(stat)

        for player in Player.objects.filter(team=self):
            value = player.cat_average(stat)
            if value > top_value:
                top_player = player
                top_value = value

        return top_player, top_value

    def next_games(self, n):
        """Creates a list of `n` previous (if `n` is negative) or next (if `n` is positive) games of a team."""
        from Games.models import Game

        t = date.today()
        games_list = list()
        if n < 0:
            games = Game.objects.filter(Q(home_team=self) | Q(away_team=self)).filter(date__lt=t).order_by(
                '-date')[:-n]
        elif n > 0:
            games = Game.objects.filter(Q(home_team=self) | Q(away_team=self)).filter(date__gte=t).order_by(
                'date')[:n]
        else:
            raise Exception("Argument can't be 0")

        for game in games:
            games_list.append(game)

        return games_list

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse

        return reverse('team_page', args=[str(self.full_name.replace(' ', '_'))])

    def __str__(self):
        """Example: Chicago Bulls (CHI)"""
        return '{full_name} ({short_name})'.format(full_name=self.full_name, short_name=self.short_name)

    def clean(self):
        if self.captain_id is not None and self.captain.team != self:
            raise ValidationError({'captain': "Team captain has to be in the team."})

        self.short_name = self.short_name.upper()