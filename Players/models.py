from django.db import models
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
    position = models.CharField(max_length=5, choices=position_choices)
    birth_date = models.DateField()
    height = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    number = models.PositiveIntegerField()
    image = models.ImageField(default="player_photos/default.jpg", upload_to="player_photos")

    def __str__(self):
        return self.first_name + ' ' + self.last_name