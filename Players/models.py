from django.db import models
from Teams.models import Team


class Position(models.Model):
    full_name = models.CharField(max_length=32)
    short_name = models.CharField(max_length=5)

    def __str__(self):
        return self.short_name


class Player(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    team = models.ForeignKey(Team)
    birth_date = models.DateField()
    number = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    position = models.ForeignKey(Position)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
