#@+leo-ver=cub-1-thin
#@0 [ekr.20210904022712.2] @f ../unittests/commands/test_checkerCommands.py
"""Tests of leo.commands.leoCheckerCommands."""

from leo.core.leoTest2 import LeoUnitTest


#@+others
#@> class TestChecker(LeoUnitTest):
class TestChecker(LeoUnitTest):
    """Test cases for leoCheckerCommands.py"""

    #@+others
    #@> test_check_nodes
    def test_check_nodes(self):
        c = self.c
        from leo.commands import checkerCommands

        x = checkerCommands.CheckNodes(c)
        x.ok_head_patterns = []
        table = (
            """
                def spam():
                    pass
                def eggs():
                    pass
            """,                    # Too many defs.
            "   ",                  # Empty body.
            "\ntest\n",             # Leading blank line.
            "\n\nclass MyClass\n",  # Trailing class line.
            "\n\ndef spam():",      # Trailing def line.
        )  # fmt: skip
        p = c.rootPosition()
        for s in table:
            p.b = s
            x.get_data()
            assert x.is_dubious_node(p)

    #@-others


#@-others

#@-leo
