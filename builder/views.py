"""
views.py
   Django views.  Not exclusive to application.

RCS Info:
   $Id: views.py 2162 2013-06-18 14:48:44Z jbrown $

   Last Revised    :  $Date: 2013-06-18 08:48:44 -0600 (Tue, 18 Jun 2013) $
   By              :  $Author: jbrown $
   Rev             :  $Rev: 2162 $

TODO:
   - copyright notice
"""

import os
import json

from django.shortcuts import render
#from django.template.response import TemplateResponse
#from django.template import RequestContext

from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.http import HttpResponse
from django.utils.html import strip_tags

from models import metadataModel
from decorators import sessionAuthed

import util
from util import SESSION
from util import datetime2Human

from bs4 import BeautifulSoup
from annoying.decorators import ajax_request

import logging
log = logging.getLogger(__name__)


# TODO: cookie validating decorator
@ajax_request
@sessionAuthed
def listSubmissionsByUserId(request):
    """
    Given a userid (we must be logged in and authorized), return
    JSON list of the datasets they have

    """
    # OK, the userid number in drupal would be the nice way to do this, but we
    # have to parse drupal pages to get that, not gonna happen.

    # We do know their username/login, which could change, but is at least
    # unique.

    # right now uid is a string, but it should be the epscor id

    # get username -- better be accurate

    # POST
    submitted = json.loads(request.body)
    username = submitted['username']

    userDR = metadataModel.objects.filter(
        username=username
    )

    # User needs:
    toRet = {
        'submissions': []
    }

    for i in userDR:
        toRet['submissions'].append({
            'id': i.submissionID,
            'identifier': i.identifier,
            'finalized': i.finalized,
            'started': datetime2Human(i.started),
            'modified': datetime2Human(i.modified),
            'fullForm': i.mdForm
        })

    log.info("Returning: '%s'" % json.dumps(toRet))
    return toRet


# TODO: cookie validating decorator
@sessionAuthed
@ensure_csrf_cookie
@ajax_request
def newSubmission(request):
    """
    Create a new submission

    Returns:  real submission object with good ID, etc.
    """

    log.debug("session: %s" % request.session.keys())

    # Post params:
    #   json submission (incomplete).
    log.debug(" " * 5 + "New Request: %s" % request.body)
    newSet = json.loads(request.body)

    newModel = metadataModel(
        username=request.session[SESSION.USERNAME],
        identifier=strip_tags(newSet['META']['label']),
        mdForm=newSet
    )

    # And now we save it to get the PK, and sync the JSON
    newModel.save()  # Save to get the ID created
    newModel.save()  # Save to resync the id to json

    return newModel.mdForm  # And... JSON out


@ensure_csrf_cookie
@sessionAuthed
@ajax_request
def updateSubmission(request):
    """
    Update a submission.  Should have enough info in it to update.

    So make sure we have a valid id, user... and do it
    """

    user = request.session[SESSION.USERNAME]
    newSet = json.loads(request.body)

    log.debug(' ' * 5 + 'newSet = %s' % newSet)

    toUpdate = metadataModel.objects.get(
        username=user,
        submissionID=newSet['META']['id']
    )

    #  Should have found just one object by user or crashed
    toUpdate.mdForm = newSet
    toUpdate.save()

    # Probably not needed
    return toUpdate.mdForm


@ensure_csrf_cookie
@sessionAuthed
@ajax_request
def finalizeSubmission(request):
    """
    finalize a submission.  It becomes immutable

    So make sure we have a valid id, user... and do it
    """

    user = request.session[SESSION.USERNAME]
    dataID = json.loads(request.body)['id']

    toFinal = metadataModel.objects.get(
        username=user,
        submissionID=int(dataID)
    )

    toFinal.finalize()

    # Probably not needed
    return True


# Djangoized angular app template.  We will need to write form handlers below
@ensure_csrf_cookie
def metadataIdx(request):
    """
    NG app root essentially.
    """

    log.info('Generating NG-App Template')
    reply = render(
        request,
        os.path.join(
            os.path.dirname(__file__), 'templates', 'app.html'
        ),
        #  Sooner or later I'll probably want some context in this...
        {
            'context1': 'a',
        }
    )

    if SESSION.AUTHENTICATED not in request.session:
        util.deAuth(request, reply)

    return reply


@csrf_protect
@ajax_request
def signout(request):
    result = HttpResponse(
        True,
        content_type='application/json'
    )
    util.deAuth(request, result)
    return result


@csrf_protect
@ajax_request
def revalidate(request):
    """
    Recheck the state of our authorized cookie and update if needed
    """

    if (SESSION.AUTHENTICATED not in request.session) or \
            (not request.session[SESSION.AUTHENTICATED]):
        unset = HttpResponse(False, content_type='application/json')
        util.deAuth(
            request,
            unset
        )
        return unset

    # Otherwise it's there, we're auth
    reset = HttpResponse(True, content_type='application/json')
    util.setAuthSvcCookies(reset, request.session[SESSION.USERNAME], True)
    return reset



@sensitive_post_parameters()
@csrf_protect
@never_cache
@ajax_request
def authDrupal(request):
    """
    Authorize user, set log in cookie

    Returns json response, but we don't use the decorator so we can munge the
    httpresponse cookie
    """
    log.info('Authentication attempt')

    success = False   # Is the user authorized

    if request.method == "POST":
        submitted = json.loads(request.body)
        log.debug(' ' * 5 + 'Posted : %s' % str(submitted))

        # Strip out any extras
        PAYLOAD = {
            "username": submitted['username'],
            "password": submitted['password']
        }

        toRet = None

        #  Proxy up
        if util.validateLogin(**PAYLOAD):
            # Just makes sure basic params are there
            log.info(' ' * 5 + 'Valid form submitted')
            # Proxy D7
            success, drupalResponse = util.remoteAuthenticate(**PAYLOAD)
            if success:
                log.info(' ' * 5 + 'User Authenticated')
                soup = BeautifulSoup(drupalResponse.text)
                name = soup.title.text.split('|')[0].strip()
                log.info(' ' * 5 + 'Grabbed name: %s' % name)
                toRet = {
                    'status': True,
                    'msg': 'Welcome, %s' % strip_tags(name)
                }
            else:
                log.info(' ' * 5 + 'User Failed to Authenticate')
                # Can we relay the server msg ?  No, the drupal site has no
                # messaging and just sends me right back to /user/login
                toRet = {
                    'status': False,
                    'msg': 'Authentication failure for %s' %
                    strip_tags(submitted['username'])
                }

            result = HttpResponse(
                json.dumps(toRet),
                content_type='application/json'
            )

            if success:
                util.authUser(request, result, PAYLOAD['username'])
            else:
                # Don't sign in and muck if you already are.
                util.deAuth(request, result)

            return result

        else:
            # Exception should have already happened.
            raise
    else:
        log.error(' ' * 5 + 'By GET')
        raise Exception('this should only be posted to.')
