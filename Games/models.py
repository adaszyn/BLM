from django.db import models
from django.db.models import Q, Sum
from django.utils.functional import cached_property
from django.core.exceptions import ValidationError
from datetime import date
from collections import OrderedDict

from Players.models import Player
from Teams.models import Team


class Game(models.Model):
    away_team = models.ForeignKey(Team, related_name='away_team')
    home_team = models.ForeignKey(Team, related_name='home_team')
    date = models.DateField()

    class Meta:
        ordering = ['date']
        unique_together = ('away_team', 'home_team', 'date',)

    def happened(self):
        """Returns True if the game happened"""
        s = self.final_score
        return True if self.date <= date.today() and (s['away_team'] != 0 or s['home_team'] != 0) else False
    happened.boolean = True

    @cached_property
    def final_score(self):
        """Returns a dict with teams final score"""
        final_score = {'home_team': TeamBoxscore.objects.get(Q(game=self), Q(team=self.home_team)).pts,
                       'away_team': TeamBoxscore.objects.get(Q(game=self), Q(team=self.away_team)).pts}
        return final_score

    @cached_property
    def winner(self):
        """Returns the team that won; None if game hadn't happened yet"""
        if self.happened():
            return self.home_team if self.final_score['home_team'] > self.final_score['away_team'] else self.away_team
        else:
            return None

    @cached_property
    def overtime(self):
        """Returns number of overtimes, 0 if none and None if game hadn't happened yet."""
        return PeriodScore.objects.filter(game=self).count() - 4 if self.happened() else None

    @cached_property
    def short_name(self):
        """Example: CHI at NYK (01.01.2000)"""
        return '{away_team} at {home_team} ({date})'.format(away_team=self.away_team.short_name,
                                                            home_team=self.home_team.short_name,
                                                            date=self.date.strftime("%d.%m.%Y"))

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse

        return reverse('game_page',
                       args=[self.date.strftime("%Y-%m-%d"), self.away_team.short_name, self.home_team.short_name])

    def __str__(self):
        """Example: Chicago Bulls at New York Knicks (01.01.2000)"""
        return '{away_team} at {home_team} ({date})'.format(away_team=self.away_team.full_name,
                                                            home_team=self.home_team.full_name,
                                                            date=self.date.strftime("%d.%m.%Y"))

    def clean(self):
        if self.away_team == self.home_team:
            raise ValidationError("Team can't play itself.")

        if TeamBoxscore.objects.filter(game=self).count() not in [0, 2]:
            raise ValidationError("Game has wrong number of TeamBoxscores.")


class PlayerBoxscore(models.Model):
    player = models.ForeignKey(Player)
    team = models.ForeignKey(Team)  # Should be deleted
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

    class Meta:
        unique_together = ('player', 'game',)

    def __str__(self):
        """Example: Michael Jordan (CHI at NYK, 01.01.2000)"""
        return '{player} ({game})'.format(player=self.player.full_name, game=self.game.short_name)

    def clean(self):
        if self.min == 0:
            raise ValidationError({'min': "Player who played in the game can't have 0 minutes."})

        # TODO: Zmienna minut w kwarcie
        if self.min > 48:
            raise ValidationError({'min': "Player can't play more than 48 minutes"})

        if any([self.fgm > self.fga, self.three_pm > self.three_pa, self.ftm > self.fta]):
            raise ValidationError({'player': "Player can't hit more shots then attempted."})

        if self.three_pa > self.fga:
            raise ValidationError({'three_pa': "Player can't attempt more threes then field goals."})

    def save(self, *args, **kwargs):
        self.pts = self.ftm + (self.fgm - self.three_pm) * 2 + self.three_pm * 3
        self.reb_all = self.reb_def + self.reb_off
        self.fg_perc = '{0:.3f}'.format(self.fgm / self.fga) if self.fga > 0 else '-'
        self.three_perc = '{0:.3f}'.format(self.three_pm / self.three_pa) if self.three_pa > 0 else '-'
        self.ft_perc = '{0:.3f}'.format(self.ftm / self.fta) if self.fta > 0 else '-'

        super(PlayerBoxscore, self).save(*args, **kwargs)


