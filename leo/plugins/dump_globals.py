#@+leo-ver=cub-1-thin
#@0 [edream.110203113231.730] @f ../plugins/dump_globals.py
"""Dumps Python globals at startup."""

from leo.core import leoGlobals as g


#@+others
#@> init
def init():
    """Return True if the plugin has loaded successfully."""
    ok = not g.unitTesting  # Not for unit testing.
    if ok:
        g.registerHandler("start2", onStart)
        g.plugin_signon(__name__)
    return ok


#@ onStart
def onStart(tag, keywords):
    g.pr("\nglobals...")
    for s in globals():
        if s not in __builtins__:
            g.pr(s)
    g.pr("\nlocals...")
    for s in locals():
        if s not in __builtins__:
            g.pr(s)


#@-others
#@@language python
#@@tabwidth -4
#@-leo
