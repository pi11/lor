#-*- coding: utf-8 -*-

from forum.models import *

from django.db import connection, transaction
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    """This command send alert messages to users    """
    help = """This command send alert messages to users"""

    def handle(self, *args, **options):

        forum = Forum.objects.get(name=u'Новости')
        q = """select user_id, count(*) from forum_message
               where forum_id = %s and is_op=True group by user_id
               """ % (forum.pk)
        cursor = connection.cursor()
        cursor.execute(q)
        res = cursor.fetchall()
        for r in res:
            user = UserProfile.objects.get(pk=r[0])
            user.news_count = r[1]
            user.save()


        print ("News makers updated")
        cursor = connection.cursor()
        """
        print "Updating Citation Index:"
        tot = UserProfile.objects.filter(total_msg__gt=0).count()
        for u in UserProfile.objects.filter(total_msg__gt=0).order_by("-total_msg"):
            tot -= 1
            c = MessageStore.objects.filter(
                text__contains=" %s " % u.username).count()
            ci, cr = CitIndex.objects.get_or_create(user=u)
            c_count = c - u.total_msg
            ci.count = c_count
            ci.save()
            # if c > 0:
            print "User %s have %s CI. Users left: %s" % (u, c_count, tot)
        """
        print "Update messages per year"
        q = (
            "select forum_id, date_part('year', publication_date at time zone 'Europe/Moscow'), count(*) from forum_message where publication_date is not null group by forum_id, date_part('year', publication_date at time zone 'Europe/Moscow')  order by 1;")
        cursor = connection.cursor()
        cursor.execute(q)
        res = cursor.fetchall()
        for r in res:
            forum = Forum.objects.get(pk=r[0])
            ys, c = ForumYearStat.objects.get_or_create(forum=forum, year=r[1])
            if ys.count != r[2]:
                ys.count = r[2]
                ys.save(update_fields=['count', ])

        print "Update messages per month"

        # Update months stats
        for y in ForumYearStat.objects.all():
            continue
            q = ("select forum_id, date_part('month', publication_date at time zone 'Europe/Moscow'), count(*) from forum_message where date_part('year', publication_date at time zone 'Europe/Moscow') = %s and forum_id=%s group by forum_id, date_part('month', publication_date at time zone 'Europe/Moscow') order by 1;" %
                 (y.year, y.forum.pk))
            # print q
            cursor = connection.cursor()
            cursor.execute(q)
            res = cursor.fetchall()
            for r in res:
                forum = Forum.objects.get(pk=r[0])
                print "Months, Forum: %s, y.forum: %s" % (forum, y.forum)
                ms, c = ForumMonthStat.objects.get_or_create(
                    forum=forum, year=y, month=r[1])

                q2 = ("""select count(distinct(user_id)) from forum_message
                         where date_part('year', publication_date at time zone 'Europe/Moscow') = %s
                         and date_part('month', publication_date at time zone 'Europe/Moscow') = %s
                         and forum_id=%s;
                         """ % (ms.year.year, ms.month, ms.forum.pk))
                cursor2 = connection.cursor()
                cursor2.execute(q2)
                r2 = cursor2.fetchone()
                upd = False
                if ms.uniq != r2[0]:
                    ms.uniq = r2[0]
                    upd = True
                if ms.count != r[2]:
                    ms.count = r[2]
                    upd = True

                if upd:
                    ms.save(update_fields=['count', 'uniq'])

        # Update days stats
        print "Update messages per day"

        for m in ForumMonthStat.objects.all():

            q = ("""select date_part('day', publication_date at time zone 'Europe/Moscow'), count(*), forum_id from forum_message
                     where date_part('year', publication_date at time zone 'Europe/Moscow') = %s
                     and   date_part('month', publication_date at time zone 'Europe/Moscow') = %s
                     and forum_id=%s
                     group by forum_id, date_part('day', publication_date at time zone 'Europe/Moscow')
                     order by 1;""" % (m.year.year, m.month, m.forum.pk))
            # print q
            cursor = connection.cursor()
            cursor.execute(q)
            res = cursor.fetchall()
            for r in res:
                forum = Forum.objects.get(pk=r[2])
                ds, c = ForumDayStat.objects.get_or_create(
                    month=m, day=r[0], forum=forum)
                print "New day: year:%s month:%s forum_y:%s forum_m:%s, forum_d%s" % (m.year.year, m.month, m.year.forum.name,
                                                                                      m.forum.name, forum.name)

                q2 = ("""select count(distinct(user_id)) from forum_message
                         where date_part('year', publication_date at time zone 'Europe/Moscow') = %s
                         and date_part('month', publication_date at time zone 'Europe/Moscow') = %s
                         and date_part('day', publication_date at time zone 'Europe/Moscow') = %s
                         and forum_id=%s;""" % (m.year.year, m.month, r[0], forum.pk))
                cursor2 = connection.cursor()
                cursor2.execute(q2)
                r2 = cursor2.fetchone()
                # print "Year:%s, month: %s, day:%s, count: %s" % (m.year.year,
                # m.month, r[0], r2[0])
                upd = False
                if ds.uniq != r2[0]:
                    ds.uniq = r2[0]
                    upd = True
                if ds.count != r[1]:
                    ds.count = r[1]
                    upd = True
                if upd:
                    ds.save(update_fields=['count', 'uniq', ])
