from django.db import models


class Team(models.Model):
    full_name = models.CharField(max_length=64)
    short_name = models.CharField(max_length=5)
    logo = models.ImageField(default="team_logos/default.png", upload_to="team_logos")

    def __str__(self):
        return self.full_name