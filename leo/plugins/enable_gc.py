#@+leo-ver=cub-1-thin
#@0 [edream.110203113231.732] @f ../plugins/enable_gc.py
"""Enables debugging and tracing for Python's garbage collector."""

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
    try:
        import gc

        gc.set_debug(gc.DEBUG_LEAK)
    except Exception:
        pass


#@-others
#@@language python
#@@tabwidth -4
#@-leo
