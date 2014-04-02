from django.conf.urls import patterns, include, url

from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'builder.views.metadataIdx'),  # Approot, not listview
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
    #  This is supposedly equivalent to the above, but never actually works

    # Admin/URL docs only on dev
    urlpatterns = patterns('',
        (r'^builder/admin/doc/', include('django.contrib.admindocs.urls')),
    ) + urlpatterns
