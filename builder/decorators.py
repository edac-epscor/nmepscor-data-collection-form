from functools import wraps
from django.core.exceptions import PermissionDenied

from util import SESSION

import logging
log = logging.getLogger(__name__)


def sessionAuthed(func):
    """
    Check if the users session is permitted
    """

    @wraps(func)
    def wrapper(request, *args, **kwargs):

        if SESSION.AUTHENTICATED in request.session:
            if request.session[SESSION.AUTHENTICATED]:
                return func(request, *args, **kwargs)
            else:
                # They has a session, but not auth
                log.warn("Unauthorized session denied")
                raise PermissionDenied
        else:
            # No session, not allowed
            log.warn("Sessionless request denied")
            raise PermissionDenied

    return wrapper
