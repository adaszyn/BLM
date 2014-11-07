from django.db import models


class Team(models.Model):
    full_name = models.CharField(max_length=64)
    short_name = models.CharField(max_length=5)
    logo = models.ImageField(default="team_logos/default.png", upload_to="team_logos")
    description = models.CharField(max_length=1024, blank=True, default="")

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('team_page', args=[str(self.full_name.replace(' ', '_'))])

    def __str__(self):
        return self.full_name