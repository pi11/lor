# -*- coding: utf-8 -*-
import os
from datetime import date

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db import connection
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache

os.environ['MPLCONFIGDIR'] = settings.MPLCONFIGDIR
#import matplotlib
#import matplotlib.pyplot as plt
#import matplotlib.dates as mdates

from forum.models import *
from djangohelpers.utils import get_page_range


_YEARS = [x for x in range(1999, date.today().year + 1)]

@never_cache
def home(request):
    if request.method == "GET":
        username = request.GET.get("username", False)
        if username:
            return HttpResponseRedirect("/profile/%s/" % username)
    top = 50
    last_comments = Comment.objects.filter().order_by("-publication_date")[:5]

    top_users = UserProfile.objects.filter(total_msg__isnull=False).order_by("-total_msg")[:top]


    image = "%sstat/lor.png" % settings.MEDIA_ROOT

    """
    if not os.path.exists(image):
        
        cursor = connection.cursor()
        query = ("select max(publication_date) as p, extract (year from publication_date) as ye,"
                 "extract (month from publication_date) as m, "
                 "count(*) as co from forum_message a where publication_date is not null group "
                 "by ye, m order by p desc limit %s;" % 200)
        cursor.execute(query)
        total = cursor.fetchall()
        years = [(x[0]) for x in total if x is not None]
        values = [int(x[3]) for x in total if x is not None]
        #print "VALUES:", values
        #print "YEARS", years
#        fig = plt.gcf()


        fig, ax = plt.subplots(1)

        plt.ylabel(u'Messages')
        plt.xlabel(u'Year')
        plt.title(u'Messages per Year')
        plt.plot_date(years, values, 'b-o', tz=None, xdate=True, ydate=False, figure=fig, lod=True)
        fig.autofmt_xdate()
        ax.fmt_xdata = mdates.DateFormatter('%Y-%m')
        fig.set_size_inches(20,10.5)
        fig.savefig(image)
        plt.close()

    image = "%sstat/lor-detailed.png" % settings.MEDIA_ROOT

    if not os.path.exists(image):
        
        cursor = connection.cursor()
        query = ("select max(publication_date) as p, extract (year from publication_date) as ye,"
                 "extract (month from publication_date) as m, "
                 "count(*) as co from forum_message a where publication_date is not null group "
                 "by ye, m order by p desc limit %s;" % 200)
        cursor.execute(query)
        total = cursor.fetchall()

        years = [(x[0]) for x in total]
        values = [int(x[3]) for x in total]

#        fig = plt.gcf()


        fig, ax = plt.subplots(1)

        plt.ylabel(u'Messages')
        plt.xlabel(u'Year')
        plt.title(u'Messages per Year')
        plt.plot_date(years, values, 'b-o', tz=None, xdate=True, ydate=False, figure=fig, lod=True)
        fig.autofmt_xdate()
        ax.fmt_xdata = mdates.DateFormatter('%Y-%m')
        fig.set_size_inches(50, 18)
        fig.savefig(image)
        plt.close()


    """
    years = YearStat.objects.all().order_by("year")
    last_year = YearStat.objects.filter().order_by("-year")[0]
    months = MonthStat.objects.filter(year=last_year).order_by("month")
    last_month = MonthStat.objects.filter(year=last_year).order_by("-month")[0]
    days = DayStat.objects.filter(month=last_month).order_by("day")
    
    forums = Forum.objects.all()
    
    return render(request, "index.html", locals())

def profile(request, username):
    cursor = connection.cursor()
    p = get_object_or_404(UserProfile, username=username)
    last_comments = Message.objects.filter(user=p).order_by("-id")[:10]
    
    if p.trollolo_place < 5:
        lol = "Гуру флуда"
    elif p.trollolo_place < 25:
        lol = "Великий флудер"
    elif p.trollolo_place < 50:
        lol = "Мастер флуда"
    elif p.trollolo_place < 150:
        lol = "Специалист флуда I класса"
    elif p.trollolo_place < 250:
        lol = "Специалист флуда II класса"
    elif p.trollolo_place < 500:
        lol = "Обычный флудер"
    else:
        lol = "Обычный юзер"

    if p.trollolo_place == 0:
        lol = "Обычный юзер"
 
    query = ("select count(*) as co, (select name from forum_forum "
             "where id=a.forum_id), (select url from forum_forum "
             "where id=a.forum_id) from forum_message a where "
             "user_id = %s group by forum_id limit 20;" % p.pk)
    cursor.execute(query)
    user_stat = cursor.fetchall()

    query = ("select count(*) as co, extract(year from publication_date)"
             " as ye from forum_message a where"
             " user_id = %s and publication_date is not null"
             " group by ye  order by ye limit 20;" % p.pk)
    cursor.execute(query)
    stat_years = cursor.fetchall()
    image = "%sprofiles/%s-years.png" % (settings.MEDIA_ROOT, p.pk)

    """
    if not os.path.exists(image):
        #print "File not exists"
        values = [int(x[0]) for x in stat_years]
        years = [int(x[1]) for x in stat_years]
        j = -1
        for i in range(1999, 2014):
            j += 1
            if i not in years:
                print j, i
                years.insert(j, i)
                values.insert(j, 0)
                pass
                
        #print years, values

        plt.ylabel(u'Messages')
        plt.xlabel(u'Year')
        plt.title(u'Statistic')
        plt.plot(years, values, 'r-o')
        plt.savefig(image)
        plt.close()
    """

    if request.method == 'POST':
        form = CommentForm(request.POST)

        #print form
        if form.is_valid():
            if "windows" in request.META.get('HTTP_USER_AGENT', '?').lower():
                return HttpResponseRedirect("http://natribu.org/")
            r = form.save(commit=False)
            r.userprofile = p
            r.ip = request.META.get('REMOTE_ADDR', '?')
            r.ua = request.META.get('HTTP_USER_AGENT', '?')
            r.save()
        else:
            error = True

    else:
        form = CommentForm(instance=p)
    comments = Comment.objects.filter(userprofile=p).order_by("-publication_date")
    return render(request, "profile.html", locals())



