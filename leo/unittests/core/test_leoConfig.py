#@+leo-ver=cub-1-thin
#@0 [ekr.20210910073303.1] @f ../unittests/core/test_leoConfig.py
"""Tests of leoConfig.py"""

from leo.core import leoGlobals as g
from leo.core.leoTest2 import LeoUnitTest


#@+others
#@> class TestConfig(LeoUnitTest)
class TestConfig(LeoUnitTest):
    """Test cases for leoConfig.py"""

    #@+others
    #@> TestConfig.test_g_app_config_and_c_config
    def test_g_app_config_and_c_config(self):
        c = self.c
        assert g.app.config
        assert c.config

    #@ TestConfig.test_c_config_printSettings
    def test_c_config_printSettings(self):
        c = self.c
        c.config.printSettings()

    #@-others


#@-others
#@-leo
