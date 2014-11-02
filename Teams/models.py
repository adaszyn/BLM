from django.db import models


class Team(models.Model):
    full_name = models.CharField(max_length=64)
    short_name = models.CharField(max_length=5)
    color = models.CharField(max_length=32)

    def __str__(self):
        return self.full_name
