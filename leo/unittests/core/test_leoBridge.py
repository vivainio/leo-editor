#@+leo-ver=cub-1-thin
#@0 [ekr.20210903153138.1] @f ../unittests/core/test_leoBridge.py
"""Tests of leoBridge.py"""

import os
from leo.core import leoBridge
from leo.core.leoTest2 import LeoUnitTest


#@+others
#@> class TestBridge(LeoUnitTest)
class TestBridge(LeoUnitTest):
    """Test cases for leoBridge.py"""

    #@+others
    #@> TestBridge.test_bridge
    def test_bridge(self):
        # The most basic test.
        controller = leoBridge.controller(
            gui='nullGui',  # 'nullGui', 'qt'
            loadPlugins=False,  # True: attempt to load plugins.,
            readSettings=False,  # True: read standard settings files.
            silent=True,  # True: don't print signon messages.
            verbose=True,
        )
        g = controller.globals()
        self.assertTrue(g)
        unittest_dir = os.path.abspath(os.path.dirname(__file__))
        self.assertTrue(os.path.exists(unittest_dir))
        test_dot_leo = g.finalize_join(unittest_dir, '..', '..', 'test', 'test.leo')
        self.assertTrue(os.path.exists(test_dot_leo), msg=test_dot_leo)
        c = controller.openLeoFile(test_dot_leo)
        self.assertTrue(c)

    #@-others


#@-others
#@-leo
