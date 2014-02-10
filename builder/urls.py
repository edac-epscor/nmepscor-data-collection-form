import views
#from django.conf.urls import patterns, include, url
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mdform.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.metadataIdx),
    url(r'^submissions/list$', views.listSubmissionsByUserId),
    url(r'^submissions/new$', views.newSubmission),
    url(r'^submissions/update$', views.updateSubmission),
    url(r'^submissions/finalize$', views.finalizeSubmission),
    # Delete?  Not yet
)
