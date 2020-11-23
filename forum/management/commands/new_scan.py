#-*- coding: utf-8 -*-

from datetime import timedelta, datetime
import re
import sys
import time
from time import mktime
import random
import traceback
from pyquery import PyQuery as pq

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import DatabaseError, IntegrityError

from forum.models import *
from helpers.utils import load_url


def get_forum_from_link(link):
    for f in Forum.objects.all():
        # print f.url, link
        if f.url in link:
            return f
    print "No forum found"
    return False


def parse_arc(url):
    if 'news' in url:
        base_url = "http://www.linux.org.ru/news/"
        links_re = re.compile(r'<a href="/news/(.+?)">')
    elif 'gallery' in url:
        base_url = "http://www.linux.org.ru/gallery/"
        links_re = re.compile(r'<a href="/gallery/(.+?)">')
    else:
        base_url = "http://www.linux.org.ru/forum/"
        links_re = re.compile(r'<a href="/forum/(.+?)">')
    data = load_url(url)
    links = links_re.findall(data)
    rlinks = []
    for l in links:
        rlinks.append("%s%s" % (base_url, l))
    return rlinks


def extract_pages(data):
    pass


def parse_forum(url, data):
    print "Parsing forum: %s" % url
    base_url = "http://www.linux.org.ru"
    parsed = False
    links = []
    new_url = url  # "%s%s" % (base_url, url)
    d = pq(data)
    for l in d('td a').items():
        link = l.attr('href')
        text = l.text()
        if u"← предыдущие" in text or u"вперед →" in text:
            new_url = "%s%s" % (base_url, l.attr('href'))
            links.append(new_url)
    print "New links:", links
    return links


def get_threads(url, data):
    # print "Thread: %s " % link

    d = pq(data)
    links = []
    for l in d('a').items():
        link = l.attr('href')
        text = l.text()
        if link is None or text is None:
            continue
        # print link, text
        if u"← назад" in text or u"вперед →" in text:
            continue

        if "/forum/" in link or "/news/" in link or "/gallery/":
            if not "?offset=" in link:
                links.append(
                    link.replace('#comments', '').replace('#cut0', ''))
    print "Threads links:", links
    return links


def parse_mess(d):
    try:
        title = d('h1:first a').text()
    except AttributeError:
        title = d('div.title').text()

    mess = d('div.msg_body:first').text()
    topic = int(d('article:first').attr('id')
                .replace('topic-', '').replace('comment-', ''))
    sign = d('div.sign:first').text()
    if sign is None:
        op_user = "anonymous"
    else:
        if "anonymous" in sign:
            op_user = "anonymous"
        else:
            opu = d('.sign:first')
            op_user = opu('a:first').text()
    # print "Op_user:", op_user
    opt = d('.sign:first')
    op_time = opt('time:first').text()  # ('datetime')
    if op_time is None or op_time == "":
        print "=" * 20
        print "Op_time is NONE! WTF!?"
        print "=" * 20
        return None, None, None, None, None
    op_t = time.strptime(op_time, "%d.%m.%Y %H:%M:%S")
    op_t = datetime.fromtimestamp(mktime(op_t))
    op_profile, c = UserProfile.objects.get_or_create(username=op_user)
    return title, mess, topic, op_profile, op_t


