from django.db import models
from django.db.models import Q, Sum

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
            return home_team.team
        else:
            return away_team.team

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
    blocks_against = models.PositiveIntegerField()
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
        # Aggregate returns dict; Why?
        # TODO Jak sprawić żeby /admin/ najpierw zapisywał wprowadzone PlayerBoxscore, potem tworzył GameBoxscore?
        # self.rebounds_def = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('rebounds_def'))['rebounds_def__sum']
        # self.rebounds_off = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('rebounds_off'))['rebounds_off__sum']
        # self.assists = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('assists'))['assists__sum']
        # self.steals = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('steals'))['steals__sum']
        # self.blocks = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('blocks'))['blocks__sum']
        # self.blocks_against = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('blocks_against'))['blocks_against__sum']
        # self.fgm = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('fgm'))['fgm__sum']
        # self.fga = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('fga'))['fga__sum']
        # self.three_pm = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('three_pm'))['three_pm__sum']
        # self.three_pa = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('three_pa'))['three_pa__sum']
        # self.three_perc = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('three_perc'))['three_perc__sum']
        # self.ftm = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('ftm'))['ftm__sum']
        # self.fta = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('fta'))['fta__sum']
        # self.personal_fouls = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('personal_fouls'))['personal_fouls__sum']

        # self.rebounds_all = self.rebounds_def + self.rebounds_off
        # self.fg_perc = 100 * self.fgm / self.fga
        # self.three_perc = 100 * self.three_pm / self.three_pa
        # self.ft_perc = 100 * self.ftm / self.fta

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
    team_boxscore = models.ForeignKey(TeamBoxscore)
    is_starter = models.BooleanField(default=False)
    minutes = models.PositiveIntegerField(verbose_name='MIN', null=True, blank=True)
    points = models.PositiveIntegerField(verbose_name='PTS', null=True, blank=True)
    rebounds_def = models.PositiveIntegerField(verbose_name='DEF', null=True, blank=True)
    rebounds_off = models.PositiveIntegerField(verbose_name='OFF', null=True, blank=True)
    rebounds_all = models.PositiveIntegerField(verbose_name='REB', null=True, blank=True, editable=False)
    assists = models.PositiveIntegerField(verbose_name='AST', null=True, blank=True)
    steals = models.PositiveIntegerField(verbose_name='STL', null=True, blank=True)
    blocks = models.PositiveIntegerField(verbose_name='BLK', null=True, blank=True)
    blocks_against = models.PositiveIntegerField(verbose_name='BA', null=True, blank=True)
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


class PeriodScore(models.Model):
    team_boxscore = models.ForeignKey(TeamBoxscore)
    quarter = models.PositiveIntegerField()
    points = models.PositiveIntegerField()

    def is_additional(self):
        return self.quarter > 4