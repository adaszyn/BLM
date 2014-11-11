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
    def save(self, *args, **kwargs):
        super(Game, self).save(*args, **kwargs)
        home_teamboxscore = TeamBoxscore(game=self,team=self.home_team, is_home=True)
        away_teamboxscore = TeamBoxscore(game=self,team=self.away_team,is_home=False)
        away_teamboxscore.save()
        home_teamboxscore.save()

class TeamBoxscore(models.Model):
    game = models.ForeignKey(Game)
    team = models.ForeignKey(Team)
    # Czy potrzebujemy?
    is_home = models.BooleanField(default=None, editable=False)
    points = models.PositiveIntegerField(default=0)
    rebounds_def = models.PositiveIntegerField(default=0)
    rebounds_off = models.PositiveIntegerField(default=0)
    rebounds_all = models.PositiveIntegerField(default=0, editable=False)
    assists = models.PositiveIntegerField(default=0)
    steals = models.PositiveIntegerField(default=0)
    blocks = models.PositiveIntegerField(default=0)
    blocks_against = models.PositiveIntegerField(default=0)
    turnovers = models.PositiveIntegerField(default=0)
    fgm = models.PositiveIntegerField(default=0)
    fga = models.PositiveIntegerField(default=0)
    fg_perc = models.FloatField(default=0, editable=False)
    three_pm = models.PositiveIntegerField(default=0)
    three_pa = models.PositiveIntegerField(default=0)
    three_perc = models.FloatField(default=0, editable=False)
    ftm = models.PositiveIntegerField(default=0)
    fta = models.PositiveIntegerField(default=0)
    ft_perc = models.FloatField(default=0, editable=False)
    personal_fouls = models.PositiveIntegerField(default=0)


    def save(self, *args, **kwargs):
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
    minutes = models.PositiveIntegerField(verbose_name='MIN')
    points = models.PositiveIntegerField(verbose_name='PTS')
    rebounds_def = models.PositiveIntegerField(verbose_name='DEF')
    rebounds_off = models.PositiveIntegerField(verbose_name='OFF')
    rebounds_all = models.PositiveIntegerField(verbose_name='REB', editable=False)
    assists = models.PositiveIntegerField(verbose_name='AST')
    steals = models.PositiveIntegerField(verbose_name='STL')
    blocks = models.PositiveIntegerField(verbose_name='BLK')
    blocks_against = models.PositiveIntegerField(verbose_name='BA')
    turnovers = models.PositiveIntegerField(verbose_name='TO')
    fgm = models.PositiveIntegerField(verbose_name='FGM')
    fga = models.PositiveIntegerField(verbose_name='FGA')
    fg_perc = models.FloatField(verbose_name='FG%', editable=False)
    three_pm = models.PositiveIntegerField(verbose_name='3PM')
    three_pa = models.PositiveIntegerField(verbose_name='3PA')
    three_perc = models.FloatField(verbose_name='3P%', editable=False)
    ftm = models.PositiveIntegerField(verbose_name='FTM')
    fta = models.PositiveIntegerField(verbose_name='FTA')
    ft_perc = models.FloatField(verbose_name='FT%', editable=False)
    personal_fouls = models.PositiveIntegerField(verbose_name='PF')

    def save(self, *args, **kwargs):
        self.rebounds_all = self.rebounds_def + self.rebounds_off
        self.fg_perc = 100 * self.fgm / self.fga
        self.three_perc = 100 * self.three_pm / self.three_pa
        self.ft_perc = 100 * self.ftm / self.fta

        # Updating TeamBoxscore
        # Aggregate returns dict; Why?
        self.team_boxscore.rebounds_def = PlayerBoxscore.objects.filter(team_boxscore=self.team_boxscore).aggregate(Sum('rebounds_def'))['rebounds_def__sum']
        self.team_boxscore.rebounds_off = PlayerBoxscore.objects.filter(team_boxscore=self.team_boxscore).aggregate(Sum('rebounds_off'))['rebounds_off__sum']
        self.team_boxscore.assists = PlayerBoxscore.objects.filter(team_boxscore=self.team_boxscore).aggregate(Sum('assists'))['assists__sum']
        self.team_boxscore.steals = PlayerBoxscore.objects.filter(team_boxscore=self.team_boxscore).aggregate(Sum('steals'))['steals__sum']
        self.team_boxscore.blocks = PlayerBoxscore.objects.filter(team_boxscore=self.team_boxscore).aggregate(Sum('blocks'))['blocks__sum']
        self.team_boxscore.blocks_against = PlayerBoxscore.objects.filter(team_boxscore=self.team_boxscore).aggregate(Sum('blocks_against'))['blocks_against__sum']
        self.team_boxscore.fgm = PlayerBoxscore.objects.filter(team_boxscore=self.team_boxscore).aggregate(Sum('fgm'))['fgm__sum']
        self.team_boxscore.fga = PlayerBoxscore.objects.filter(team_boxscore=self.team_boxscore).aggregate(Sum('fga'))['fga__sum']
        self.team_boxscore.three_pm = PlayerBoxscore.objects.filter(team_boxscore=self.team_boxscore).aggregate(Sum('three_pm'))['three_pm__sum']
        self.team_boxscore.three_pa = PlayerBoxscore.objects.filter(team_boxscore=self.team_boxscore).aggregate(Sum('three_pa'))['three_pa__sum']
        self.team_boxscore.three_perc = PlayerBoxscore.objects.filter(team_boxscore=self.team_boxscore).aggregate(Sum('three_perc'))['three_perc__sum']
        self.team_boxscore.ftm = PlayerBoxscore.objects.filter(team_boxscore=self.team_boxscore).aggregate(Sum('ftm'))['ftm__sum']
        self.team_boxscore.fta = PlayerBoxscore.objects.filter(team_boxscore=self.team_boxscore).aggregate(Sum('fta'))['fta__sum']
        self.team_boxscore.personal_fouls = PlayerBoxscore.objects.filter(team_boxscore=self.team_boxscore).aggregate(Sum('personal_fouls'))['personal_fouls__sum']
        self.team_boxscore.rebounds_all = self.team_boxscore.rebounds_def + self.team_boxscore.rebounds_off
        self.team_boxscore.fg_perc = 100 * self.team_boxscore.fgm / self.team_boxscore.fga
        self.team_boxscore.three_perc = 100 * self.team_boxscore.three_pm / self.team_boxscore.three_pa
        self.team_boxscore.ft_perc = 100 * self.team_boxscore.ftm / self.team_boxscore.fta

        super(PlayerBoxscore, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.player) + ' (' + str(self.team_boxscore.game.away_team) + ' @ ' + str(
            self.team_boxscore.game.home_team) + ', ' + self.team_boxscore.game.date.strftime("%d.%m.%Y") + ')'


# Czy na pewno tak ?
class PeriodScore(models.Model):
    team_boxscore = models.ForeignKey(TeamBoxscore)
    quarter = models.PositiveIntegerField()
    points = models.PositiveIntegerField()

    def is_additional(self):
        return self.quarter > 4