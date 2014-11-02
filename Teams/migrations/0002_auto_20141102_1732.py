# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Teams', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='name',
            new_name='full_name',
        ),
        migrations.AddField(
            model_name='team',
            name='short_name',
            field=models.CharField(default='AAA', max_length=5),
            preserve_default=False,
        ),
    ]
