from django.db import models
from django.db.models import Q, Sum
from django.utils.functional import cached_property
from collections import OrderedDict

from Players.models import Player
from Teams.models import Team


class Game(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_team')
    away_team = models.ForeignKey(Team, related_name='away_team')
    date = models.DateField()

    @cached_property
    def winner(self):
        home_team_box = TeamBoxscore.objects.get(Q(game=self), Q(team=self.home_team))
        away_team_box = TeamBoxscore.objects.get(Q(game=self), Q(team=self.away_team))
        if home_team_box.pts > away_team_box.pts:
            return home_team_box.team
        else:
            return away_team_box.team

    @cached_property
    def overtime(self):
        return PeriodScore.objects.filter(game=self).count - 4

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
        return str(self.player) + ' (' + str(self.game.away_team) + ' @ ' + str(
            self.game.home_team) + ', ' + self.game.date.strftime("%d.%m.%Y") + ')'

    def save(self, *args, **kwargs):
        self.pts = self.ftm + (self.fgm - self.three_pm) * 2 + self.three_pm * 3
        self.reb_all = self.rebounds_def + self.rebounds_off
        self.fg_perc = "{0:.2f}".format(self.fgm / self.fga) * 100 if self.fga > 0 else "-"
        self.three_perc = "{0:.2f}".format(self.three_pm / self.three_pa) * 100 if self.three_pa > 0 else "-"
        self.ft_perc = "{0:.2f}".format(self.ftm / self.fta) * 100 if self.fta > 0 else "-"
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

    @cached_property
    def team_game_leaders(self):
        # TODO: Wszystko w jedną pętle?
        """
        Creates an OrderedDict of team leaders in statistics (PTS, REB, AST, STL, BLK) of given game (TeamBoxscore).

        Dict consists of lists, where the key is the short name of the statistic.
        The list has a format: [String shown on the page, link address, statistic value]
        When there's one leader, the link points to the player page, otherwise to "#".
        """
        leaders = OrderedDict()
        # PTS
        box = PlayerBoxscore.objects.filter(game=self.game).filter(team=self.team).order_by('-pts')[0]
        n = PlayerBoxscore.objects.filter(game=self.game).filter(team=self.team).filter(pts=box.pts).count()
        if n > 1:
            leaders['PTS'] = [str(n) + ' players', '#', box.pts]
        elif n == 1:
            leaders['PTS'] = [box.player.full_name, box.player.get_absolute_url(), box.pts]
        # REB
        box = PlayerBoxscore.objects.filter(game=self.game).filter(team=self.team).order_by('-reb_all')[0]
        n = PlayerBoxscore.objects.filter(game=self.game).filter(team=self.team).filter(reb_all=box.reb_all).count()
        if n > 1:
            leaders['REB'] = [str(n) + ' players', '#', box.reb_all]
        elif n == 1:
            leaders['REB'] = [box.player.full_name, box.player.get_absolute_url(), box.reb_all]
        # AST
        box = PlayerBoxscore.objects.filter(game=self.game).filter(team=self.team).order_by('-ast')[0]
        n = PlayerBoxscore.objects.filter(game=self.game).filter(team=self.team).filter(ast=box.ast).count()
        if n > 1:
            leaders['AST'] = [str(n) + ' players', '#', box.ast]
        elif n == 1:
            leaders['AST'] = [box.player.full_name, box.player.get_absolute_url(), box.ast]
        # STL
        box = PlayerBoxscore.objects.filter(game=self.game).filter(team=self.team).order_by('-stl')[0]
        n = PlayerBoxscore.objects.filter(game=self.game).filter(team=self.team).filter(stl=box.stl).count()
        if n > 1:
            leaders['STL'] = [str(n) + ' players', '#', box.stl]
        elif n == 1:
            leaders['STL'] = [box.player.full_name, box.player.get_absolute_url(), box.stl]
        # BLK
        box = PlayerBoxscore.objects.filter(game=self.game).filter(team=self.team).order_by('-blk')[0]
        n = PlayerBoxscore.objects.filter(game=self.game).filter(team=self.team).filter(blk=box.blk).count()
        if n > 1:
            leaders['BLK'] = [str(n) + ' players', '#', box.blk]
        elif n == 1:
            leaders['BLK'] = [box.player.full_name, box.player.get_absolute_url(), box.blk]

        return leaders

    @cached_property
    def team_players_boxscores(self):
        """
        Creates a list of players boxscores in given game (TeamBoxscore).

        The list has a format: [Number, Name, MIN, PTS, FGM-FGA, FG%, 3PM-3PA, 3P%, FTM-FTA, FT%, ORB, DRG, TRB,
                                AST, STL, BLK, BA, TO, PF]
        Players are ordered by starter status and then by minutes played.
        """
        players_boxscores = list()
        for player_box in PlayerBoxscore.objects.filter(game=self.game).filter(team=self.team).order_by('-is_starter', '-min'):
            players_boxscores.append([player_box.player.number, '<a href="' + player_box.player.get_absolute_url() + '">' +
                                      player_box.player.full_name + '<a/>', player_box.min, player_box.pts,
                                      str(player_box.fgm) + '-' + str(player_box.fga), player_box.fg_perc,
                                      str(player_box.three_pm) + '-' + str(player_box.three_pa), player_box.three_perc,
                                      str(player_box.ftm) + '-' + str(player_box.fta), player_box.ft_perc,
                                      player_box.reb_off, player_box.reb_def, player_box.reb_all, player_box.ast,
                                      player_box.stl, player_box.blk, player_box.ba, player_box.to, player_box.pf])

        return players_boxscores

    @cached_property
    def team_boxscore(self):
        """
        Creates a list of team_boxscore in given game (TeamBoxscore).

        The list has a format: [Number of player that played, MIN, PTS, FGM-FGA, FG%, 3PM-3PA, 3P%, FTM-FTA, FT%,
                                ORB, DRG, TRB, AST, STL, BLK, BA, TO, PF]
        """
        n = PlayerBoxscore.objects.filter(game=self.game).filter(team=self.team).filter(min__gt=0).count()
        team_boxscore = [str(n) + ' players', '240', self.pts,
                         str(self.fgm) + '-' + str(self.fga), self.fg_perc,
                         str(self.three_pm) + '-' + str(self.three_pa), self.three_perc,
                         str(self.ftm) + '-' + str(self.fta), self.ft_perc,
                         self.reb_off, self.reb_def, self.reb_all, self.ast,
                         self.stl, self.blk, self.ba, self.to, self.pf]

        return team_boxscore

    def __str__(self):
        return str(self.team) + ' (' + str(self.game.away_team) + ' @ ' + str(
            self.game.home_team) + ', ' + self.game.date.strftime("%d.%m.%Y") + ')'

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
        self.fg_perc = "{0:.2f}".format(self.fgm / self.fga) * 100 if self.fga > 0 else "-"
        self.three_pm = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('three_pm'))['three_pm__sum']
        self.three_pa = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('three_pa'))['three_pa__sum']
        self.three_perc = "{0:.2f}".format(self.three_pm / self.three_pa) * 100 if self.three_pa > 0 else "-"
        self.ftm = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('ftm'))['ftm__sum']
        self.fta = PlayerBoxscore.objects.filter(team_boxscore=self).aggregate(Sum('fta'))['fta__sum']
        self.ft_perc = "{0:.2f}".format(self.ftm / self.fta) * 100 if self.fta > 0 else "-"
        self.pf = PlayerBoxscore.objects.filter(team_boxscore=sel).aggregate(Sum('pf'))['pf__sum']

        super(TeamBoxscore, self).save(*args, **kwargs)


class PeriodScore(models.Model):
    game = models.ForeignKey(Game)
    quarter = models.PositiveIntegerField()
    home_team_points = models.PositiveIntegerField()
    away_team_points = models.PositiveIntegerField()

    def __str__(self):
        return str(self.game.home_team) + " : " + str(self.home_team_points) + " | " + str(
            self.game.away_team) + " : " + str(self.away_team_points)