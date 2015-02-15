from django.db import models
from django.db.models import Q

from Players.models import Player
from Teams.models import Team


class Game(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_team')
    away_team = models.ForeignKey(Team, related_name='away_team')
    date = models.DateField()

    def who_won(self):
        home_team_box = TeamBoxscore.objects.get(Q(game=self), Q(team=self.home_team))
        away_team_box = TeamBoxscore.objects.get(Q(game=self), Q(team=self.away_team))
        if home_team_box.pts > away_team_box.pts:
            return home_team_box.team
        else:
            return away_team_box.team

    # Returns the number of overtime periods; 0 when no overtime
    def overtime(self):
        return PeriodScore.objects.filter(game__exact=self).count - 4

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse

        return reverse('game_page',
                       args=[self.date.strftime("%d.%m.%Y"), self.away_team.short_name, self.home_team.short_name])

    def __str__(self):
        return str(self.away_team) + ' @ ' + str(self.home_team) + ' (' + self.date.strftime("%d.%m.%Y") + ')'


class PlayerBoxscore(models.Model):
    player = models.ForeignKey(Player)
    team = models.ForeignKey(Team)
    game = models.ForeignKey(Game)
    is_starter = models.BooleanField(default=False)
    min = models.PositiveIntegerField(verbose_name='MIN', default=0)
    reb_def = models.PositiveIntegerField(verbose_name='DEF', default=0)
    reb_off = models.PositiveIntegerField(verbose_name='OFF', default=0)
    ast = models.PositiveIntegerField(verbose_name='AST', default=0)
    stl = models.PositiveIntegerField(verbose_name='STL', default=0)
    blk = models.PositiveIntegerField(verbose_name='BLK', default=0)
    ba = models.PositiveIntegerField(verbose_name='BA', default=0)
    to = models.PositiveIntegerField(verbose_name='TO', default=0)
    fgm = models.PositiveIntegerField(verbose_name='FGM', default=0)
    fga = models.PositiveIntegerField(verbose_name='FGA', default=0)
    three_pm = models.PositiveIntegerField(verbose_name='3PM', default=0)
    three_pa = models.PositiveIntegerField(verbose_name='3PA', default=0)
    ftm = models.PositiveIntegerField(verbose_name='FTM', default=0)
    fta = models.PositiveIntegerField(verbose_name='FTA', default=0)
    pf = models.PositiveIntegerField(verbose_name='PF', default=0)

    def _pts(self):
        return self.ftm + self.fgm * 2 + self.three_pm * 3

    pts = property(_pts)

    def _reb_all(self):
        return self.rebounds_def + self.rebounds_off

    reb_all = property(_reb_all)

    def _fg_perc(self):
        if self.fga == 0:
            return "-"
        else:
            return round(self.fgm / self.fga, 3) * 100

    fg_perc = property(_fg_perc)

    def _three_perc(self):
        if self.three_pa == 0:
            return "-"
        else:
            return round(self.three_pm / self.three_pa, 3) * 100

    three_perc = property(_three_perc)

    def _ft_perc(self):
        if self.fta == 0:
            return "-"
        else:
            return round(self.ftm / self.fta, 3) * 100

    ft_perc = property(_ft_perc)

    def __str__(self):
        return str(self.player) + ' (' + str(self.game.away_team) + ' @ ' + str(
            self.game.home_team) + ', ' + self.game.date.strftime("%d.%m.%Y") + ')'


class TeamBoxscore(models.Model):
    game = models.ForeignKey(Game)
    team = models.ForeignKey(Team)
    reb_def = models.PositiveIntegerField(default=0, editable=False)
    reb_off = models.PositiveIntegerField(default=0, editable=False)
    ast = models.PositiveIntegerField(default=0, editable=False)
    stl = models.PositiveIntegerField(default=0, editable=False)
    blk = models.PositiveIntegerField(default=0, editable=False)
    ba = models.PositiveIntegerField(default=0, editable=False)
    to = models.PositiveIntegerField(default=0, editable=False)
    fgm = models.PositiveIntegerField(default=0, editable=False)
    fga = models.PositiveIntegerField(default=0, editable=False)
    three_pm = models.PositiveIntegerField(default=0, editable=False)
    three_pa = models.PositiveIntegerField(default=0, editable=False)
    ftm = models.PositiveIntegerField(default=0, editable=False)
    fta = models.PositiveIntegerField(default=0, editable=False)
    pf = models.PositiveIntegerField(default=0, editable=False)

    def _pts(self):
        return self.ftm + self.fgm * 2 + self.three_pm * 3

    pts = property(_pts)

    def _reb_all(self):
        return self.rebounds_def + self.rebounds_off

    reb_all = property(_reb_all)

    def _fg_perc(self):
        if self.fga == 0:
            return "-"
        else:
            return round(self.fgm / self.fga, 3) * 100

    fg_perc = property(_fg_perc)

    def _three_perc(self):
        if self.three_pa == 0:
            return "-"
        else:
            return round(self.three_pm / self.three_pa, 3) * 100

    three_perc = property(_three_perc)

    def _ft_perc(self):
        if self.fta == 0:
            return "-"
        else:
            return round(self.ftm / self.fta, 3) * 100

    ft_perc = property(_ft_perc)

    def __str__(self):
        return str(self.team) + ' (' + str(self.game.away_team) + ' @ ' + str(
            self.game.home_team) + ', ' + self.game.date.strftime("%d.%m.%Y") + ')'


class PeriodScore(models.Model):
    game = models.ForeignKey(Game)
    quarter = models.PositiveIntegerField()
    home_team_points = models.PositiveIntegerField()
    away_team_points = models.PositiveIntegerField()

    def __str__(self):
        return str(self.game.home_team) + " : " + str(self.home_team_points) + " | " + str(
            self.game.away_team) + " : " + str(self.away_team_points)