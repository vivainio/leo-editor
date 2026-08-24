#@+leo-ver=cub-1-thin
#@0 [ekr.20210911052754.1] @f ../unittests/core/test_leoExternalFiles.py
"""Tests of leoExternalFiles.py"""

from unittest import mock

from leo.core import leoGlobals as g
from leo.core import leoApp, leoExternalFiles
from leo.core.leoTest2 import LeoUnitTest


#@+others
#@> class TestExternalFiles (LeoUnitTest)
class TestExternalFiles(LeoUnitTest):
    #@+others
    #@> TestExternalFiles.setUp
    def setUp(self):
        """setUp for TestFind class"""
        super().setUp()
        c = self.c
        g.app.idleTimeManager = leoApp.IdleTimeManager()
        g.app.idleTimeManager.start()
        g.app.externalFilesController = leoExternalFiles.ExternalFilesController(c=c)

    #@ TestExternalFiles.test_on_idle
    def test_on_idle(self):
        """
        A minimal test of the on_idle and all its helpers.

        More detail tests would be difficult.
        """
        efc = g.app.externalFilesController
        for i in range(100):
            efc.on_idle()

    #@ TestExternalFiles.test_open_file_in_external_editor_uses_argv_on_posix
    def test_open_file_in_external_editor_uses_argv_on_posix(self):
        """The subprocess.Popen branch must not pass a shell-style string on posix."""
        c = self.c
        efc = g.app.externalFilesController
        calls = []

        def fake_popen(args):
            calls.append(args)

        d = {
            'kind': 'subprocess.Popen',
            'args': ['"/usr/bin/editor"'],
            'ext': None,
        }
        fn = '/tmp/example file.md'
        with mock.patch.object(g, 'unitTesting', False):
            with mock.patch.object(leoExternalFiles.os, 'name', 'posix'):
                with mock.patch.object(leoExternalFiles.subprocess, 'Popen', fake_popen):
                    command = efc.open_file_in_external_editor(c, d, fn)
        expected = [
            '/usr/bin/editor',
            '/tmp/example file.md',
        ]
        assert calls == [expected]
        assert command == f"subprocess.Popen({expected})"

    #@-others


#@-others
#@-leo
