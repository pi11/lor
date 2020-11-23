#-*- coding: utf-8 -*-

import nltk, string
from pymorphy import get_morph

from django.core.management.base import BaseCommand, CommandError
from django.utils.html import strip_tags
import re
from forum.models import *

class Command(BaseCommand):
    """This command send alert messages to users    """
    help = """This command send alert messages to users"""

    def handle(self, *args, **options):
        for u in UserProfile.objects.order_by("-total_msg")[:50000]:
            try:
                print u.username
            except:
                pass
