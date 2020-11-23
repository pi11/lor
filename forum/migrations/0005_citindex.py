# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20150527_1741'),
    ]

    operations = [
        migrations.CreateModel(
            name='CitIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField(default=0)),
                ('user', models.OneToOneField(to='forum.UserProfile')),
            ],
        ),
    ]
