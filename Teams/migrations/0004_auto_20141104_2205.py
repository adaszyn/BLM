# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Teams', '0003_auto_20141104_2201'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='photo',
            new_name='logo',
        ),
    ]