def parse_thread(url, data, page_id):
    forum = get_forum_from_link(url)
    base_url = "http://www.linux.org.ru/forum/"
    base_url2 = "http://www.linux.org.ru"
    last_re = re.compile(r'(.*?)\?lastmod(.*?)')
    last_mod = last_re.findall(url)
    if len(last_mod) > 0:
        link = last_mod[0][0]
    start_url = url

    print "Parsing thread: %s" % start_url

    d = pq(data)
    first_mess = d('article:first')
    title, message, topic, op_profile, op_t = parse_mess(first_mess)
    if topic is None:
        print "Topic is NONE!!! WTF!?? Ignore such thread for now"
        return data

    topic_links = d('ul#topicMenu a').items()
    thread_url = False
    for pl in topic_links:
        # print ">>", pl.text(), pl
        if pl.text() == u"Ссылка":
            thread_url = "%s%s" % (base_url2, pl.attr('href'))

    if not thread_url:
        print "Topic links", topic_links
        raise

    try:
        thread = Thread.objects.get(url=thread_url)
    except Thread.DoesNotExist:
        print "New thread! - %s" % thread_url
        thread = Thread(user=op_profile, forum=forum,
                        title=title, url=thread_url,
                        lor_id=topic, publication_date=op_t)
        thread.thread_url = start_url
        thread.save()

    j = 0
    rpage_id = page_id + 1
    comments_count = 0
    for comment in d('article').items():
        comments_count += 1
        title, message, topic, op_profile, op_t = parse_mess(comment)
        if topic is None:
            print "=" * 20
            print "Topic is none, continue..."
            continue

        try:
            mes, cr = Message.objects.get_or_create(user=op_profile,
                                                    lor_message_id=topic,
                                                    forum=forum, thread=thread)
        except Message.MultipleObjectsReturned:
            k = 0
            for m in Message.objects.filter(user=op_profile,
                                            lor_message_id=topic,
                                            forum=forum, thread=thread).order_by("id"):
                if k == 0:
                    mes = m
                    cr = False
                else:
                    m.delete()
                k += 1
        except IntegrityError:
            # if already exists, try to get it
            mes, cr = Message.objects.get_or_create(user=op_profile,
                                                    lor_message_id=topic,
                                                    forum=forum, thread=thread)

            continue

        if cr:
            mes.message_id = j * rpage_id
            mes.publication_date = op_t
            ms = MessageStore(text=message, ms=mes)
            ms.save()
        if j == 0 and page_id == 0:
            print "Top message..."
            mes.is_op = True
        try:
            mes.save()
        except IntegrityError:
            print "Error saving message!"
            continue

        j += 1
    print "Comments: %s" % comments_count

    p, c = ParsedUrls.objects.get_or_create(url=start_url)
    return data


