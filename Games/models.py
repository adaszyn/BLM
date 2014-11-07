from django.db import models
from Players.models import Player
from Teams.models import Team


class Game(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_team')
    away_team = models.ForeignKey(Team, related_name='away_team')
    date = models.DateField()
    overtime = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('game_page', args=[self.date.strftime("%d.%m.%Y"), self.away_team, self.home_team])

    def __str__(self):
        return str(self.away_team) + ' @ ' + str(self.home_team) + ' (' + self.date.strftime("%d.%m.%Y") + ')'


class GameBoxscore(models.Model):
    game = models.ForeignKey(Game)
    team = models.ForeignKey(Team)
    result = models.BooleanField(default=None)  # TODO Change to Win/Lost dropdown
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

        super(GameBoxscore, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.team) + ' (' + str(self.game.away_team) + ' @ ' + str(
            self.game.home_team) + ', ' + self.game.date.strftime("%d.%m.%Y") + ')'


class PlayerBoxscore(models.Model):

    player = models.ForeignKey(Player)
    game_boxscore = models.ForeignKey(GameBoxscore)
    is_starter = models.BooleanField(default=None)
    minutes = models.PositiveIntegerField()
    points = models.PositiveIntegerField()
    rebound_def = models.PositiveIntegerField()
    rebound_off = models.PositiveIntegerField()
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

        super(PlayerBoxscore, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.player) + ' (' + str(self.game.away_team) + ' @ ' + str(
            self.game.home_team) + ', ' + self.game.date.strftime("%d.%m.%Y") + ')'


class PeriodScore(models.Model):
    game_boxscore = models.ForeignKey(GameBoxscore)
    quarter = models.PositiveIntegerField()
    points = models.PositiveIntegerField()

    def is_additional(self):
        return self.quarter > 4