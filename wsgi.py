"""
WSGI config for mdform project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os, sys

sys.path.append('/home/vagrant/testsite/lib/python2.7/site-packages/')
sys.path.append('/home/vagrant/testsite/nmepscor-data-collection-form/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mdform.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
