import views
#from django.conf.urls import patterns, include, url
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^list$', views.listSubmissionsByUserId),
    url(r'^new$', views.newSubmission),
    url(r'^update$', views.updateSubmission),
    url(r'^finalize$', views.finalizeSubmission),
    # Delete?  Not yet
)
