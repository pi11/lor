from django.conf.urls import include, url

from forum.views import *

urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'^profile/(?P<username>.*?)/(?P<year>\d{4})/$', profile_year, name="profile_year"),
    url(r'^profile/(?P<username>.*?)/$', profile, name="profile"),
                       
    url(r'^forum/(?P<forum_name>[\-_\w]+)/$', forum_top, name="forum_top"),

    url(r'^top-long/$', top_long, name="top_long"),
    url(r'^long-comments/$', long_comments, name="long_comments"),
    #url(r'^top-threads/(?P<year>\d{4})/$', top_threads, name="top_threads_year"),
    #url(r'^top-threads/$', top_threads, name="top_threads"),
    url(r'^users-list/$', users_list, name="users_list"),
    url(r'^topic-starters/$', topic_starters, name="topic_starters"),
    url(r'^talkers/$', talkers, name="talkers"),
    url(r'^no-talks/$', no_talks, name="no_talks"),

    url(r'^verbose-guys/$', vg, name="verbose_guys"),
    url(r'^brief-guys/$', bg, name="brief_guys"),

    url(r'^by-date/(?P<year>\d{4})/(?P<month>\d{1,2})/$', bydate, name="bydate"),
    url(r'^by-date/(?P<year>\d{4})/$', bydate, name="bydate"),
    url(r'^by-date/$', bydate, name="bydate"),
    url(r'^year/(\d+)/cmp/(\d+)/$', year_stat, name="year_stat"),

    url(r'^year/(\d+)/$', year_stat, name="year_stat"),
    url(r'^year/(\d+)/month/(\d+)/$', month_stat, name="month_stat"),

    url(r'^forum/(?P<forum_name>[\-_\w]+)/year/(?P<year>\d+)/$', forum_year_stat, name="forum_year_stat"),
    url(r'^forum/(?P<forum_name>[\-_\w]+)/year/(?P<year>\d+)/cmp/(?P<cyear>\d+)/$', forum_year_stat, name="forum_year_stat"),

    url(r'^forum/(?P<forum_name>[\-_\w]+)/year/(?P<year>\d+)/month/(?P<month>\d+)/$', forum_month_stat, name="forum_month_stat"),


    #url(r'^message/(?P<mid>\d+)/$', message, name="message"),
    url(r'^citation-index/$', cit, name="cit"),

    url(r'^news-makers/$', top_news_makers, name="top_news_makers"),


    url(r'^users-list/year/(\d{4})/$', users_list_year, name="users_list_year"),
    url(r'^users-list/year/(\d{4})/month/(\d{1,2})/$', users_list_month, name="users_list_month"),
]
