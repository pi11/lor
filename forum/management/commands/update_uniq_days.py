#-*- coding: utf-8 -*-

from forum.models import MonthStat, YearStat, DayStat
from django.db import connection, transaction
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    """This command update count of uniq users posted this day   """
    help = """This command update count of uniq users posted this day"""
 
    def handle(self, *args, **options):

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
            
