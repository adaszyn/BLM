# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Players', '0002_player_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='image',
            field=models.ImageField(upload_to='player_photos', default='player_photos/default.jpg'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.CharField(max_length=5, choices=[('PG', 'Point Guard'), ('PG/SG', 'Point Guard/Shooting Guard'), ('SG', 'Shooting Guard'), ('SG/SF', 'Shooting Guard/Small Forward'), ('SF', 'Small Forward'), ('SF/PF', 'Small Forward/Power Forward'), ('PF', 'Power Forward'), ('PF/C', 'Power Forward/Center'), ('C', 'Center')]),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='Position',
        ),
    ]
