#-*- coding: utf-8 -*-

from django.db import connection, transaction
from django.core.management.base import BaseCommand, CommandError

from forum.models import LongMessages, Thread, Message

class Command(BaseCommand):
    """This command send alert messages to users    """
    help = """This command send alert messages to users"""
 
    def handle(self, *args, **options):
        q = ("select length(text), ms_id from forum_messagestore"
             " order by length(text) desc limit 100;")
        cursor = connection.cursor()
        cursor.execute(q)
        res = cursor.fetchall()
        LongMessages.objects.all().delete()
        for r in res:
            m = Message.objects.get(pk=r[1])
            try:
                l = LongMessages.objects.get(url=m.thread.url)
            except LongMessages.DoesNotExist:
                if m.is_op:
                    l = LongMessages(url=m.thread.url, length=r[0])
                    l.save()
                else:
                    url = "%s#comment-%s" % (m.thread.url, m.lor_message_id)
                    l = LongMessages(url=url, length=r[0])
                    l.save()

