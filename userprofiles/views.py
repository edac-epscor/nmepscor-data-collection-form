from annoying.decorators import ajax_request

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from userprofiles.models import UserProfile, InvestigatorProfile
from builder.decorators import sessionAuthed
from model_choices import INSTITUTIONS

import json

import logging
log = logging.getLogger(__name__)


# Public Requests

@ajax_request
@csrf_protect
def getInstitutions(request):
    """
    List of institutions for form
    """
    return INSTITUTIONS


# Private/Authenticated Requests

@ajax_request
@sessionAuthed
@login_required
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
@login_required
def setProfile(request):
    """
    Save user profile object & sub PIs.

    Note -- we could serialize the deletes and process here,
    but we don't.

    """
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
@sessionAuthed
@login_required
def deletePI(request):
    """
    Given a user's PI, delete it...
    """
    sent = json.loads(request.body)
    toDelete = int(sent['pid'])
    log.info("Deleting PI: %s" % toDelete)

    investigator = InvestigatorProfile.objects.get(
        profile__user=request.user,
        pk=toDelete
    )
    investigator.delete()

    return {'success': True}
