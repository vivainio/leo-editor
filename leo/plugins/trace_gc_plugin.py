#@+leo-ver=cub-1-thin
#@0 [edream.110203113231.735] @f ../plugins/trace_gc_plugin.py
"""Traces changes to Leo's objects at idle time."""

from leo.core import leoGlobals as g

g.debugGC = True  # Force debugging on.
gcCount = 0


#@+others
#@> init (trace_gc_plugin)
def init():
    """Return True if the plugin has loaded successfully."""
    ok = not g.unitTesting  # Not for unit testing.
    if ok:  # Register the handlers...
        if 1:  # Very effective.
            g.registerHandler("idle", printIdleGC)
        else:  # Very precise.
            g.registerHandler("all", printIdleGC)
        if 0:  # Another idea.
            g.registerHandler("command2", printIdleRefs)
        g.plugin_signon(__name__)
    return ok


#@ printIdleRefs
def printIdleRefs(tag, keywords):
    g.printGcRefs()


#@ printIdleGC (trace_gc_plugin)
def printIdleGC(tag, keywords):
    # Calling printGc is too expensive to do on every idle call.
    if g.app.killed:
        return
    if tag == "idle":
        global gcCount
        gcCount += 1
        if (gcCount % 20) == 0:
            g.printGc()
    else:
        g.printGc()


#@-others
#@@language python
#@@tabwidth -4
#@-leo
