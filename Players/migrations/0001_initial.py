# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('birth_date', models.DateField()),
                ('number', models.PositiveIntegerField()),
                ('height', models.PositiveIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=32)),
                ('short_name', models.CharField(max_length=5)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='player',
            name='position',
            field=models.ForeignKey(to='Players.Position'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(to='Teams.Team'),
            preserve_default=True,
        ),
    ]
