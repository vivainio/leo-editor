#@+leo-ver=cub-1-thin
#@0 [ekr.20210902055206.1] @f ../unittests/core/test_leoRst.py
"""Tests of leoRst.py"""

try:
    import docutils
except Exception:  # pragma: no cover
    docutils = None
from leo.core import leoRst  # Required for coverage tests.
from leo.core.leoTest2 import LeoUnitTest

assert leoRst


#@+others
#@> class TestRst (LeoUnitTest)
class TestRst(LeoUnitTest):
    """A class to run rst-related unit tests."""

    def setUp(self):
        super().setUp()
        if not docutils:
            self.skipTest('Requires docutils')  # pragma: no cover

    #@+others
    #@> TestRst.test_at_no_head
    def test_at_no_head(self):
        c = self.c
        rc = c.rstCommands
        # Create the *input* tree.
        root = c.rootPosition().insertAfter()
        root.h = fn = '@rst test.html'
        child = root.insertAsLastChild()
        child.h = '@rst-no-head section'
        # Insert the body texts.  Overindent to eliminate @verbatim sentinels.
        root.b = self.prep(
            """
            #####
            Title
            #####

            This is test.html
        """
        )

        child.b = """This is the body of the section.\n"""

        # Define the expected output.
        expected = (
            self.prep(
                f"""
            .. rst3: filename: {fn}

            .. _http-node-marker-1:

            #####
            Title
            #####

            This is test.html

            This is the body of the section.
        """
            )
            + '\n'
        )  # Required.
        # Get and check the rst result.
        rc.nodeNumber = 0
        rc.http_server_support = True  # Override setting for testing.
        source = rc.write_rst_tree(root, fn)
        self.assertEqual(source, expected)
        # Get the html from docutils.
        html = rc.writeToDocutils(source, ext='.html')
        # Don't bother testing the html. It will depend on docutils.
        assert html and html.startswith('<?xml') and html.strip().endswith('</html>')

    #@ TestRst.test_handleMissingStyleSheetArgs
    def test_handleMissingStyleSheetArgs(self):
        c = self.c
        x = c.rstCommands
        result = x.handleMissingStyleSheetArgs(s=None)
        self.assertEqual(result, {})
        expected = {
            'documentoptions': '[english,12pt,lettersize]',
            'language': 'ca',
            'use-latex-toc': '1',
        }
        for s in (
            '--language=ca, --use-latex-toc,--documentoptions=[english,12pt,lettersize]',
            '--documentoptions=[english,12pt,lettersize],--language=ca, --use-latex-toc',
            '--use-latex-toc,--documentoptions=[english,12pt,lettersize],--language=ca, ',
        ):
            result = x.handleMissingStyleSheetArgs(s=s)
            self.assertEqual(result, expected)

    #@ TestRst.test_unicode_characters
    def test_unicode_characters(self):
        c = self.c
        rc = c.rstCommands
        # Create the *input* tree.
        root = c.rootPosition().insertAfter()
        root.h = fn = '@rst unicode_test.html'
        # Insert the body text.  Overindent to eliminate @verbatim sentinels.
        root.b = self.prep(
            """
            Test of unicode characters: ÀǋϢﻙ

            End of test.
        """
        )

        # Define the expected output.
        expected = (
            self.prep(
                f"""
            .. rst3: filename: {fn}

            .. _http-node-marker-1:

            Test of unicode characters: ÀǋϢﻙ

            End of test.
        """
            )
            + '\n'
        )  # Required.

        # Get and check the rst result.
        rc.nodeNumber = 0
        rc.http_server_support = True  # Override setting for testing.
        source = rc.write_rst_tree(root, fn)
        self.assertEqual(source, expected)
        # Get the html from docutils.
        html = rc.writeToDocutils(source, ext='.html')
        # Don't bother testing the html. It will depend on docutils.
        assert html and html.startswith('<?xml') and html.strip().endswith('</html>')

    #@ TestRst.write_logic
    def test_write_to_docutils(self):
        c = self.c
        rc = c.rstCommands
        # Create the *input* tree.
        root = c.rootPosition().insertAfter()
        root.h = fn = '@rst test.html'
        child = root.insertAsLastChild()
        child.h = 'section'
        # Insert the body texts.  Overindent to eliminate @verbatim sentinels.
        root.b = self.prep(
            """
    #@@language rest

            #####
            Title
            #####

            This is test.html
        """
        )
        child.b = self.prep(
            """
            @ This is a doc part
            it has two lines.
    #@@c
            This is the body of the section.
        """
        )
        # Define the expected output.
        expected = (
            self.prep(
                f"""
            .. rst3: filename: {fn}

            .. _http-node-marker-1:

    #@@language rest

            #####
            Title
            #####

            This is test.html

            .. _http-node-marker-2:

            section
            +++++++

            @ This is a doc part
            it has two lines.
    #@@c
            This is the body of the section.
        """
            )
            + '\n'
        )  # Required.

        # Get and check the rst result.
        rc.nodeNumber = 0
        rc.http_server_support = True  # Override setting for testing.
        source = rc.write_rst_tree(root, fn)
        self.assertEqual(source, expected)
        # Get the html from docutils.
        html = rc.writeToDocutils(source, ext='.html')
        # Don't bother testing the html. It will depend on docutils.
        assert html and html.startswith('<?xml') and html.strip().endswith('</html>')

    #@-others


#@-others
#@-leo
