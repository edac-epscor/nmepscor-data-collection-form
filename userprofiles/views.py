#from django.shortcuts import render

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from django.views.generic import ListView, DetailView
#from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User

from annoying.decorators import ajax_request
from django.contrib.auth.decorators import login_required

from userprofiles.models import UserProfile, InvestigatorProfile
from builder.decorators import sessionAuthed
import json

from model_choices import INSTITUTIONS

# Create your views here.

import logging
log = logging.getLogger(__name__)


def only_edit_self(request, pk):
    """
    Mixin, Fail if attempt to edit other than self
    """
    user = request.user
    if user.username != pk:
        raise Http404("Not authorized to edit this user: %s" % pk)


@ajax_request
@sessionAuthed
def getProfile(request):
    """
    Return MY profile for editing.
    """

    profile = UserProfile.objects.get(
        user=request.user
    )

    return profile.ajax()


@ajax_request
@sessionAuthed
def setProfile(request):
    updated = json.loads(request.body)
    log.debug("update profile: %s" % updated)

    profile = UserProfile.objects.get(
        user=request.user
    )

    # Can only save to your own profile info
    profile.jsonSave(updated)

    # New elements may have IDs set
    return profile.ajax()


@ajax_request
def getInstitutions(request):
    """
    List of institutions for form
    """
    return INSTITUTIONS


class UserProfileMixin(object):
    """
    Override  views.generic:
         get_object method, basically core django code but by username
         get method to require login
    """
    def get_object(self, queryset=None):

        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg, None)

        if pk is not None:
            # hardcode my PK instead of using pk attr
            queryset = queryset.filter(
                user=User.objects.get(username=pk)
            )

        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404((u"No %(verbose_name)s found matching the query") %
                {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    # And use the same get method, but override
    def get(self, request, *args, **kwargs):
        login_required(request)
        only_edit_self(request, *args, **kwargs)

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class UserProfileDetail(UserProfileMixin, DetailView):
    model = UserProfile


class UserProfileUpdate(UserProfileMixin, UpdateView):
    model = UserProfile
    success_url = reverse_lazy('user_profile_list')


class InvestigatorProfileList(ListView):
    model = InvestigatorProfile


class InvestigatorProfileCreate(CreateView):
    model = InvestigatorProfile
    success_url = reverse_lazy('investigator_profile_list')


class InvestigatorProfileUpdate(UpdateView):
    model = InvestigatorProfile
    success_url = reverse_lazy('investigator_profile_list')


class InvestigatorProfileDelete(DeleteView):
    model = InvestigatorProfile
    success_url = reverse_lazy('investigator_profile_list')
