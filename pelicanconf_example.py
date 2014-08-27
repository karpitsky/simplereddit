#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import os

DEBUG = True

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))

AUTHOR = u'Author'
SITENAME = u'Sitename'
SITESUBTITLE = u'Links feed'
SITEURL = u'http://localhost:8000/output'

PATH = 'content'
THEME = 'themes/simplereddit'

TIMEZONE = 'Europe/Moscow'

DEFAULT_LANG = u'ru'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
# LINKS = (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          ('You can modify those links in your config file', '#'),)
LINKS = ()

# Social widget
# SOCIAL = (('You can add links in your config file', '#'),
#           ('Another social link', '#'),)
SOCIAL = ()

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False
DISQUS_SITENAME = 'linksfeed'

# Watcher settings
UPDATE_TIME = 300  # Update feed every 5 min
FEED_URL = 'http://feeds.feedburner.com/TechCrunch/?format=xml'
DISQUS_API_KEY = ''
STATE_FILE = 'state'
