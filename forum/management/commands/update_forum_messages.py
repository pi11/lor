#-*- coding: utf-8 -*-

from forum.models import MonthStat, YearStat, DayStat
from django.db import connection, transaction
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    """This command send alert messages to users    """
    help = """This command send alert messages to users"""
 
    def handle(self, *args, **options):
        print "Update messages per forum"
        q = ("update forum_forum a set messages = (select count(*) "
             "from forum_message b where a.id=b.forum_id group by forum_id);")
        cursor = connection.cursor()
        #cursor.execute(q)
        #transaction.commit_unless_managed()


        print "Update messages per year"
        q = ("select date_part('year', publication_date at time zone 'Europe/Moscow'), count(*) from forum_message where publication_date is not null group by date_part('year', publication_date at time zone 'Europe/Moscow')  order by 1;")
        cursor = connection.cursor()
        cursor.execute(q)
        res = cursor.fetchall()
        for r in res:
            ys, c = YearStat.objects.get_or_create(year=r[0])
            if ys.count != r[1]:
                ys.count = r[1]
                ys.save(update_fields=['count',])
            

        print "Update messages per year"
        q = ("select date_part('year', publication_date at time zone 'Europe/Moscow'), count(*) from forum_message where publication_date is not null group by date_part('year', publication_date at time zone 'Europe/Moscow') order by 1;")
        cursor = connection.cursor()
        cursor.execute(q)
        res = cursor.fetchall()
        for r in res:
            ys, c = YearStat.objects.get_or_create(year=r[0])
            if ys.count != r[1]:
                ys.count = r[1]
                ys.save(update_fields=['count',])
            
        print "Update messages per month"


        # Update months stats
        for y in YearStat.objects.all():
            
            q = ("select date_part('month', publication_date at time zone 'Europe/Moscow'), count(*) from forum_message where date_part('year', publication_date at time zone 'Europe/Moscow') = %s group by date_part('month', publication_date at time zone 'Europe/Moscow') order by 1;" % y.year)
            cursor = connection.cursor()
            cursor.execute(q)
            res = cursor.fetchall()
            for r in res:
                ms, c = MonthStat.objects.get_or_create(year=y, month=r[0])

                
                q2 = ("""select count(distinct(user_id)) from forum_message
                         where date_part('year', publication_date at time zone 'Europe/Moscow') = %s
                         and date_part('month', publication_date at time zone 'Europe/Moscow') = %s;
                         """ % (ms.year.year, ms.month))
                cursor2 = connection.cursor()
                cursor2.execute(q2)
                r2 = cursor2.fetchone()
                upd = False

                if ms.uniq !=r2[0]:
                    ms.uniq = r2[0]
                    upd = True
                if ms.count != r[1]:
                    ms.count = r[1]
                    upd = True

                if upd:
                    ms.save(update_fields=['count', 'uniq'])

        # Update days stats
        print "Update messages per day"
        
        for m in MonthStat.objects.all():
            
            q = ("""select date_part('day', publication_date at time zone 'Europe/Moscow'), count(*) from forum_message
                     where date_part('year', publication_date at time zone 'Europe/Moscow') = %s
                     and   date_part('month', publication_date at time zone 'Europe/Moscow') = %s
                     group by date_part('day', publication_date at time zone 'Europe/Moscow') order by 1;""" % (m.year.year, m.month))
            cursor = connection.cursor()
            cursor.execute(q)
            res = cursor.fetchall()
            for r in res:
                ds, c = DayStat.objects.get_or_create(month=m, day=r[0])

                q2 = ("""select count(distinct(user_id)) from forum_message
                         where date_part('year', publication_date at time zone 'Europe/Moscow') = %s
                         and date_part('month', publication_date at time zone 'Europe/Moscow') = %s
                         and date_part('day', publication_date at time zone 'Europe/Moscow') = %s;""" % (m.year.year, m.month, r[0]))
                cursor2 = connection.cursor()
                cursor2.execute(q2)
                r2 = cursor2.fetchone()
                print "Year:%s, month: %s, day:%s, count: %s" % (m.year.year, m.month, r[0], r2[0])
                upd = False
                if ds.uniq != r2[0]:
                    ds.uniq = r2[0]
                    upd = True
                if ds.count != r[1]:
                    ds.count = r[1]
                    upd = True
                if upd:
                    ds.save(update_fields=['count', 'uniq',])

            
