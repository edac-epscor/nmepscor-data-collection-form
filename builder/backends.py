"""
Okay, settings.AUTHENTICATION_BACKENDS is a fail-open system, checking each and
every backend.  So, we can't reject and have another backend with a default
password created or we would have written a backdoor.

"""

##### IMPORTS       #####

# Platform
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

##### REL IMPORTS   #####

import util  # Remote auth

import logging
log = logging.getLogger(__name__)


# Remote authentication to EPSCoR server as django.auth module
#   Had something unusual going on when extending ModelBackend, so choosing to
#   encapsulate instead
class DualAuthBackend:
    """
    EPSCoR auth backend.  We first check the remote backend that we implement,
    then cascade into modelbackend -- but reject all default passwords to avoid
    having a default.

    Encapsulates modelbackend when remote fails
    """

    # Create an authentication method
    # This is called by the standard Django login procedure
    def authenticate(self, **kwargs):
        log.info("Authenticating: %(username)s" % kwargs)
        try:
            user = RemoteDrupalBackend().authenticate(**kwargs)
            if user is None:
                log.info("Remote Auth Rejected, trying local user list: %(username)s" % kwargs)
                # Then... Remote failed, try local model
                #return super(DualAuthBackend, self).authenticate(self,
                #    **kwargs)
                return ModelBackend().authenticate(**kwargs)
            else:
                #  Remote succeeded, but we're still cautious and refuse
                #  this one password out of abundance of prudence
                log.info(" " * 5 + "Remote Auth Accepted: %(username)s" %
                        kwargs)
                return user
        except PermissionDenied:
            log.warn(" " * 5 +
                 "Full Abort after remote Auth for user: %(username)s" % kwargs)
            raise  # abort abort abort!
        except:
            raise
            log.warn(" " * 5 +
                "Other error in remote Auth for user: %(username)s" % kwargs)
            return None

    # We don't need this method, since it'll fall through anyway.  But I may
    # wish to change it later...
    def get_user(self, user_id):
        return ModelBackend().get_user(user_id)


class RemoteDrupalBackend:
    """
    Remote Drupal auth backend.  If valid, setup
    """

    def authenticate(self, **kwargs):
        """
        kwargs requires username, password
        """
        username = kwargs['username']
        log.info("Remotely Drupal Authenticating: %s" % username)
        try:
            # Basic...input sanity check
            if not util.validateLogin(**kwargs):
                log.info(" " * 5 + "invalid args")
                return None

            # Check if user is authentic remote
            # /Real brunt of work
            goodPass, response = util.remoteAuthenticate(**kwargs)

            if not goodPass:
                log.info(" " * 5 + "rejected password")
                return None

        except:
            log.warn("Unknown error in remote drupal authentication")
            return None

        log.info("Remotely Drupal Success for: %s" % username)
        try:
            # Check if the user exists in Django's local database
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            log.info("Creating first time user: %s" % username)
            # Create a user in Django's local database
            #
            # We...*could* hash their real pw to speed things up, but I don't
            #  want a copy.  Also -- there is an email field, but we don't
            #  have a reset password form and won't/can't (it's epscors p/w)
            user = User.objects.create_user(
                username=username,
                email=None,  # Get later
                password=None,  # set_unusable_password called
            )

            # Scrape once, if they don't like or have it set there, they can
            # change it here later.
            profile = util.nameFromAuthenticLoginResponse(response)
            user.first_name = profile['first']
            user.last_name = profile['last']
            user.save()

        log.info(" " * 5 + "success!")
        return user

    # Stock from auth.backends
    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
