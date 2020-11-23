# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nick', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('publication_date', models.DateTimeField(auto_now_add=True)),
                ('ip', models.CharField(max_length=25)),
                ('ua', models.CharField(max_length=512)),
                ('reply', models.ForeignKey(blank=True, to='forum.Comment', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DayStat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.IntegerField(default=0)),
                ('count', models.IntegerField(default=0)),
                ('uniq', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=200)),
                ('messages', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForumDayStat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.IntegerField(default=0)),
                ('count', models.IntegerField(default=0)),
                ('uniq', models.IntegerField(default=0)),
                ('forum', models.ForeignKey(to='forum.Forum')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForumMonthStat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('month', models.IntegerField(default=0)),
                ('count', models.IntegerField(default=0)),
                ('uniq', models.IntegerField(default=0)),
                ('forum', models.ForeignKey(to='forum.Forum')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForumYearStat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField(default=0)),
                ('count', models.IntegerField(default=0)),
                ('uniq', models.IntegerField(default=0)),
                ('forum', models.ForeignKey(to='forum.Forum')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_url', models.CharField(unique=True, max_length=512)),
                ('image', models.ImageField(null=True, upload_to=b'media/images/%Y-%m/', blank=True)),
                ('is_exists', models.BooleanField(default=True)),
                ('last_check', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LongMessages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(unique=True, max_length=500)),
                ('length', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LSMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avglen', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_op', models.BooleanField(default=False)),
                ('message_id', models.IntegerField(null=True, blank=True)),
                ('lor_message_id', models.IntegerField()),
                ('reply_to', models.IntegerField(default=0)),
                ('publication_date', models.DateTimeField(null=True, blank=True)),
                ('year', models.SmallIntegerField(default=0)),
                ('month', models.SmallIntegerField(default=0)),
                ('forum', models.ForeignKey(to='forum.Forum')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MessageStore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('is_processed', models.BooleanField(default=False)),
                ('image_ex', models.BooleanField(default=False)),
                ('ms', models.ForeignKey(to='forum.Message')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MonthStat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('month', models.IntegerField(default=0)),
                ('count', models.IntegerField(default=0)),
                ('uniq', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParsedUrls',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(unique=True, max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('url', models.CharField(unique=True, max_length=500)),
                ('thread_url', models.CharField(max_length=500)),
                ('lor_id', models.IntegerField()),
                ('publication_date', models.DateTimeField()),
                ('year', models.SmallIntegerField(default=0)),
                ('month', models.SmallIntegerField(default=0)),
                ('forum', models.ForeignKey(to='forum.Forum')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=150)),
                ('user_id', models.IntegerField(default=0)),
                ('last_visit', models.DateTimeField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=False)),
                ('about', models.TextField(null=True, blank=True)),
                ('total_msg', models.IntegerField(default=0)),
                ('themes', models.IntegerField(default=0)),
                ('user_place', models.IntegerField(default=0)),
                ('trollolo', models.FloatField(default=0)),
                ('trollolo_place', models.IntegerField(default=0)),
                ('notalks', models.IntegerField(default=0)),
                ('is_updated', models.BooleanField(default=False)),
                ('avatar', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserWord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField(default=1)),
                ('user', models.ForeignKey(to='forum.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=100)),
                ('user', models.ForeignKey(to='forum.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('count', models.IntegerField(default=1)),
                ('is_usable', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='YearStat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField(default=0)),
                ('count', models.IntegerField(default=0)),
                ('uniq', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='userword',
            name='word',
            field=models.ForeignKey(to='forum.Word'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='thread',
            name='user',
            field=models.ForeignKey(to='forum.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monthstat',
            name='year',
            field=models.ForeignKey(to='forum.YearStat'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='thread',
            field=models.ForeignKey(editable=False, to='forum.Thread'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(editable=False, to='forum.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lsmessage',
            name='user',
            field=models.ForeignKey(to='forum.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forummonthstat',
            name='year',
            field=models.ForeignKey(to='forum.ForumYearStat'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forumdaystat',
            name='month',
            field=models.ForeignKey(to='forum.ForumMonthStat'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='daystat',
            name='month',
            field=models.ForeignKey(to='forum.MonthStat'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='userprofile',
            field=models.ForeignKey(to='forum.UserProfile'),
            preserve_default=True,
        ),
    ]