class TeamBoxscore(models.Model):
    team = models.ForeignKey(Team)
    game = models.ForeignKey(Game)
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

    class Meta:
        unique_together = ('team', 'game',)

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
        Creates an OrderedDict of players game boxscores with statistic fields from `stat_fields` list as value,
        and Player as a key.

        The dict has a format: dict[Player] = [STAT0, STAT1, ...]
        Players are ordered by starter status and then by minutes played.
        Example:
            stats = ['min', 'pts', 'fgm', 'fga', 'fg_perc', 'three_pm', 'three_pa', 'three_perc',
                     'ftm', 'fta', 'ft_perc', 'reb_off', 'reb_def', 'reb_all', 'ast', 'stl', 'blk']
            players_boxscores[Michael Jordan] = [29, 34, 11, 24, 0.460, 4, 13, 0.310, 8, 9, 0.890, 5, 3, 8, 5, 0, 5]
        """
        players_boxscores = OrderedDict()
        for player_box in PlayerBoxscore.objects.filter(game=self.game).filter(team=self.team).order_by('-is_starter',
                                                                                                        '-min'):
            player = player_box.player
            players_boxscores[player] = list()

            for item in stat_fields:
                players_boxscores[player].append(getattr(player_box, item))

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
        # TODO: Zmienna minut w kwarcie
        team_box = [str(n) + ' players', '240']

        for item in stat_fields[1:]:
                team_box.append(getattr(self, item))

        return team_box

    def __str__(self):
        """Example: Chicago Bulls (CHI at NYK, 01.01.2000)"""
        return '{team} ({away_team} at {home_team}, {date})'.format(team=self.team.full_name,
                                                                    away_team=self.game.away_team.short_name,
                                                                    home_team=self.game.home_team.short_name,
                                                                    date=self.game.date.strftime("%d.%m.%Y"))

    def save(self, *args, **kwargs):
        super(TeamBoxscore, self).save(*args, **kwargs)

        s = PlayerBoxscore.objects.filter(game=self.game).filter(team=self.team).aggregate(
            reb_def=Sum('reb_def'), reb_off=Sum('reb_off'), ast=Sum('ast'), stl=Sum('stl'), blk=Sum('blk'),
            ba=Sum('ba'), fgm=Sum('fgm'), fga=Sum('fga'), three_pm=Sum('three_pm'), three_pa=Sum('three_pa'),
            ftm=Sum('ftm'), fta=Sum('fta'), pf=Sum('pf'))

        self.reb_def = s['reb_def']
        self.reb_off = s['reb_off']
        self.ast = s['ast']
        self.stl = s['stl']
        self.blk = s['blk']
        self.ba = s['ba']
        self.fgm = s['fgm']
        self.fga = s['fga']
        self.three_pm = s['three_pm']
        self.three_pa = s['three_pa']
        self.ftm = s['ftm']
        self.fta = s['fta']
        self.pf = s['pf']

        self.pts = self.ftm + (self.fgm - self.three_pm) * 2 + self.three_pm * 3
        self.reb_all = self.reb_def + self.reb_off
        self.fg_perc = '{0:.3f}'.format(self.fgm / self.fga) if self.fga > 0 else '-'
        self.three_perc = '{0:.3f}'.format(self.three_pm / self.three_pa) if self.three_pa > 0 else '-'
        self.ft_perc = '{0:.3f}'.format(self.ftm / self.fta) if self.fta > 0 else '-'

        super(TeamBoxscore, self).save(*args, **kwargs)


class PeriodScore(models.Model):
    game = models.ForeignKey(Game)
    quarter = models.PositiveIntegerField()
    away_team = models.PositiveIntegerField(default=0)
    home_team = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['game', 'quarter']
        unique_together = ('game', 'quarter',)

    def __str__(self):
        """Example: CHI: 40 | NYK: 10 (1Q)"""
        return ('{away_team}: {away_points} | '
                '{home_team}: {home_points} ({q}Q)').format(away_team=self.game.away_team.short_name,
                                                            away_points=self.away_team,
                                                            home_team=self.game.home_team.short_name,
                                                            home_points=self.home_team,
                                                            q=self.quarter)