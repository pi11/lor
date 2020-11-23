#-*- coding: utf-8 -*-
import urllib, traceback
from django.db import connection, transaction
from django.core.management.base import BaseCommand, CommandError
from forum.models import Image, MessageStore
from django.core.files import File

class Command(BaseCommand):
    """This command send alert messages to users    """
    help = """This command send alert messages to users"""
 
    def handle(self, *args, **options):
        
        q = ("select max(id) from forum_messagestore ")
        cursor = connection.cursor()
        cursor.execute(q)
        row = cursor.fetchone()
        max_id = row[0]
        print "Max id = %s" % max_id
        
        q = ("select regexp_matches(text, 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+') from forum_messagestore where image_ex=False")
        cursor = connection.cursor()
        cursor.execute(q)
        for row in cursor.fetchall():
            for k in row:
                url = k[0].lower()
                if (url.endswith('.jpg') or url.endswith('.jpeg') \
                    or url.endswith('.png') or url.endswith('.gif') \
                    or url.endswith('.svg')):
                    print k[0], type(k[0])
                    try:
                        ch = Image.objects.get(image_url=k[0])
                    except Image.DoesNotExist:
                        nim = Image(image_url=k[0])
                        nim.save()
                    
                    """
                    """
        q = ("update forum_messagestore set image_ex=True where id < %s" % max_id)
        cursor = connection.cursor()
        cursor.execute(q)
        transaction.commit_unless_managed()

        print "Loading images..."
        for nim in Image.objects.filter(is_exists=True, image__isnull=True):
            print "Loading image %s" % nim.image_url
            
            try:
                result = urllib.urlretrieve(nim.image_url)
            except:
                print traceback.format_exc()
            if not result:
                print "Can't load image:%s" % nim.image_url
                nim.is_exists=False
            else:
                nim.image.save(
                    os.path.basename(nim.image_url),
                    File(open(result[0]), 'rb')
                    )

            nim.save()

