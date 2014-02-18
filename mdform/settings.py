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

STATIC_URL = '/builder/static/'
ADMIN_MEDIA_PREFIX = '/builder/static/admin'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

###########
# LOGGING #
###########

LOGGING = getLogDictSchema(stripColors=not DEBUG)
