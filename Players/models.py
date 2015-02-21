from django.db import models
from django.utils.datetime_safe import date
from django.db.models import Q, Sum
from django.utils.functional import cached_property

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

    @cached_property
    def full_name(self):
        """Example: Michael Jordan"""
        return self.first_name + ' ' + self.last_name

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
        """Returns total sum of given statistic"""
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
        Creates a list of all boxscores of given player, with statistic fields from `stat_fields` list.

        The list has a format: [Short date, Opposing team with link, Game with link, STAT0, STAT1, ...]
        Boxscores are ordered by game date; 'W' or 'L' is shown before score, depending on who won; first score is of
        his team; 'vs' or 'at' is shown before opposing team, depending of who was the home team.
        Example:
            stats = ['min', 'pts', 'fgm', 'fga', 'fg_perc', 'three_pm', 'three_pa', 'three_perc',
                     'ftm', 'fta', 'ft_perc', 'reb_off', 'reb_def', 'reb_all', 'ast', 'stl', 'blk']
            leaders[0] = [18 Feb vs CHI, L 194 - 198, 29, 28, 8, 25, 0.32, 5, 13, 0.38, 7, 8, 0.88, 4, 9, 13, 13, 5, 1]
            leaders[1] = [23 Feb at NYK, W 231 - 213, 11 ,28, 9, 29, 0.31, 3, 10, 0.30, 7, 15, 0.47, 3, 9, 12, 2, 1, 2]
        """
        from Games.models import PlayerBoxscore

        season_stats = list()
        for player_box in PlayerBoxscore.objects.filter(player=self).order_by('game__date'):
            game_date = player_box.game.date.strftime("%d %b")
            game = player_box.game
            home_team = game.home_team
            away_team = game.away_team

            if player_box.game.home_team == self.team:
                opp = 'vs ' + '<a href="' + away_team.get_absolute_url() + '">' + away_team.short_name + '<a/>'

                if game.final_score['home_team'] > game.final_score['away_team']:
                    score = 'W <a href="' + game.get_absolute_url() + '" class="text-success">' + str(
                        game.final_score['home_team']) + ' - ' + str(game.final_score['away_team']) + '</a>'
                else:
                    score = 'L <a href="' + game.get_absolute_url() + '" class="text-danger">' + str(
                        game.final_score['home_team']) + ' - ' + str(game.final_score['away_team']) + '</a>'
            else:
                opp = 'at ' + '<a href="' + home_team.get_absolute_url() + '">' + home_team.short_name + '<a/>'

                if game.final_score['away_team'] > game.final_score['home_team']:
                    score = 'W <a href="' + game.get_absolute_url() + '" class="text-success">' + str(
                        game.final_score['away_team']) + ' - ' + str(game.final_score['home_team']) + '</a>'
                else:
                    score = 'L <a href="' + game.get_absolute_url() + '" class="text-danger">' + str(
                        game.final_score['away_team']) + ' - ' + str(game.final_score['home_team']) + '</a>'

            box = [game_date, opp, score]

            for item in stat_fields:
                box.append(getattr(player_box, item))

            season_stats.append(box)

        return season_stats

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse

        return reverse('player_page', args=[str(self.first_name) + '_' + str(self.last_name)])

    def __str__(self):
        """Example: Michael Jordan (Chicago Bulls)"""
        return self.first_name + ' ' + self.last_name + '(' + self.team.full_name + ')'