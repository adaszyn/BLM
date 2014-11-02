from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=64)
    color = models.CharField(max_length=32)

    def __str__(self):
        return self.name
