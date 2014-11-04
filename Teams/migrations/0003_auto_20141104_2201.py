# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Teams', '0002_auto_20141102_1732'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='color',
        ),
        migrations.AddField(
            model_name='team',
            name='photo',
            field=models.ImageField(upload_to='team_logos', default='team_logos/default.png'),
            preserve_default=True,
        ),
    ]
