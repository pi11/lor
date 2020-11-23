#-*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from forum.models import UserProfile, Forum, Message

class Command(BaseCommand):
    """This command send alert messages to users    """
    help = """This command send alert messages to users"""
 
    def handle(self, *args, **options):
        talks = Forum.objects.get(name="talks")
        j = 0
        for p in UserProfile.objects.filter().order_by("-trollolo"):
            j += 1
            if j % 10 == 0:
                print j
            total = Message.objects.filter(user=p).count()
            talks_co = Message.objects.filter(user=p, forum=talks).count()

            delta = total - talks_co

            p.notalks = delta

            if delta == 0:
                delta = 1
            eff = float(talks_co) / float(delta)

            p.trollolo = eff

            p.save()

        j = 0
        for p in UserProfile.objects.filter(total_msg__gt=100, trollolo__gt=0).order_by("-trollolo"):
            j += 1
            if j % 100 == 0:
                print j
            p.trollolo_place = j
            p.save()


