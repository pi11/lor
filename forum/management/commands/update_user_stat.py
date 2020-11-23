#-*- coding: utf-8 -*-

from django.db import connection, transaction
from django.core.management.base import BaseCommand, CommandError

from forum.models import UserProfile


class Command(BaseCommand):

    """This command send alert messages to users    """
    help = """This command send alert messages to users"""

    def handle(self, *args, **options):
        q = ("update forum_userprofile a set total_msg "
             "= (select count(*) from forum_message b where "
             "a.id=b.user_id and publication_date is not null group by user_id having count(*)>0);")
        cursor = connection.cursor()
        cursor.execute(q)
        transaction.commit()

        q = ("update forum_userprofile a set themes "
             "= (select count(*) from forum_message b where "
             "a.id=b.user_id and is_op = True and publication_date is not null group by user_id );")
        cursor = connection.cursor()
        cursor.execute(q)
        transaction.commit()

        j = 0
        for u in UserProfile.objects.filter().order_by("-total_msg"):
            j += 1
            u.user_place = j
            u.save()
