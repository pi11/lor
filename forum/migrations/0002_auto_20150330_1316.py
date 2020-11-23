# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250)),
                ('count', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='fav_tags',
            field=models.ManyToManyField(to='forum.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_stars_grey',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='reg_date',
            field=models.CharField(default=datetime.datetime(2015, 3, 30, 13, 16, 27, 137709), max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='stars_count',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
