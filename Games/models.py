from django.db import models
from django.db.models import Q

from Players.models import Player
from Teams.models import Team


class Game(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_team')
    away_team = models.ForeignKey(Team, related_name='away_team')
    date = models.DateField()
    overtime = models.PositiveIntegerField(default=0)

    def who_won(self):
        home_team = TeamBoxscore.objects.get(Q(game=self), Q(team=self.home_team))
        away_team = TeamBoxscore.objects.get(Q(game=self), Q(team=self.away_team))
        if home_team.points > away_team.points:
            return home_team
        else:
            return away_team

    def save(self, *args, **kwargs):
        # TODO Stworzenie dwóch TeamBoxscore które zawierają sumę odpowiednich PlayerBoxscore
        super(Game, self).save(*args, **kwargs)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('game_page',
                       args=[self.date.strftime("%d.%m.%Y"), self.away_team.short_name, self.home_team.short_name])

    def __str__(self):
        return str(self.away_team) + ' @ ' + str(self.home_team) + ' (' + self.date.strftime("%d.%m.%Y") + ')'


class TeamBoxscore(models.Model):
    game = models.ForeignKey(Game)
    team = models.ForeignKey(Team)
    is_home = models.BooleanField(default=None, editable=False)
    points = models.PositiveIntegerField()
    rebounds_def = models.PositiveIntegerField()
    rebounds_off = models.PositiveIntegerField()
    rebounds_all = models.PositiveIntegerField(editable=False)
    assists = models.PositiveIntegerField()
    steals = models.PositiveIntegerField()
    blocks = models.PositiveIntegerField()
    block_against = models.PositiveIntegerField()
    turnovers = models.PositiveIntegerField()
    fgm = models.PositiveIntegerField()
    fga = models.PositiveIntegerField()
    fg_perc = models.DecimalField(max_digits=4, decimal_places=2, editable=False)
    three_pm = models.PositiveIntegerField()
    three_pa = models.PositiveIntegerField()
    three_perc = models.DecimalField(max_digits=4, decimal_places=2, editable=False)
    ftm = models.PositiveIntegerField()
    fta = models.PositiveIntegerField()
    ft_perc = models.DecimalField(max_digits=4, decimal_places=2, editable=False)
    personal_fouls = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        self.rebounds_all = self.rebounds_def + self.rebounds_off
        self.fg_perc = 100 * self.fgm / self.fga
        self.three_perc = 100 * self.three_pm / self.three_pa
        self.ft_perc = 100 * self.ftm / self.fta

        if self.game.home_team == self.team:
            self.is_home = True
        else:
            self.is_home = False

        super(TeamBoxscore, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.team) + ' (' + str(self.game.away_team) + ' @ ' + str(
            self.game.home_team) + ', ' + self.game.date.strftime("%d.%m.%Y") + ')'


class PlayerBoxscore(models.Model):
    player = models.ForeignKey(Player)
    team = models.ForeignKey(Team)
    game = models.ForeignKey(Game)
    is_starter = models.BooleanField(default=False)
    minutes = models.PositiveIntegerField(verbose_name='MIN', null=True, blank=True)
    points = models.PositiveIntegerField(verbose_name='PTS', null=True, blank=True)
    rebound_def = models.PositiveIntegerField(verbose_name='DEF', null=True, blank=True)
    rebound_off = models.PositiveIntegerField(verbose_name='OFF', null=True, blank=True)
    rebounds_all = models.PositiveIntegerField(verbose_name='REB', null=True, blank=True, editable=False)
    assists = models.PositiveIntegerField(verbose_name='AST', null=True, blank=True)
    steals = models.PositiveIntegerField(verbose_name='STL', null=True, blank=True)
    blocks = models.PositiveIntegerField(verbose_name='BLK', null=True, blank=True)
    block_against = models.PositiveIntegerField(verbose_name='BA', null=True, blank=True)
    turnovers = models.PositiveIntegerField(verbose_name='TO', null=True, blank=True)
    fgm = models.PositiveIntegerField(verbose_name='FGM', null=True, blank=True)
    fga = models.PositiveIntegerField(verbose_name='FGA', null=True, blank=True)
    fg_perc = models.DecimalField(verbose_name='FG%', null=True, blank=True, max_digits=4, decimal_places=2, editable=False)
    three_pm = models.PositiveIntegerField(verbose_name='3PM', null=True, blank=True)
    three_pa = models.PositiveIntegerField(verbose_name='3PA', null=True, blank=True)
    three_perc = models.DecimalField(verbose_name='3P%', null=True, blank=True, max_digits=4, decimal_places=2, editable=False)
    ftm = models.PositiveIntegerField(verbose_name='FTM', null=True, blank=True)
    fta = models.PositiveIntegerField(verbose_name='FTA', null=True, blank=True)
    ft_perc = models.DecimalField(verbose_name='FT%', null=True, blank=True, max_digits=4, decimal_places=2, editable=False)
    personal_fouls = models.PositiveIntegerField(verbose_name='PF', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.rebounds_all = self.rebounds_def + self.rebounds_off
        self.fg_perc = 100 * self.fgm / self.fga
        self.three_perc = 100 * self.three_pm / self.three_pa
        self.ft_perc = 100 * self.ftm / self.fta

        super(PlayerBoxscore, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.player) + ' (' + str(self.game.away_team) + ' @ ' + str(
            self.game.home_team) + ', ' + self.game.date.strftime("%d.%m.%Y") + ')'


# TODO Czy na pewno tak?
class PeriodScore(models.Model):
    team_boxscore = models.ForeignKey(TeamBoxscore)
    quarter = models.PositiveIntegerField()
    points = models.PositiveIntegerField()

    def is_additional(self):
        return self.quarter > 4