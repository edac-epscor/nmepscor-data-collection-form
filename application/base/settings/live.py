from .default import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

###########
# LOGGING #
###########

# fork customLogger to appropriate levels
LOGGING = getLogDictSchema(stripColors=True)

LOGGING['handlers']['console']['level'] = 'ERROR'
for log in LOGGING['loggers']:
    LOGGING['loggers'][log]['level'] = 'ERROR'
