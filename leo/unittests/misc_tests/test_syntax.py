#@+leo-ver=cub-1-thin
#@0 [ekr.20210901140718.1] @f ../unittests/misc_tests/test_syntax.py
"""Syntax tests, including a check that Leo will continue to load!"""

import glob

from leo.core import leoGlobals as g
from leo.core.leoTest2 import LeoUnitTest


#@+others
#@> class TestSyntax(LeoUnitTest)
class TestSyntax(LeoUnitTest):
    """Unit tests checking syntax of Leo files."""

    #@+others
    #@> TestSyntax.tests...
    #@> TestSyntax.check_syntax
    def check_syntax(self, fileName, s):
        """Called by a unit test to check the syntax of a file."""
        try:
            s = s.replace('\r', '')
            tree = compile(s + '\n', fileName, 'exec')
            del tree  # #1454: Suppress -Wd ResourceWarning.
            return True
        except SyntaxError:  # pragma: no cover
            raise SyntaxError(fileName)  # pylint: disable=raise-missing-from
        except Exception:  # pragma: no cover
            g.trace("unexpected error in:", fileName)
            raise

    #@ TestSyntax.test_syntax_of_all_files
    def test_syntax_of_all_files(self):
        skip_tuples = (
            ('extensions', 'asciidoc.py'),
            ('test', 'scriptFile.py'),
            ('test', 'beautify_node.py'),
        )
        join = g.finalize_join
        skip_list = [join(g.app.loadDir, '..', a, b) for a, b in skip_tuples]
        n = 0
        for theDir in (
            'core',
            'external',
            'extensions',
            'modes',
            'plugins',
            'scripts',
            'test',
        ):
            path = g.finalize_join(g.app.loadDir, '..', theDir)
            self.assertTrue(g.os_path_exists(path), msg=path)
            aList = glob.glob(g.os_path_join(path, '*.py'))
            if g.isWindows:
                aList = [z.replace('\\', '/') for z in aList]
            for z in aList:
                if z not in skip_list:
                    n += 1
                    fn = g.shortFileName(z)
                    s, e = g.readFileIntoString(z)
                    self.assertTrue(self.check_syntax(fn, s or ''), msg=fn)

    #@-others


#@-others
#@-leo
