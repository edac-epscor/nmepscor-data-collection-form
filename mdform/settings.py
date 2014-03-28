"""
Django settings for mdform project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from secret_settings import SECRET_KEY, SECRET_EPSCOR_SERVER, ADMINS,\
    ALLOWED_HOSTS

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from customLogger import getLogDictSchema
import django.conf.global_settings as DEFAULT_SETTINGS

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# To prevent login to the admin site and pop an error message.
#  Handy when performing updates in the console
ADMIN_ENABLED = True

TEMPLATE_DEBUG = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'djangobower',
    'builder',
)

if DEBUG:
    INSTALLED_APPS += (
        #'debug_toolbar',  # Debug toolbar causes nasty wsgi/urls.py crashes
        'django.contrib.admindocs',
    )

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(BASE_DIR, '..', 'builder', 'templates'),
]


MIDDLEWARE_CLASSES = DEFAULT_SETTINGS.MIDDLEWARE_CLASSES + (
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mdform.urls'

WSGI_APPLICATION = 'mdform.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Denver'

USE_I18N = False

USE_L10N = True

USE_TZ = True

SESSION_COOKIE_HTTPONLY = True
# No JS tampering
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True

#  Not needed w/ standalone install, but if we ever cohost handy
SITE_ID = 1


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

WEB_ROOT = '/builder'  # If deploy in '/', '' if in /builder, '/builder'

# Web (can't use urlparse.urljoin...)
STATIC_URL = "{0}/static/".format(WEB_ROOT)
ADMIN_MEDIA_PREFIX = "{0}admin".format(STATIC_URL)

# System
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_FINDERS = tuple(
    list(DEFAULT_SETTINGS.STATICFILES_FINDERS) +
    ['djangobower.finders.BowerFinder'],
)

###########
# LOGGING #
###########

LOGGING = getLogDictSchema(stripColors=not DEBUG)

############
# BOWER/JS #
############

BOWER_COMPONENTS_ROOT = os.path.join(
    BASE_DIR, 'vendor_components'
)

BOWER_INSTALLED_APPS = (
    'jquery#1.10.2',
    'jqueryui#1.9.2',

    'modernizr#2.6.2',
    'respond#1.1.0',

    #'angular#1.0.8',
    #'angular-cookies#1.0.8',
    #'angular-sanitize#1.0.8',  # upgraded
    'angular#1.2.1',
    'angular-cookies#1.2.1',
    'angular-sanitize#1.2.1',  # upgraded
    'angular-route#1.2.1',  # upgraded

    'bootstrap#3.0.0',
    'angular-ui-bootstrap-bower#0.1.0',  # 2xcheck

    'angular-ui#0.4.0',
    # my ngr-grid was pre 2.0.3
    'ng-grid#2.0.3',
    #'angular-ui-bootstrap#0.1.0',  # Wrong formatting for tpls build ?
    'angular-xeditable#0.1.7',  # choose 3.0.0 in bower

    'underscore#1.4.4',  # upgraded
    #'ace-builds#1.1.1',  # we were cdnjs 1.1.01
    #'angular-ui-ace#0.1.0',  # upgraded
    #'google-code-prettify',  # the bower finds are...weird...sticking with cdnjs right now
    'angular-strap#0.7.5',  # choose 3.0.0 in bower

    'noty#2.1.0',  # choose 3.0.0 in bower
    # somewhere the nucleus theme came into existence
)
