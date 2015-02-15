from django.db import models
from django.core.exceptions import ValidationError
from django.utils.datetime_safe import date
from django.db.models import Q

from Teams.models import Team


class Player(models.Model):
    position_choices = (
        ('PG', 'Point Guard'),
        ('PG/SG', 'Point Guard/Shooting Guard'),
        ('SG', 'Shooting Guard'),
        ('SG/SF', 'Shooting Guard/Small Forward'),
        ('SF', 'Small Forward'),
        ('SF/PF', 'Small Forward/Power Forward'),
        ('PF', 'Power Forward'),
        ('PF/C', 'Power Forward/Center'),
        ('C', 'Center'),
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    team = models.ForeignKey(Team)
    is_captain = models.BooleanField(default=False)
    position = models.CharField(max_length=5, choices=position_choices)
    birth_date = models.DateField()
    height = models.PositiveIntegerField(verbose_name='Height [cm]')
    weight = models.PositiveIntegerField(verbose_name='Weight [kg]')
    number = models.PositiveIntegerField()
    image = models.ImageField(verbose_name='Player photo', default='player_photos/default.jpg',
                              upload_to='player_photos')

    def age(self):
        born = self.birth_date
        today = date.today()
        try:
            birthday = born.replace(year=today.year)
        except ValueError:  # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year, month=born.month + 1, day=1)
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse

        return reverse('player_page', args=[str(self.first_name) + '_' + str(self.last_name)])

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def clean(self):
        try:
            Player.objects.get(Q(team=self.team), Q(is_captain=True))
            raise ValidationError('The team already has a captain.')
        except Player.DoesNotExist:
            pass