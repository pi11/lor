#-*- coding: utf-8 -*-

from django.db import connection, transaction
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    """This command send alert messages to users    """
    help = """This command send alert messages to users"""
 
    def handle(self, *args, **options):
        with open("result-rutube1.txt", "w+") as r:

            q = ("select regexp_matches(text, 'rutube.ru/tracks/(\d+)\.') from forum_messagestore where text like '%rutube.ru%'")
            cursor = connection.cursor()
            cursor.execute(q)
            for row in cursor.fetchall():
                for k in row:
                    print k[0], type(k[0])
                    r.write(k[0])
                    r.write("\n")


            q = ("select regexp_matches(text, 'rutube.ru/video/(\w+)') from forum_messagestore where text like '%rutube.ru%'")
            cursor = connection.cursor()
            cursor.execute(q)
            for row in cursor.fetchall():
                for k in row:
                    print k[0], type(k[0])
                    r.write(k[0])
                    r.write("\n")

