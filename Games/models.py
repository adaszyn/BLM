from django.db import models
from Players.models import Player
from Teams.models import Team

class Game(models.Model):
    home_team = models.ForeignKey(Team)
    away_team = models.ForeignKey(Team)
    date = models.DateField()
    overtime = models.PositiveIntegerField()

class GameBoxscore(models.Model):
    game = models.ForeignKey(Game)
    team_id = models.ForeignKey(Team)
    result = models.BooleanField()
    points = models.PositiveIntegerField()
    rebounds_def = models.PositiveIntegerField()
    rebounds_off = models.PositiveIntegerField()
    assists = models.PositiveIntegerField()
    steals = models.PositiveIntegerField()
    blocks = models.PositiveIntegerField()
    fgm = models.PositiveIntegerField()
    fga = models.PositiveIntegerField()
    three_pm = models.PositiveIntegerField()
    three_pa = models.PositiveIntegerField()
    ftm = models.PositiveIntegerField()
    fta = models.PositiveIntegerField()

    def rebounds_all(self):
        return self.rebounds_off + self.rebounds_def
    def fg_percentage(self):
        return (100 * self.fgm / self.fga)
    def three_p_percentage(self):
        return (100 * self.three_pa / self.three_pm)
    def ft_percentage(self):
        return (100 * self.fta / self.ftm)

class PlayerBoxscore(models.Model):

    player = models.ForeignKey(Player)
    game = models.ForeignKey(GameBoxscore)
    is_starter = models.BooleanField()
    minutes = models.PositiveIntegerField()
    points = models.PositiveIntegerField()
    rebound_def = models.PositiveIntegerField()
    rebound_off = models.PositiveIntegerField()
    rebound_all = models.PositiveIntegerField()
    assists = models.PositiveIntegerField()
    steals = models.PositiveIntegerField()
    blocks =  models.PositiveIntegerField()
    fgm = models.PositiveIntegerField()
    fga = models.PositiveIntegerField()
    three_pm = models.PositiveIntegerField()
    three_pa = models.PositiveIntegerField()
    ftm = models.PositiveIntegerField()
    fta = models.PositiveIntegerField()
    personal_fouls =models.PositiveIntegerField()

    def fg_percentage(self):
        return (100 * self.fgm / self.fga)
    def three_p_percentage(self):
        return (100 * self.three_pa / self.three_pm)
    def ft_percentage(self):
        return (100 * self.fta / self.ftm)

class PeriodScore(models.Model):
    game = models.ForeignKey(GameBoxscore)
    quarter = models.PositiveIntegerField()
    points = models.PositiveIntegerField()
    def is_additional(self):
        return (self.quarter > 4)