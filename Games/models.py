from django.db import models
from django.db.models import Q, Sum
from django.utils.functional import cached_property
from datetime import datetime

from Players.models import Player
from Teams.models import Team


class Game(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_team')
    away_team = models.ForeignKey(Team, related_name='away_team')
    date = models.DateField()

    @cached_property
    def happened(self):
        """Returns True if the game happened"""
        if self.date < datetime.today().date() and TeamBoxscore.objects.filter(game=self).count() == 2:
            return True
        else:
            return False

    @cached_property
    def final_score(self):
        """Returns a dict with teams final score"""
        final_score = {'home_team': TeamBoxscore.objects.get(Q(game=self), Q(team=self.home_team)).pts,
                       'away_team': TeamBoxscore.objects.get(Q(game=self), Q(team=self.away_team)).pts}

        return final_score

    @cached_property
    def winner(self):
        """Returns the team that won"""
        if self.final_score['home_team'] > self.final_score['away_team']:
            return self.home_team
        else:
            return self.away_team

    @cached_property
    def overtime(self):
        """Returns number of overtimes; 0 if none"""
        return PeriodScore.objects.filter(game=self).count - 4

    @cached_property
    def short_name(self):
        """Example: CHI at NYK (01.01.2000)"""
        return str(self.away_team.short_name) + ' at ' + str(self.home_team.short_name) + ' (' + self.date.strftime(
            "%d.%m.%Y") + ')'

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse

        return reverse('game_page',
                       args=[self.date.strftime("%Y-%m-%d"), self.away_team.short_name, self.home_team.short_name])

    def __str__(self):
        """Example: Chicago Bulls at New York Knicks (01.01.2000)"""
        return str(self.away_team.full_name) + ' at ' + str(self.home_team.full_name) + ' (' + self.date.strftime(
            "%d.%m.%Y") + ')'


class PlayerBoxscore(models.Model):
    player = models.ForeignKey(Player)
    team = models.ForeignKey(Team)
    game = models.ForeignKey(Game)
    is_starter = models.BooleanField(default=False)
    min = models.PositiveIntegerField(verbose_name='MIN', default=0)
    pts = models.PositiveIntegerField(verbose_name='PTS', default=0, editable=False)
    reb_def = models.PositiveIntegerField(verbose_name='DEF', default=0)
    reb_off = models.PositiveIntegerField(verbose_name='OFF', default=0)
    reb_all = models.PositiveIntegerField(verbose_name='REB', default=0, editable=False)
    ast = models.PositiveIntegerField(verbose_name='AST', default=0)
    stl = models.PositiveIntegerField(verbose_name='STL', default=0)
    blk = models.PositiveIntegerField(verbose_name='BLK', default=0)
    ba = models.PositiveIntegerField(verbose_name='BA', default=0)
    to = models.PositiveIntegerField(verbose_name='TO', default=0)
    fgm = models.PositiveIntegerField(verbose_name='FGM', default=0)
    fga = models.PositiveIntegerField(verbose_name='FGA', default=0)
    fg_perc = models.TextField(verbose_name='FG%', default=0, editable=False)
    three_pm = models.PositiveIntegerField(verbose_name='3PM', default=0)
    three_pa = models.PositiveIntegerField(verbose_name='3PA', default=0)
    three_perc = models.TextField(verbose_name='3P%', default=0, editable=False)
    ftm = models.PositiveIntegerField(verbose_name='FTM', default=0)
    fta = models.PositiveIntegerField(verbose_name='FTA', default=0)
    ft_perc = models.TextField(verbose_name='FT%', default=0, editable=False)
    pf = models.PositiveIntegerField(verbose_name='PF', default=0)

    def __str__(self):
        """Example: Michael Jordan (CHI at NYK, 01.01.2000)"""
        return str(self.player) + ' (' + str(self.game.away_team) + ' at ' + str(
            self.game.home_team) + ', ' + self.game.date.strftime("%d.%m.%Y") + ')'

    def save(self, *args, **kwargs):
        self.pts = self.ftm + (self.fgm - self.three_pm) * 2 + self.three_pm * 3
        self.reb_all = self.rebounds_def + self.rebounds_off
        self.fg_perc = '{0:.3f}'.format(self.fgm / self.fga) if self.fga > 0 else '-'
        self.three_perc = '{0:.3f}'.format(self.three_pm / self.three_pa) if self.three_pa > 0 else '-'
        self.ft_perc = '{0:.3f}'.format(self.ftm / self.fta) if self.fta > 0 else '-'
        super(PlayerBoxscore, self).save(*args, **kwargs)


class TeamBoxscore(models.Model):
    game = models.ForeignKey(Game)
    team = models.ForeignKey(Team)
    pts = models.PositiveIntegerField(default=0, editable=False)
    reb_def = models.PositiveIntegerField(default=0, editable=False)
    reb_off = models.PositiveIntegerField(default=0, editable=False)
    reb_all = models.PositiveIntegerField(default=0, editable=False)
    ast = models.PositiveIntegerField(default=0, editable=False)
    stl = models.PositiveIntegerField(default=0, editable=False)
    blk = models.PositiveIntegerField(default=0, editable=False)
    ba = models.PositiveIntegerField(default=0, editable=False)
    to = models.PositiveIntegerField(default=0, editable=False)
    fgm = models.PositiveIntegerField(default=0, editable=False)
    fga = models.PositiveIntegerField(default=0, editable=False)
    fg_perc = models.TextField(default=0, editable=False)
    three_pm = models.PositiveIntegerField(default=0, editable=False)
    three_pa = models.PositiveIntegerField(default=0, editable=False)
    three_perc = models.TextField(default=0, editable=False)
    ftm = models.PositiveIntegerField(default=0, editable=False)
    fta = models.PositiveIntegerField(default=0, editable=False)
    ft_perc = models.TextField(default=0, editable=False)
    pf = models.PositiveIntegerField(default=0, editable=False)

    def team_game_leader(self, stat):
        """
        Returns the player (and value) with team high value of given statistic in a game.
        If there's more then one player, it returns the number of players (and value).
        """
        player_box = PlayerBoxscore.objects.filter(game=self.game).filter(team=self.team).order_by('-' + stat)[0]
        value = getattr(player_box, stat)
        n = PlayerBoxscore.objects.filter(game=self.game).filter(team=self.team).filter(**{stat: value}).count()

        if n > 1:
            return str(n) + ' players', value
        elif n == 1:
            return player_box.player, value

    def team_players_boxscores(self, stat_fields):
        """
        Creates a list of players game boxscores with statistic fields from `stat_fields` list.

        The list has a format: [Player number, Player name, STAT0, STAT1, ...]
        Players are ordered by starter status and then by minutes played.
        Example:
            stats = ['min', 'pts', 'fgm', 'fga', 'fg_perc', 'three_pm', 'three_pa', 'three_perc',
                     'ftm', 'fta', 'ft_perc', 'reb_off', 'reb_def', 'reb_all', 'ast', 'stl', 'blk']
            players_boxscores[0] = [Michael Jordan, 29, 34, 11, 24, 0.460, 4, 13, 0.310, 8, 9, 0.890, 5, 3, 8, 5, 0, 5]
        """
        players_boxscores = list()
        for player_box in PlayerBoxscore.objects.filter(game=self.game).filter(team=self.team).order_by('-is_starter',
                                                                                                        '-min'):
            box = [player_box.player.number,
                   '<a href="' + player_box.player.get_absolute_url() + '">' + player_box.player.full_name + '<a/>']

            for item in stat_fields:
                box.append(getattr(player_box, item))

            players_boxscores.append(box)

        return players_boxscores

    def team_boxscore(self, stat_fields):
        """
        Creates a list of team sum of statistic fields from `stat_fields` list

        The list has a format: [Number of player that played, `MIN`, STAT0, STAT1, ...]
        Example:
            stats = ['min', 'pts', 'fgm', 'fga', 'fg_perc', 'three_pm', 'three_pa', 'three_perc',
                     'ftm', 'fta', 'ft_perc', 'reb_off', 'reb_def', 'reb_all', 'ast', 'stl', 'blk', 'ba', 'to', 'pf']
            [10 players, 240, 198, 70, 181, 0.387, 28, 75, 0.373, 30, 50, 0.600, 25, 63, 88, 57, 18, 32, 24, 42, 27]
        """
        n = PlayerBoxscore.objects.filter(game=self.game).filter(team=self.team).filter(min__gt=0).count()
        team_box = [str(n) + ' players', '240']

        for item in stat_fields[1:]:
                team_box.append(getattr(self, item))

        return team_box

    def __str__(self):
        """Example: Chicago Bulls (CHI at NYK, 01.01.2000)"""
        return str(self.team.full_name) + ' (' + str(self.game.away_team.short_name) + ' at ' + str(
            self.game.home_team.short_name) + ', ' + self.game.date.strftime("%d.%m.%Y") + ')'

    def save(self, *args, **kwargs):
        # Aggregate returns dict
        self.pts = self.ftm + (self.fgm - self.three_pm) * 2 + self.three_pm * 3
        self.reb_def = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('reb_def'))['reb_def__sum']
        self.reb_off = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('reb_off'))['reb_off__sum']
        self.reb_all = self.rebounds_def + self.rebounds_off
        self.ast = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('ast'))['ast__sum']
        self.stl = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('stl'))['stl__sum']
        self.blk = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('blk'))['blk__sum']
        self.ba = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('ba'))['ba__sum']
        self.fgm = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('fgm'))['fgm__sum']
        self.fga = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('fga'))['fga__sum']
        self.fg_perc = '{0:.3f}'.format(self.fgm / self.fga) if self.fga > 0 else '-'
        self.three_pm = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('three_pm'))['three_pm__sum']
        self.three_pa = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('three_pa'))['three_pa__sum']
        self.three_perc = '{0:.3f}'.format(self.three_pm / self.three_pa) if self.three_pa > 0 else '-'
        self.ftm = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('ftm'))['ftm__sum']
        self.fta = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('fta'))['fta__sum']
        self.ft_perc = '{0:.3f}'.format(self.ftm / self.fta) if self.fta > 0 else '-'
        self.pf = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('pf'))['pf__sum']

        super(TeamBoxscore, self).save(*args, **kwargs)


class PeriodScore(models.Model):
    game = models.ForeignKey(Game)
    quarter = models.PositiveIntegerField()
    home_team_points = models.PositiveIntegerField()
    away_team_points = models.PositiveIntegerField()

    def __str__(self):
        """Example: CHI: 40 | NYK: 10 (1Q)"""
        return str(self.game.home_team.short_name) + ': ' + str(self.home_team_points) + ' | ' + str(
            self.game.away_team.short_name) + ': ' + str(self.away_team_points) + ' (' + str(self.quarter) + 'Q)'