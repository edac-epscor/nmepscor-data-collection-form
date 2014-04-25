from .default import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
COMPRESS_ENABLED = False

###########
# LOGGING #
###########

LOGGING = getLogDictSchema(stripColors=False)
