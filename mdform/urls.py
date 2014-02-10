from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mdform.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^builder/', include('builder.urls')),
    (r'^keepAlive$', 'builder.views.revalidate'),
    (r'^signin$', 'builder.views.authDrupal'),
    (r'^logout$', 'builder.views.signout'),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {
                'document_root': settings.MEDIA_ROOT,
                'show_indexes': True
            })
    )

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    urlpatterns = patterns('',
        (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    ) + urlpatterns
