# -*- coding: utf-8 -*-

"""
customLogger.py
   custom dictLogger for use in settings because it was getting way too
   big to be managing in the settings file...

   This file is basically an extension of settings.py

   (from EPHT CL)

RCS Info:
   $Id: customLogger.py 2218 2013-10-29 15:11:22Z jbrown $

   Last Revised    :  $Date: 2013-10-01 12:18:55 -0600 (Tue, 01 Oct 2013) $
   By              :  $Author: jbrown $
   Rev             :  $Rev: 2218 $

"""

# pylint -- name convention
#pylint: disable-msg=C0103
# pylint -- undefined variables.  Ignore while running on desktop
#pylint: disable-msg=E0602


#####    Imports    #####
from os import path
from colorlog import ColoredFormatter

import re

##### Rel Imports   #####

##### Configuration #####
ansi_escape = re.compile(r'\x1b[^m]*m')

# Recreate, cannot circular import from settings (careful about moving this
# file)
PROJECT_DIR = path.abspath(path.dirname(__file__))

# port of django logger w/ enhancement

#################################################
#      Private Functions
#################################################


#------------------------------------------------------------------------
def _ansiStrip(text):
    """
    Given a string, flush ANSI codes from it.
    """
    regex = ansi_escape
    # Gratuitous, but we need it in scope and I'm not using  a global
    return regex.sub('', text)
#------------------------------------------------------------------------


#------------------------------------------------------------------------
def _getLogString(extraParams='', stripAnsi=False):
    """
    Return an interpolable log string.  There may be extra format parameters
    that we wish to apply before the message...

    extraParams: (string)
       Python log module interpolated parameters to be appended to our defaults
    """

    default = [
        "%(log_color)s%(levelname)s%(reset)s",
        "-(%(name)s)- ",
        "[%(asctime)s]- %(module)s:%(lineno)d-",
        "%(extra)s" % {'extra': extraParams},  # prunable
        "%(log_color)s %(message)s%(reset)s"
    ]

    # Blow out the color codes we just made if we need to
    if stripAnsi:
        default = [_ansiStrip(i) for i in default]

    # Purge empty extra if needed
    logStr = [i for i in default if i]

    return ''.join(logStr)
#------------------------------------------------------------------------


#------------------------------------------------------------------------
def getLogDictSchema(stripColors=False):
    """
    @see http://docs.python.org/2/library/logging.config.html#logging-config-dictschema
    """

    configDS = {
        'version': 1,  # only valid version @ present
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            }
        },
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
            'verbose': {
                '()': 'colorlog.ColoredFormatter',
                'format': _getLogString(stripAnsi=stripColors)
            },
            'hardcore': {
                # thread debug
                '()': 'colorlog.ColoredFormatter',
                'format': _getLogString(
                    " %(cyan)s[pid:%(process)d td:%(thread)d]%(reset)s-",
                    stripAnsi=stripColors
                )
            }
        },
        'handlers': {
            'mail_admins': {
                # only available on debug false
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'badLog': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'hardcore',
                'filename': path.join(PROJECT_DIR, 'CRASH_LOGS', 'crash.log'),
                'when': 'D',  # daily
                'interval': 1,  # 1/day
                'backupCount': 0,  # forever
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',  # stderr
                'formatter': 'verbose'
            },
            'null': {
                # throw it out
                'level': 'DEBUG',
                'class': 'django.utils.log.NullHandler',
            }
        },
        'loggers': {
            # in any module of app, call getlogger(__name__)
            'nmepscor-data-collection-form': {
                'handlers': ['console'],
                'propagate': True,
                'level': 'DEBUG'
            },
            'mdform': {
                'handlers': ['console'],
                'propagate': True,
                #'level': 'WARN'
                'level': 'DEBUG'
            },
            'builder': {
                'handlers': ['console'],
                'propagate': True,
                #'level': 'WARN'
                'level': 'DEBUG'
            },
            # django only logs msg
            'django.request': {
                'handlers': ['badLog'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }
    return configDS
#------------------------------------------------------------------------
