# -*- coding: utf-8 -*-

import os
import sys
import time
from pyquery import PyQuery as pq
import requests
import pickle
import requests.cookies

from django.conf import settings



def load_url(url):
    def save_cookies(session, filename):
        with open(filename, 'w') as f:
            f.truncate()
            pickle.dump(session.cookies._cookies, f)


    def load_cookies(session, filename):
        if not os.path.isfile(filename):
            #print "NO file:", filename
            return session

        with open(filename) as f:
            loaded = False
            attempts = 5
            while not loaded and attempts > 0:
                try:
                    cookies = pickle.load(f)
                except EOFError:
                    print "EOF error while loading cookies =("
                    time.sleep(5 - attempts)
                    attempts -= 1
                else:
                    loaded = True
            if not loaded:
                print "Unable to load cookies =("
            if cookies:
                jar = requests.cookies.RequestsCookieJar()
                jar._cookies = cookies
                session.cookies = jar
                #print "FFFFF:", session.cookies
        return session

    cookie_file = "cookie.pkl"
    headers= {"User-agent": "Mozilla/5.0 (compatible; LorStatBot/0.2; +http://lor-stat.com/"}
    session = requests.session()
    session = load_cookies(session, cookie_file)
    session.headers.update(headers)
    #print "Loaded COOKIES", session.cookies

    r = session.get(url)
    #print r.cookies
    #print "#######################"
    data = r.text
    if not settings.LOR_USER in data:
        print "-=" * 20
        print "Not logged in!"
        print "Try to log in"
        # do login
        r = session.get('https://www.linux.org.ru/login.jsp')
        data = pq(r.text)
        csrf_val = data('input[name="csrf"]').attr('value')
        if not csrf_val:
            print "Csrf not found"
            print r.text
        form = {"csrf":csrf_val, "nick": settings.LOR_USER,
                "passwd": settings.LOR_PASS,}
        #print "Sending form: %s" % form
        r = session.post('https://www.linux.org.ru//login_process', data=form)

        #print "Cookies after Login attempt:"
        #print r.cookies
        #print "-=" * 20
        #print "PAGE TEXT:", r.text
        #print r.status_code


        if not settings.LOR_USER in r.text:
            print "=" * 40
            print "======[Can't log in!]====="
            print r.text
            print "=" * 40
            sys.exit()
        else:
            r = session.get(url)
            if not settings.LOR_USER in r.text:
                print "FUCK!!! " * 40
                print r.text
                print r.cookies

            #print "Cookies after next page load:"
            #print r.cookies
            data = r.text
        save_cookies(session, cookie_file)
    return data
