#@+leo-ver=cub-1-thin
#@0 [ekr.20220911163718.1] @f ../unittests/core/test_leoQt6.py
"""Tests of Qt6 methods and attributes."""

from leo.unittests.plugins.test_importers import BaseTestImporter
from leo.core import leoGlobals as g


#@+others
#@> class TestQt6(BaseTestImporter)
class TestQt6(BaseTestImporter):
    """Test cases for leoImport.py"""

    #@+others
    #@> TestQt6.test_qt6
    def test_qt6(self):
        """Test of Qt6 methods and attributes"""
        # pylint: disable=no-name-in-module
        try:
            import leo.core.leoQt6 as Qt6
        except Exception:
            self.skipTest('Requires Qt6')

        attrs = [z for z in dir(Qt6) if not z.startswith('__')]

        if 1:  # A real unit test.
            # Optional modules.
            exceptions = ('Qsci', 'QtSvg', 'QWebEngineSettings', 'WebEngineAttribute', 'uic')
            fails = [
                attr
                for attr in attrs
                if attr not in exceptions and getattr(Qt6, attr, None) is None
            ]
            self.assertFalse(fails, msg=','.join(fails))

        else:  # Inspection.

            def print_attr(attr: str) -> str:
                obj = getattr(Qt6, attr, None)
                r = repr(obj)
                return (
                    f"{attr:>25}: ***Missing***"
                    if obj is None
                    else f"{attr:>25}: module"
                    if 'module' in r
                    else f"{attr:>25}: class"
                    if 'class' in r
                    else f"{attr:>25}: enum"
                    if 'enum' in r
                    else f"{attr:>25}: {obj}"
                )

            g.printObj([print_attr(attr) for attr in attrs])

    #@-others


#@-others
#@-leo
