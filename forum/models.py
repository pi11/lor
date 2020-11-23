# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.signals import request_finished
from django.db.models.signals import pre_save, post_save
from django.core.mail import send_mail, mail_admins
from django.template.defaultfilters import slugify
from django.forms import ModelForm


class Tag(models.Model):
    name = models.CharField(max_length=250, unique=True)
    count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    username = models.CharField(max_length=150)
    user_id = models.IntegerField(default=0)
    reg_date = models.CharField(max_length=40)
    last_visit = models.DateTimeField(null=True, blank=True)
    stars_count = models.IntegerField(default=0)
    is_stars_grey = models.BooleanField(default=False)

    fav_tags = models.ManyToManyField(Tag)

    is_active = models.BooleanField(default=False)
    about = models.TextField(null=True, blank=True)

    total_msg = models.IntegerField(default=0)
    themes = models.IntegerField(default=0)
    user_place = models.IntegerField(default=0)

    trollolo = models.FloatField(default=0)
    trollolo_place = models.IntegerField(default=0)
    notalks = models.IntegerField(default=0)

    news_count = models.IntegerField(default=0)

    is_updated = models.BooleanField(default=False)
    avatar = models.CharField(max_length=300)

    def __unicode__(self):
        return self.username

    def get_avatar(self):
        if self.avatar != "":
            if self.avatar[0] == "/":
                return "http://www.linux.org.ru%s" % self.avatar
        else:
            return "/static/images/logo.png"
        return self.avatar


class Word(models.Model):
    name = models.CharField(max_length=50, unique=True)
    count = models.IntegerField(default=1)
    is_usable = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class UserWord(models.Model):
    user = models.ForeignKey(UserProfile)
    word = models.ForeignKey(Word)
    count = models.IntegerField(default=1)

    def __unicode__(self):
        return self.user


class Forum(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    messages = models.IntegerField()

    def __unicode__(self):
        return self.name

    def get_color(self):  # FIXME
        colors = {"Новости": "FF7600",
                  "general": "B35300", "desktop": "FFBB80",
                  "admin": "FFDDBF", "linux-install": "FFD300",
                  "development": "B39400", "linux-org-ru": "FFE980",
                  "security": "FFF4BF", "linux-hardware": "43AE39",
                  "talks": "FF7259", "job": "B1FFA9", "games": "D8FFB4",
                  "web-development": "336698", "lor-source": "24476A",
                  "mobile": "AAD5FF", "science": "DSEAFF",
                  "multimedia": "DDFF28", "midnight": "28FFDA",
                  "gallery": "FFB128", "polls": "245300"}

        try:
            c = colors[self.name]
        except KeyError:
            c = "FFFF00"
        return c

    def get_h_color(self):
        return "FF7A00"


class Thread(models.Model):
    user = models.ForeignKey(UserProfile)
    forum = models.ForeignKey(Forum)
    title = models.CharField(max_length=250)
    url = models.CharField(max_length=500, unique=True)
    thread_url = models.CharField(max_length=500)
    lor_id = models.IntegerField()
    publication_date = models.DateTimeField()
    year = models.SmallIntegerField(default=0)
    month = models.SmallIntegerField(default=0)

    def __unicode__(self):
        return self.title


class MessageStore(models.Model):
    text = models.TextField()
    ms = models.ForeignKey('Message')
    is_processed = models.BooleanField(default=False)
    have_href = models.BooleanField(default=False)
    image_ex = models.BooleanField(default=False)


class Message(models.Model):
    forum = models.ForeignKey(Forum)
    user = models.ForeignKey(UserProfile, editable=False)
    thread = models.ForeignKey(Thread, editable=False)
    is_op = models.BooleanField(default=False)
    message_id = models.IntegerField(null=True, blank=True)
    lor_message_id = models.IntegerField()
    reply_to = models.IntegerField(default=0)  # 0 - no reply

    publication_date = models.DateTimeField(null=True, blank=True)

    year = models.SmallIntegerField(default=0)
    month = models.SmallIntegerField(default=0)

    def __unicode__(self):
        return u"%s: [%s]" % (self.user, self.message_id)

    def get_text(self):
        return MessageStore.objects.get(ms=self)


class ParsedUrls(models.Model):
    url = models.CharField(max_length=500, unique=True)


class LongMessages(models.Model):
    url = models.CharField(max_length=500, unique=True)
    length = models.IntegerField()


class Comment(models.Model):
    userprofile = models.ForeignKey(UserProfile)
    nick = models.CharField(max_length=100)
    text = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', null=True, blank=True)
    ip = models.CharField(max_length=25)
    ua = models.CharField(max_length=512)

    def __unicode__(self):
        return self.text


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        exclude = ('publication_date', 'userprofile', 'reply', 'ip', 'ua')


class LSMessage(models.Model):
    user = models.ForeignKey(UserProfile)
    avglen = models.IntegerField()

    def __unicode__(self):
        return unicode(self.user)


class Vk(models.Model):
    user = models.ForeignKey(UserProfile)
    url = models.CharField(max_length=100)

    def __unicode__(self):
        return self.url


class Image(models.Model):
    image_url = models.CharField(max_length=512, unique=True)
    image = models.ImageField(
        null=True, blank=True, upload_to="media/images/%Y-%m/")
    is_exists = models.BooleanField(default=True)
    last_check = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.image_url


class YearStat(models.Model):
    year = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    uniq = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s (%s)" % (self.year, self.count)


class MonthStat(models.Model):
    year = models.ForeignKey(YearStat)
    month = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    uniq = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s (%s)" % (self.month, self.count)

    def get_desc(self):
        months = [u"", u"январь", u"февраль", u"март", u"апрель", u"май",
                  u"июнь", u"июль", u"август", u"сентябрь", u"октябрь",
                  u"ноябрь", u"декабрь", ]
        print self.month
        return months[self.month]


class DayStat(models.Model):
    month = models.ForeignKey(MonthStat)
    day = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    uniq = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s (%s)" % (self.day, self.count)


class ForumYearStat(models.Model):
    forum = models.ForeignKey(Forum)
    year = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    uniq = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s (%s)" % (self.year, self.count)


class ForumMonthStat(models.Model):
    forum = models.ForeignKey(Forum)
    year = models.ForeignKey(ForumYearStat)
    month = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    uniq = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s (%s)" % (self.month, self.count)

    def get_desc(self):
        months = [u"", u"январь", u"февраль", u"март", u"апрель", u"май",
                  u"июнь", u"июль", u"август", u"сентябрь", u"октябрь",
                  u"ноябрь", u"декабрь", ]
        print self.month
        return months[self.month]


class ForumDayStat(models.Model):
    forum = models.ForeignKey(Forum)
    month = models.ForeignKey(ForumMonthStat)
    day = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    uniq = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s (%s)" % (self.day, self.count)

class CitIndex(models.Model):
    user = models.OneToOneField(UserProfile)
    count = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s %s" % (self.user, self.count)
        

class Queue(models.Model):
    url = models.CharField(max_length=250)
    added = models.DateTimeField(auto_now_add=True)
    is_parsed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.url