def profile_year(request, username, year):
    cmp_p = request.GET.get('cmp', False)
    cmp_profile = False
    if cmp_p:
        cmp_profile = get_object_or_404(UserProfile, username=cmp_p)
    
    cursor = connection.cursor()
    p = get_object_or_404(UserProfile, username=username)

    query = ("select count(*) as co, extract(month from publication_date)"
             " as mo from forum_message a where "
             "extract(year from publication_date) = %s "
             "and user_id = %s group by mo order by mo limit 20;" % (int(year), p.pk))
    cursor.execute(query)
    stat_months = cursor.fetchall()

    if cmp_profile:
        query = ("select count(*) as co, extract(month from publication_date)"
                 " as mo from forum_message a where "
                 "extract(year from publication_date) = %s "
                 "and user_id = %s group by mo order by mo limit 20;" % (int(year), cmp_profile.pk))
        cursor.execute(query)
        cmp_stat_months = cursor.fetchall()
    else:
        cmp_stat_months = []


    return render(request, "profile-month.html", {"p": p, "cmp_stat_months":cmp_stat_months,
                                                  "stat_months": stat_months,
                                                  "year": year})

def forum_top(request, forum_name):
    top = 50
    f = get_object_or_404(Forum, name=forum_name)
    cursor = connection.cursor()
    query = ("select (select username from forum_userprofile where "
             "id=a.user_id), count(*) as co from forum_message a where "
             "forum_id = %s group by user_id order by count(*) "
             "desc limit %s;" % (f.pk, top))
    cursor.execute(query)
    top = cursor.fetchall()

    years = ForumYearStat.objects.filter(forum=f).order_by("year")
    tyears = _YEARS
    return render(request, "forum-top.html", locals())

    

def top_long(request):
    top = 30
    cursor = connection.cursor()
    query = ("select username from forum_userprofile order by length(username) "
             "desc limit %s;" % top)
    cursor.execute(query)
    top = cursor.fetchall()
    
    return render(request, "top-long.html", locals())


def top_threads(request, year=False):
    top = 30
    cursor = connection.cursor()
    if year:
        query = ("select thread_url, count(*) as co, max(title) from "
             "forum_message a, forum_thread b where "
             "a.thread_id=b.id and extract(year from b.publication_date) = %s "
             "group by b.thread_url order by co "
             "desc limit %s;" % (year, top))
    else:
        query = ("select thread_url, count(*) as co, max(title) from "
             "forum_message a, forum_thread b where "
             "a.thread_id=b.id group by b.thread_url order by co "
             "desc limit %s;" % top)

    cursor.execute(query)
    top = cursor.fetchall()
    years = _YEARS

    return render(request, "top-threads.html", locals())

def users_list(request):
    total = 50
    users = UserProfile.objects.filter(total_msg__gt=0).order_by("-total_msg")
    paginator = Paginator(users, total)
    page_id = int(request.GET.get("p", 1))
    add_p = (page_id - 1) * total
    try:
        page = paginator.page(page_id)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    page_range = get_page_range(paginator, page_id)
    return render(request, "users-list.html", locals())

def topic_starters(request):
    total = 50
    users = UserProfile.objects.filter(themes__isnull=False).order_by("-themes")
    paginator = Paginator(users, total)
    page_id = int(request.GET.get("p", 1))
    add_p = (page_id - 1) * total
    try:
        page = paginator.page(page_id)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    page_range = get_page_range(paginator, page_id)
    return render(request, "topic-starters.html", locals())
    

def talkers(request):
    total = 50
    users = UserProfile.objects.filter(total_msg__gt=100, trollolo__gt=0).order_by("-trollolo")
    paginator = Paginator(users, total)
    page_id = int(request.GET.get("p", 1))
    add_p = (page_id - 1) * total
    try:
        page = paginator.page(page_id)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    page_range = get_page_range(paginator, page_id)
    return render(request, "talkers.html", locals())


def no_talks(request):
    total = 50
    users = UserProfile.objects.filter(notalks__gt=0).order_by("-notalks")
    paginator = Paginator(users, total)
    page_id = int(request.GET.get("p", 1))
    add_p = (page_id - 1) * total
    try:
        page = paginator.page(page_id)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    page_range = get_page_range(paginator, page_id)
    return render(request, "no-talks.html", locals())
    


