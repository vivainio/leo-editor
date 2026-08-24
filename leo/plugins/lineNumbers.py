#@+leo-ver=cub-1-thin
#@0 [ekr.20040419105219] @f ../plugins/lineNumbers.py
#@+<< docstring >>
#@> << docstring >>
"""Adds #line directives in perl and perlpod programs.

Over-rides two methods in leoAtFile.py to write #line directives after node
sentinels. This allows compilers to give locations of errors in relation to the
node name rather than the filename. Currently supports only perl and perlpod.
"""
#@-<< docstring >>

# Use and distribute under the same terms as Leo.
# Original code by Mark Ng <markn@cs.mu.oz.au>

#@+<< imports >>
#@ << imports >>
import re
from leo.core import leoGlobals as g
from leo.core import leoAtFile
#@-<< imports >>

linere = re.compile("^#line 1 \".*\"$")


def init():
    """Return True if the plugin has loaded successfully."""
    ok = not g.unitTesting  # Not safe for unit testing.  Changes core class.
    if ok:
        #@+<< override write methods >>
        #@-<< override write methods >>
        g.plugin_signon(__name__)
    return ok


#@-leo
