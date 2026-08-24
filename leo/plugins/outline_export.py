#@+leo-ver=cub-1-thin
#@0 [edream.110203113231.720] @f ../plugins/outline_export.py
"""Modifies the way exported outlines are written."""

#@@language python
#@@tabwidth -4

from leo.core import leoGlobals as g


#@+others
#@> init
def init():
    """Return True if the plugin has loaded successfully."""
    ok = not g.unitTesting  # Not for unit testing: modifies core class.
    if ok:
        g.registerHandler("start2", onStart)
        g.plugin_signon(__name__)
    return ok


#@ newMoreHead
# Returns the headline string in MORE format.


def newMoreHead(self, firstLevel, useVerticalBar=True):
    useVerticalBar = True  # Force the vertical bar

    v = self
    level = self.level() - firstLevel
    if level > 0:
        if useVerticalBar:
            s = " |\t" * level
        else:
            s = "\t"
    else:
        s = ""
    s += "+ " if v.hasChildren() else "- "
    s += v.h
    return s


#@ onStart
def onStart(tag, keywords):
    from leo.core import leoNodes

    g.funcToMethod(newMoreHead, leoNodes.VNode, "moreHead")


#@-others
#@-leo
