from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property


class Team(models.Model):
    full_name = models.CharField(max_length=64)
    short_name = models.CharField(max_length=5)
    logo = models.ImageField(default='team_logos/default.png', upload_to='team_logos')
    description = models.TextField(max_length=1024, blank=True, default='')

    @cached_property
    def count_players(self):
        from Players.models import Player

        return Player.objects.filter(team=self).count()

    @cached_property
    def captain(self):
        from Players.models import Player

        return Player.objects.get(Q(team=self), Q(is_captain=True))

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse

        return reverse('team_page', args=[str(self.full_name.replace(' ', '_'))])

    def __str__(self):
        return self.full_name