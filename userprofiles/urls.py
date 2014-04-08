import views
from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^read$', views.getProfile),
    url(r'^update$', views.setProfile),
    url(r'^institutions$', views.getInstitutions),

    url(r'^profile/(?P<pk>\w+)$', views.UserProfileDetail.as_view(),
        name='user_profile_detail'),

    url(r'^edit/(?P<pk>\w+)$', views.UserProfileUpdate.as_view(),
        name='user_profile_edit'),

    #url(r'^$', views.UserProfileList.as_view(), name='user_profile_list'),
    #url(r'^new$', views.UserProfileCreate.as_view(), name='user_profile_new'),
    #url(r'^delete/(?P<pk>\d+)$', views.UserProfileDelete.as_view(),
    #    name='user_profile_delete')

    # Just edit your own profile.

    url(r'^pis/$', views.InvestigatorProfileList.as_view(), name='investigator_profile_list'),
    url(r'^pis/new$', views.InvestigatorProfileCreate.as_view(),
        name='investigator_profile_new'),
    url(r'^pis/edit/(?P<pk>d+)$', views.InvestigatorProfileUpdate.as_view(),
        name='investigator_profile_edit'),
    url(r'^pis/delete/(?P<pk>\d+)$', views.InvestigatorProfileDelete.as_view(),
        name='investigator_profile_delete')
)
