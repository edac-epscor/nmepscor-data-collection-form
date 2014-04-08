import views
from django.conf.urls import patterns, url

urlpatterns = patterns('',

    # Ajaxy Crud NS app & subapps

    # /users/...
    url(r'^read$', views.getProfile),
    url(r'^update$', views.setProfile),

    # /users/institutions
    url(r'^institutions/list$', views.getInstitutions),

    # /users/pis/list
    # url(r'^pis/list$', views.getInstitutions),
    # /users/pis/delete
    url(r'^pis/delete$', views.deletePI),
)
