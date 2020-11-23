# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_citindex'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagestore',
            name='have_href',
            field=models.BooleanField(default=False),
        ),
    ]
