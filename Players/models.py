from django.db import models
from django.utils.datetime_safe import date
from django.db.models import Q, Sum
from django.utils.functional import cached_property
from collections import OrderedDict

from Teams.models import Team


class Player(models.Model):
    position_choices = (
        ('PG', 'Point Guard'),
        ('PG/SG', 'Point Guard/Shooting Guard'),
        ('SG', 'Shooting Guard'),
        ('SG/SF', 'Shooting Guard/Small Forward'),
        ('SF', 'Small Forward'),
        ('SF/PF', 'Small Forward/Power Forward'),
        ('PF', 'Power Forward'),
        ('PF/C', 'Power Forward/Center'),
        ('C', 'Center'),
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    team = models.ForeignKey(Team)
    is_captain = models.BooleanField(default=False)
    position = models.CharField(max_length=5, choices=position_choices)
    birth_date = models.DateField()
    height = models.PositiveIntegerField(verbose_name='Height [cm]')
    weight = models.PositiveIntegerField(verbose_name='Weight [kg]')
    number = models.PositiveIntegerField()
    image = models.ImageField(verbose_name='Player photo', default='player_photos/default.jpg',
                              upload_to='player_photos')

    class Meta:
        ordering = ['last_name', 'first_name']

    @cached_property
    def full_name(self):
        """Example: Michael Jordan"""
        return '{first_name} {last_name}'.format(first_name=self.first_name,
                                                 last_name=self.last_name)

    @cached_property
    def age(self):
        """Returns age of the player"""
        born = self.birth_date
        today = date.today()
        try:
            birthday = born.replace(year=today.year)
        except ValueError:  # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year, month=born.month + 1, day=1)
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

    def number_of_games(self):
        """Returns the number of games played by the player (min > 0)"""
        from Games.models import PlayerBoxscore

        return PlayerBoxscore.objects.filter(player=self).filter(min__gt=0).count()

    def cat_total(self, stat):
        """Returns total sum of given statistic (overall percentage in case of percentages)"""
        from Games.models import PlayerBoxscore

        # Calculates percentage from total values, instead of rounded game percentages
        if stat == 'fg_perc':
            return '{0:.3f}'.format(self.cat_total('fgm') / self.cat_total('fga'))
        elif stat == 'three_perc':
            return '{0:.3f}'.format(self.cat_total('three_pm') / self.cat_total('three_pa'))
        elif stat == 'ft_perc':
            return '{0:.3f}'.format(self.cat_total('ftm') / self.cat_total('fta'))
        else:
            return PlayerBoxscore.objects.filter(player=self).aggregate(total=Sum(stat))['total']

    def cat_average(self, stat):
        """Returns per game average of given statistic, rounded to one decimal place"""
        from Games.models import PlayerBoxscore

        # No such thing as average percentage
        if stat in ['fg_perc', 'three_perc', 'ft_perc']:
            return self.cat_total(stat)
        else:
            return '{0:.1f}'.format(self.cat_total(stat) / self.number_of_games())

    def season_stats(self, stat_fields):
        """
        Creates an OrderedDict of all boxscores of given player,
        with statistic fields from `stat_fields` list as a value and Game as a key.

        The dict has a format: dict[Game] = [STAT0, STAT1, ...]
        Example:
            stats = ['min', 'pts', 'fgm', 'fga', 'fg_perc', 'three_pm', 'three_pa', 'three_perc',
                     'ftm', 'fta', 'ft_perc', 'reb_off', 'reb_def', 'reb_all', 'ast', 'stl', 'blk']
            season_stats[CHI at NYK] = [29, 28, 8, 25, 0.32, 5, 13, 0.38, 7, 8, 0.88, 4, 9, 13, 13, 5, 1]
        """
        from Games.models import PlayerBoxscore

        season_stats = OrderedDict()
        for player_box in PlayerBoxscore.objects.filter(player=self).order_by('game__date'):
            season_stats[player_box.game] = list()

            for item in stat_fields:
                season_stats[player_box.game].append(getattr(player_box, item))

        return season_stats

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse

        return reverse('player_page', args=[str(self.first_name) + '_' + str(self.last_name)])

    def __str__(self):
        """Example: Michael Jordan (Chicago Bulls)"""
        return '{first_name} {last_name} ({team})'.format(first_name=self.first_name,
                                                          last_name=self.last_name,
                                                          team=self.team.full_name)