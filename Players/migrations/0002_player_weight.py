# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Players', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='weight',
            field=models.PositiveIntegerField(default=100),
            preserve_default=False,
        ),
    ]
