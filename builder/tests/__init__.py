import doctest
import unittest

# doctests
# unit tests...

from dualauth import *


#-----------------------------------------------------------------------
def addModuleToSuite(ste, mod):
    """
    Side effect on suite, returned also
    """
    ste.addTests(unittest.TestLoader().loadTestsFromModule(mod))
    return ste
#-----------------------------------------------------------------------


#-----------------------------------------------------------------------
def addDocToSuite(ste, mod):
    """
    Side effect on suite, returned also
    """
    ste.addTests(doctest.DocTestSuite(mod))
#-----------------------------------------------------------------------


#-----------------------------------------------------------------------
def unitSuite():
    suite = unittest.TestSuite()
    addModuleToSuite(suite, dualauth)
    return suite
#-----------------------------------------------------------------------


#-----------------------------------------------------------------------
def docTSuite():
    suite = unittest.TestSuite()
    # No doctests written yet
    return suite
#-----------------------------------------------------------------------


#-----------------------------------------------------------------------
def suite():
    suite = unittest.TestSuite()
    suite.addTests(unitSuite())
    return suite
#-----------------------------------------------------------------------
