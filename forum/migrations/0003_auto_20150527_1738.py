# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20150330_1316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='fav_tags',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
