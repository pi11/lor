#-*- coding: utf-8 -*-
# This script should be started from cron as many times as needed
# it take only alerts which was not checked for last 24 hours
# it found new listings for users Alert


from datetime import timedelta, datetime 
import re, sys
import time
from time import mktime
import random, urllib
from pyquery import PyQuery as pq

from django.core.management.base import BaseCommand, CommandError
from forum.models import *
from helpers.utils import load_url


class Command(BaseCommand):
    """This command send alert messages to users    """
    help = """This command send alert messages to users"""
 
    def handle(self, *args, **options):
        for user in UserProfile.objects.filter(is_updated=False):
            print user.username
            try:
                page = load_url("http://www.linux.org.ru/people/%s/profile" % user.username)
            except UnicodeEncodeError: # FIXME
                user.is_updated = True
                user.save()
                continue
                
            if page == False:
                user.is_updated = True
                user.save()
                continue
            try:
                data = unicode(page.decode(encoding='UTF-8'))
            except UnicodeEncodeError: # FIXME
                user.is_updated = True
                user.save()
                continue
                
            d = pq(data)
            avatar = d('div.userpic img.photo').attr('src')
            print user.username, avatar
            about = d('div#bd')
            user.avatar = avatar
            user.about = about
            user.is_updated = True
            user.save()
            
