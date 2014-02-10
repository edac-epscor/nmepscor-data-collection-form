#   Utility functions

from django.conf import settings
from django import forms
import requests

import logging
log = logging.getLogger(__name__)

from django.utils import formats
import pytz


########################################
#   CONSTANTS
########################################
# enumish/constantish.  Reserving words in session both internal and cookies.
class SESSION(object):
    USERNAME = 'username'
    AUTHENTICATED = 'authenticated'


#  As above, different strings to keep incompatible (defensive code) in case
#  these are ever accidentally crossed
class COOKIE(object):
    USERNAME = 'c_username'
    AUTHENTICATED = 'c_authenticated'

DENVER = pytz.timezone('America/Denver')

########################################
#   Utility Methods
########################################


def validateLogin(**kwargs):
    """
    TODO: rewrite as form processor with JSON

    username
    password

    If form is valid, return True.  Otherwise bubble exception
    """

    uname = kwargs['username']
    pw = kwargs['password']
    VE = forms.ValidationError

    if len(uname) < 5:
        raise VE('Invalid User Name')

    if len(pw) < 5:
        raise VE('Invalid Password')

    log.info(' ' * 5 + 'Good login args')
    return True


def remoteAuthenticate(**kwargs):
    """
    Contact the EPSCoR server and see if our params work there...

    @PARAMS:  (kwargs/PAYLOAD, username, password
    @RETURNS tuple:
        success  (Bool)
        response (requests.Response)
    """

    URL = 'http://%s/user/login' % settings.SECRET_EPSCOR_SERVER
    PAYLOAD = {
        'name': kwargs['username'],
        'pass': kwargs['password'],
        'form_id': 'user_login'  # stupid drupal
    }  # no chance of ever sending epscor server other params

    response = requests.post(URL, data=PAYLOAD, timeout=5.0)  # 2s

    #invalidLogin = forms.ValidationError(
    #    AuthenticationForm.error_messages['invalid_login'],
    #    code='invalid_login'
    #)

    #  If we come back without a history/302
    if len(response.history) == 0:
        # Drupal sends me a 302
        return False, response

    # Paranoia... if we come back to where we restarted
    if response.url == URL:
        return False, response

    # Paranoia...
    if response.url.split('/')[-1] == 'login':
        # If we come back to /login, period
        return False, response

    #  If we get a 302 otherwise....
    if response.history[0].status_code == 302:
        # good sign, redirect...
        #
        #soup = BeautifulSoup(response.text)
        #  2x check response.url
        return True, response

    else:
        log.error('Unknown authentication failure')
        return False, response


def setAuthSvcCookies(response, username='', auth=False):
    """
    Set cookies for angular auth svc to use.

    Because we're setting cookies, that the browser can change, this is really
    just a hint to the client about what it can do.  We still have to actually
    check our own internal session on every request, and the auth svc itself is
    corruptible.
    """

    response.set_signed_cookie(
        COOKIE.USERNAME,
        username,
        max_age=24 * 60 * 60  # 1 day
    )

    response.set_signed_cookie(
        COOKIE.AUTHENTICATED,
        auth,
        max_age=24 * 60 * 60  # 1 day
    )


def authUser(request, response, username):
    """
    Indicate a username is authenticated

    @param (HttpRequest)
    @param (HttpResponse)
    @param (str) username
    """

    setAuthSvcCookies(response, username, True)
    request.session[SESSION.USERNAME] = username
    request.session[SESSION.AUTHENTICATED] = True


def deAuth(request, response):
    setAuthSvcCookies(response, '', False)
    request.session[SESSION.USERNAME] = ''
    request.session[SESSION.AUTHENTICATED] = False


def datetime2Human(dt):
    """
    Given a datetime object out of the DB, reprize it for locale.

    Normally we would do this with django views and localization, but
    we have JSON we're generating for human consumption...
    """

    return formats.date_format(dt.astimezone(DENVER), 'DATETIME_FORMAT')
