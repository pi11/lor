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

    def process(self, interval):
        jk_re = re.compile(r"%s" % u'(.*?)[\w_\-]+[\s]{1,3}\( (.*?) \)(.*?)Ссылка$')
        cit_re = re.compile(r"%s" % u">>-----Цитата---->>(.*?)<<-----Цитата----<<", re.DOTALL)
        rus = u"йцукенгшщзхъёфывапролджэячсмитьбю."
        morph = get_morph('dicts')
        finished = True
        for m in MessageStore.objects.filter(is_processed=False).order_by("-id")[:interval]:
            finished = False
            user = m.ms.user
            #print user
            
            data = strip_tags(m.text).strip()
            data = re.sub(cit_re, "", data)
            jk = jk_re.findall(data)
            try:
                line = jk[0][0]
            except IndexError:
                print "ERROR: [%s]" % data
                line = data.replace(u">>> Подробности", "")[:-33]
                
            tokens = nltk.word_tokenize(line.lower())
            #text = nltk.word_tokenize(line.lower())
            #print nltk.pos_tag(text)
            m.is_processed = True
            m.save(update_fields=['is_processed'])
            
            for t in tokens:
                if len(t) > 35 or len(t) < 4:
                    continue
                if t in string.punctuation or t in string.letters or t in rus:
                    print "%s skipped" % t
                else:
                    tok = morph.normalize(t.upper())
                    if isinstance(tok, unicode):
                        word = tok.lower()
                    else:
                        word = list(tok)[0].lower()
                    #print word
                    w, c = Word.objects.get_or_create(name=word)
                    if not c:
                        w.count += 1
                        w.save(update_fields=["count"])
                    wu, c = UserWord.objects.get_or_create(word=w, user=user)
                    if not c:
                        wu.count += 1
                        wu.save(update_fields=["count"])
        return finished

        
    def handle(self, *args, **options):
        interval = 1000
        finished = False
        from random import randint
        while not finished:
            print "[Processing, please wait... %s ]" % randint(0, 100)
            finished = self.process(interval)

