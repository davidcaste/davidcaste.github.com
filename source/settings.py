# ===============
# Basic settings
# ===============
AUTHOR = 'David Castellanos'
DEFAULT_CATEGORY = 'general'
SITENAME = 'pataliebre.net'
SITEURL = 'http://pataliebre.net'
STATIC_PATHS = ['images', 'files']
TIMEZONE = 'Europe/Madrid'
DEFAULT_LANG = 'es'
FILES_TO_COPY = [('CNAME', 'CNAME')]

# =============
# URL settings
# =============
PERMALINK_STRUCTURE = '{date:%Y}/{date:%m}/'
ARTICLE_URL = '%s{slug}.html' % PERMALINK_STRUCTURE
ARTICLE_LANG_URL = '%s{slug}-{lang}.html' % PERMALINK_STRUCTURE
PAGE_URL = '%spages/{slug}.html' % PERMALINK_STRUCTURE
PAGE_LANG_URL = '%spages/{slug}-{lang}.html' % PERMALINK_STRUCTURE
ARTICLE_SAVE_AS = '%s{slug}.html' % PERMALINK_STRUCTURE
ARTICLE_LANG_SAVE_AS = '%s{slug}-{lang}.html' % PERMALINK_STRUCTURE
PAGE_SAVE_AS = '%spages/{slug}.html' % PERMALINK_STRUCTURE
PAGE_LANG_SAVE_AS = '%spages/{slug}-{lang}.html' % PERMALINK_STRUCTURE


# ===========
# Pagination
# ===========
WITH_PAGINATION = True
DEFAULT_PAGINATION = 10


# =================
# Ordering content
# =================
REVERSE_ARCHIVE_ORDER = True


# =================
# Theming
# =================
THEME = 'notmyidea'
DISPLAY_PAGES_ON_MENU = True

DISQUS_SITENAME = 'pataliebredotnet'
GITHUB_URL = 'http://github.com/davidcaste/davidcaste.github.com'
GOOGLE_ANALYTICS = 'UA-31198203-1'
MENUITEMS = (
#    ('Archives', '{0}/archives.html'.format(SITEURL)),
#    ('Tags', 'tags.html'),
)
TWITTER_USERNAME = 'davidcaste'
