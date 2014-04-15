"""
WSGI config for nmepscor-data-collection-form project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/home/vagrant/testsite/lib/python2.7/site-packages/')
sys.path.append('/home/vagrant/testsite/nmepscor-data-collection-form/application/')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings.live")
application = get_wsgi_application()