def long_comments(request):
    comments = LongMessages.objects.all()
    return render(request, "long-comments.html", locals())

def vg(request):
    users = LSMessage.objects.filter().order_by("-avglen")[:100]
    return render(request, "verbose-guys.html", locals())

def bg(request):
    users = LSMessage.objects.filter().order_by("avglen")[:100]
    return render(request, "brief-guys.html", locals())

def bydate(request, year=None, month=None):
    years = _YEARS
    top = 100
    if year:
        cursor = connection.cursor()
        query = ("select distinct(extract(month from publication_date)) as m"
                 " from forum_message where extract(year from "
                 "publication_date) = %s order by 1" % year)
        cursor.execute(query)
        months = cursor.fetchall()
    if month == None:
        query = ("select (select username from forum_userprofile where "
                 "id=a.user_id), count(*) as co from forum_message a where "
                 "extract(year from publication_date)=%s group by user_id "
                 "order by count(*) desc limit %s;" % (year, top))
    else:
        query = ("select (select username from forum_userprofile where "
                 "id=a.user_id), count(*) as co from forum_message a where "
                 "extract(year from publication_date)=%s and "
                 "extract(month from publication_date)=%s "
                 "group by user_id order by count(*) "
                 "desc limit %s;" % (year, month, top))
    if year:
        cursor.execute(query)
        top_users = cursor.fetchall()        

    return render(request, "by-date.html", locals())

def message(request, mid):
    mess = get_object_or_404(Message, pk=mid)
    mstore = get_object_or_404(MessageStore, ms=mess)
    return render(request, "message.html", locals())

@never_cache
def year_stat(request, year, cyear=None):
    y = get_object_or_404(YearStat, year=year)

    months = MonthStat.objects.filter(year=y).order_by('month')
    forums = ForumYearStat.objects.filter(year=year).order_by('-count')

    #print cyear
    if cyear:
        cy = get_object_or_404(YearStat, year=cyear)
        cmp_months = MonthStat.objects.filter(year=cy).order_by('month')
    years = _YEARS
    return render(request, "month-stat.html", locals())

@never_cache
def month_stat(request, year, month):
    y = get_object_or_404(YearStat, year=year)
    month = get_object_or_404(MonthStat, year=y, month=month)
    days = DayStat.objects.filter(month=month).order_by('day')
    return render(request, "day-stat.html", locals())
    


@never_cache
def forum_year_stat(request, forum_name, year, cyear=None):
    f = get_object_or_404(Forum, name=forum_name)
    y = get_object_or_404(ForumYearStat, year=year, forum=f)

    months = ForumMonthStat.objects.filter(year=y, forum=f).order_by('month')
    #print cyear
    if cyear:
        cy = get_object_or_404(ForumYearStat, year=cyear, forum=f)
        cmp_months = ForumMonthStat.objects.filter(year=cy, forum=f).order_by('month')
    years = _YEARS
    return render(request, "forum-month-stat.html", locals())

@never_cache
def forum_month_stat(request, forum_name, year, month):
    f = get_object_or_404(Forum, name=forum_name)
    y = get_object_or_404(ForumYearStat, year=year, forum=f)
    print y.id
    month = get_object_or_404(ForumMonthStat, year=y, month=month, forum=f)
    print month.pk, f.pk
    days = ForumDayStat.objects.filter(month=month, forum=f).order_by('day')
    print days
    return render(request, "forum-day-stat.html", locals())


def users_list_year(request, year):
    q = """select user_id from forum_message
           where date_part('year', publication_date at time zone 'Europe/Moscow') = %s
           group by user_id order by count(*) desc limit 50;
           """ % year
    cursor = connection.cursor()
    cursor.execute(q)
    users_ids = [i[0] for i in cursor.fetchall()]
    profiles = UserProfile.objects.filter(pk__in=users_ids)
    months = [1,2,3,4,5,6,7,8,9,10,11,12] # FIXME show only active months
    return render(request, "users-list-year.html", {"profiles":profiles, "year":year,
                                                    "months":months})

def users_list_month(request, year, month):
    q = """select user_id from forum_message
           where date_part('year', publication_date at time zone 'Europe/Moscow') = %s
           and date_part('month', publication_date at time zone 'Europe/Moscow') = %s
           group by user_id order by count(*) desc limit 50;
           """ % (year, month)
    cursor = connection.cursor()
    cursor.execute(q)
    users_ids = [i[0] for i in cursor.fetchall()]
    profiles = UserProfile.objects.filter(pk__in=users_ids)
    
    return render(request, "users-list-month.html", {"profiles":profiles,
                                                     "year":year, "month":month})


def top_news_makers(request):
    profiles = UserProfile.objects.filter().order_by("-news_count")[:100]
    return render(request, "top-news-makers.html", {"users":profiles})


def cit(request):
    users = CitIndex.objects.filter(count__gt=0).order_by("-count")
    return render(request, "user-cit-index.html",
                  {"users": users})
