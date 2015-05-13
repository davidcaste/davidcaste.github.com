#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'David Castellanos'
SITENAME = u'pataliebre.net'
SITEURL = ''

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'es'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
#LINKS =  (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),)

# Social widget
SOCIAL = (('github', 'http://github.com/davidcaste'),
          ('linkedin', 'http://es.linkedin.com/in/davidcaste'),
          ('twitter', 'http://twitter.com/davidcaste'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

STATIC_PATHS = ['files', 'images', 'extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}

GITHUB_URL = 'https://github.com/davidcaste/davidcaste.github.com'

# Pelican plugins
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['related_posts', 'pelican_gist']

# Pelican-bootstrap3 Theme Settings
THEME = 'pelican-bootstrap3'
BOOTSTRAP_NAVBAR_INVERSE = True
BOOTSTRAP_THEME = "united"

CC_LICENSE = "CC-BY"

DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False

DISPLAY_CATEGORIES_ON_SIDEBAR = True
DISPLAY_TAGS_INLINE = True
TAG_CLOUD_MAX_ITEMS = 10

USE_PAGER = True
DEFAULT_PAGINATION = 5
