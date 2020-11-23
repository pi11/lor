#-*- coding: utf-8 -*-

from django.db import connection, transaction
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    """This command send alert messages to users    """
    help = """This command send alert messages to users"""
 
    def handle(self, *args, **options):
        with open("result2.txt", "w+") as r:

            q = ("select regexp_matches(text, 'vimeo.com/(\d+)') from forum_messagestore where text like '%vimeo.com%'")
            cursor = connection.cursor()
            cursor.execute(q)
            for row in cursor.fetchall():
                for k in row:
                    print k[0], type(k[0])
                    r.write(k[0])
                    r.write("\n")

            """
            q = ("select regexp_matches(text, 'youtube\.com/watch\?v=([\w\-]+)') from forum_messagestore where text like '%youtube.com%'")
            cursor = connection.cursor()
            cursor.execute(q)
            for row in cursor.fetchall():
                for k in row:
                    print k[0], type(k[0])
                    r.write(k[0])
                    r.write("\n")

            print "Next"
            q = ("select regexp_matches(text, 'youtu.be/([\w\-]+)') from forum_messagestore where text like '%youtu.be%'")
            cursor = connection.cursor()
            cursor.execute(q)

            for row in cursor.fetchall():
                for k in row:
                    print k[0], type(k[0])
                    r.write(k[0])
                    r.write("\n")

"""