def parse_f(links, f, arc=False):
    print "Parsing: %s [%s] " % (links, f)

    base_url = "http://www.linux.org.ru/forum"
    base_url2 = "http://www.linux.org.ru"
    print "Links to parse: %s" % links
    for l in links:
        print "Go:", l
        purl = l
        # print "Forum: %s" % purl

        f_links = parse_forum(l)
        f_links.append(purl)
        # print f_links
        for ll in f_links:
            if ll[:4] != 'http':
                ll_url = "%s%s" % (base_url, ll[0])
            else:
                ll_url = ll
                ll_url = ll_url.replace("https:", "http:")
            if arc:
                try:
                    ch = ParsedUrls.objects.get(url=ll_url)
                except ParsedUrls.DoesNotExist:
                    pass
                else:
                    print "Url:%s already parsed?" % ll_url
                    # continue

            print "Parsing.... %s" % ll_url
            threads = get_threads(ll_url)
            print "Found %s threads" % len(threads)
            for th in threads:
                th_match_re = re.compile(r'/\w{4,10}/[\-\w]{3,30}/\d+[/\w]*')
                is_thread = th_match_re.match(th)
                print "https://www.linux.org.ru%s is thread?" % (th)
                if not is_thread:
                    print "No, skip.."
                    continue
                if "/archive/" in th:
                    continue
                if th.endswith("/news/"):
                    print "NEWs. Why we skip this?"
                    continue

                nu = "%s%s" % (base_url2, th)
                new_url = False
                if arc:
                    try:
                        ch = ParsedUrls.objects.get(url=nu)
                    except ParsedUrls.DoesNotExist:
                        new_url = True
                # else:
                #    new_url = True

                if new_url == False:
                    now = datetime.now()
                    # if now - th.publication_date < timedelta(days=30):
                        # If this is new url we should parse it
                    #    new_url = True
                    #    pass

                # if this is old ulr -> skip it
                if new_url == False:
                    pass  # FIXME
                #    print "old url.. skip..."
                #    continue
                sl = 0 + random.randint(0, 1)
                # time.sleep(sl)

                page_id_re = re.compile(r'/page(\d+)')
                try:
                    page_id = int(page_id_re.findall(nu)[0])
                except IndexError:
                    page_id = 0

                d = parse_thread(nu, f, page_id)
                pqd = pq(d)
                pages = pqd('a.page-number').items()  # comments"
                new_urls = []
                for p in pages:
                    tmp_url = "%s%s" % (
                        base_url2, p.attr('href').replace('#comments', ''))
                    if tmp_url.endswith('/page1'):
                        pass
                    else:
                        new_urls.append(tmp_url)

                new_urls = list(set(new_urls))
                for nu in new_urls:
                    last_re = re.compile(r'(.*?)\?lastmod(.*?)')
                    last_mod = last_re.findall(nu)  # FIXME with urlparse
                    if len(last_mod) > 0:
                        plink = last_mod[0][0]
                    else:
                        plink = nu
                    # print "II:", nu, plink
                    new_url = False

                    try:
                        ch = ParsedUrls.objects.get(url=plink)
                    except ParsedUrls.DoesNotExist:
                        new_url = True
                    if arc == False:
                        new_url = True
                    # try:
                    #    th = Thread.objects.get(url=nu)
                    # except Thread.DoesNotExist:
                    #    new_url = True

                    if new_url == False:
                        now = datetime.now()
                        # if now - th.publication_date < timedelta(days=30):
                        #    print th.publication_date
                            # If this is new url we should parse it
                        #    new_url = True

                    # if this is old ulr -> skip it
                    if not new_url:
                        print "Old... skip"
                        continue

                    page_id_re = re.compile(r'/page(\d+)')
                    try:
                        page_id = int(page_id_re.findall(plink)[0])
                    except IndexError:
                        page_id = 0
                    d = parse_thread(plink, f, page_id)
            try:
                ch, c = ParsedUrls.objects.get_or_create(url=ll_url)
            except:
                print traceback.format_exc()
                pass


class Command(BaseCommand):

    """This command send alert messages to users    """
    help = """This command send alert messages to users"""

    def add_arguments(self, parser):
        parser.add_argument('--forum',
                            dest='forum_name',
                            )

        parser.add_argument('--thread',
                            dest='thread',
                            )

    def handle(self, *args, **options):
        print options
        if options['thread']:
            d = parse_thread(options['thread'], False, 0)
            pqd = pq(d)
            pages = pqd('a.page-number').items()  # comments"

            new_urls = []
            for p in pages:
                print p

                base_url2 = "http://www.linux.org.ru"
                new_urls.append("%s%s" % (base_url2,
                                          p.attr('href')
                                          .replace('#comments', '')))
                new_urls = list(set(new_urls))
            print new_urls

            for nu in new_urls:

                last_re = re.compile(r'(.*?)\?lastmod(.*?)')
                last_mod = last_re.findall(nu)  # FIXME with urlparse
                if len(last_mod) > 0:
                    plink = last_mod[0][0]
                else:
                    plink = nu
                    # print "II:", nu, plink
                    new_url = False

                page_id_re = re.compile(r'/page(\d+)')
                try:
                    page_id = int(page_id_re.findall(plink)[0])
                except IndexError:
                    page_id = 0
                d = parse_thread(plink, False, page_id)

        if options['forum_name']:
            forums = Forum.objects.filter(
                name=options['forum_name'])  # get(name='desktop')
        else:
            forums = Forum.objects.all()  # get(name='desktop')

        for f in forums:
            parse_f([f.url, ], f)
            links = parse_arc("%sarchive" % f.url)
            parse_f(links, f, arc=True)

        return None
