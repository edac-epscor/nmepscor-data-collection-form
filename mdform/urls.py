from django.conf.urls import patterns, include, url

from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'builder.views.metadataIdx'),
    (r'^submissions/', include('builder.urls')),
    (r'^keepAlive$', 'builder.views.revalidate'),
    (r'^signin$', 'builder.views.authDrupal'),
    (r'^logout$', 'builder.views.signout'),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
    #urlpatterns += staticfiles_urlpatterns()
    #  This is supposedly equivalent to the above, but it doesn't appear to
    #  actually work.

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    urlpatterns = patterns('',
        (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    ) + urlpatterns
