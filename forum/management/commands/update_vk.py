#-*- coding: utf-8 -*-

from django.db import connection, transaction
from django.core.management.base import BaseCommand, CommandError
from forum.models import *
import re

class Command(BaseCommand):
    """This command send alert messages to users    """
    help = """This command send alert messages to users"""
 
    def handle(self, *args, **options):
        vkre = re.compile(r'<a class="url" href="http://vk.com/(.*?)"')
        for u in UserProfile.objects.filter(about__contains='vk.com'):
            print u.pk
            try:
                vk = vkre.findall(u.about)[0]
            except:
                pass
            else:
                print u.username, "http://vk.com/%s" % vk
        
