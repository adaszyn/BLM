from datetime import datetime
from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property
from datetime import datetime


class Team(models.Model):
    full_name = models.CharField(max_length=64)
    short_name = models.CharField(max_length=5)
    logo = models.ImageField(default='team_logos/default.png', upload_to='team_logos')
    description = models.TextField(max_length=1024, blank=True, default='')

    @cached_property
    def count_players(self):
        """Returns the number of players on the team"""
        from Players.models import Player

        return Player.objects.filter(team=self).count()

    @cached_property
    def captain(self):
        """Returns the captain of the team"""
        from Players.models import Player

        return Player.objects.get(Q(team=self), Q(is_captain=True))

    def team_average_leader(self, stat):
        # TODO: Poprawić z sortowaniem po stronie bazy (.extra)
        # https://docs.djangoproject.com/en/dev/ref/models/querysets/#django.db.models.query.QuerySet.extra
        """Returns the player (and value) with best average in given statistic"""
        from Players.models import Player

        top_player = Player.objects.filter(team=self)[0]
        top_value = top_player.cat_average(stat)

        for player in Player.objects.filter(team=self):
            value = player.cat_average(stat)
            if value > top_value:
                top_player = player
                top_value = value

        return top_player, top_value

    def next_games(self, n, converted=False):
        """
        Creates a list of `n` previous (if `n` is negative) or next (if `n` is positive) games of a team. If converted
        is set to `True`, then creates a list of lists for the template.

        List format for previous games: [String shown on the template, Game link, Short date, String CSS class]
        List format for next games: [String shown on the template, Game link, Short date]
        Example:
            ['BOS 169 at OKC 173', '/game/2014-12-25/BOS_at_OKC/', '25 Dec', 'text-danger']
            ['BOS at OKC', '/game/2013-12-25/BOS_at_OKC/', '25 Dec']
        """
        from Games.models import Game
        global games

        today = datetime.today().date()
        games_list = list()

        if n > 0:
            games = Game.objects.filter(Q(home_team=self) | Q(away_team=self)).filter(date__gte=today).order_by('date')[:n]
        elif n < 0:
            games = Game.objects.filter(Q(home_team=self) | Q(away_team=self)).filter(date__lt=today).order_by('-date')[:-n]

        if not converted:
            for game in games:
                games_list.append(game)
        elif converted and n > 0:
            for game in games:
                if game.home_team == self:
                    # Example: [CHI vs NYK]
                    game_item = [game.home_team.short_name + ' vs ' + game.away_team.short_name]
                else:
                    # Example: [CHI at NYK]
                    game_item = [game.away_team.short_name + ' at ' + game.home_team.short_name]
                game_item.extend((game.get_absolute_url(), game.date.strftime("%d %b")))

                games_list.append(game_item)
        elif converted and n < 0:
            for game in games:
                if game.home_team == self:
                    # Example: [CHI 230 vs NYK 169]
                    game_item = [
                        game.home_team.short_name + ' ' + str(game.final_score['home_team']) + ' vs '
                        + game.away_team.short_name + ' ' + str(game.final_score['away_team'])]
                else:
                    # Example: [CHI 230 at NYK 169]
                    game_item = [
                        game.away_team.short_name + ' ' + str(game.final_score['away_team']) + ' at '
                        + game.home_team.short_name + ' ' + str(game.final_score['home_team'])]

                msg = 'text-success' if game.winner == self else 'text-danger'
                game_item.extend((game.get_absolute_url(), game.date.strftime("%d %b"), msg))

                games_list.append(game_item)

        return games_list

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse

        return reverse('team_page', args=[str(self.full_name.replace(' ', '_'))])

    def __str__(self):
        """Example: Chicago Bulls"""
        return self.full_name


class Coach(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    team = models.ForeignKey(Team)

    def __str__(self):
        return self.first_name + " " + self.last_name