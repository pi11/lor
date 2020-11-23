# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_auto_20150527_1738'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='fav_tags',
            field=models.ManyToManyField(to='forum.Tag'),
        ),
    ]
