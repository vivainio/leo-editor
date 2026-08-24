#@+leo-ver=cub-1-thin
#@0 [edream.110203113231.741] @f ../plugins/add_directives.py
"""Allows users to define new @directives."""

from leo.core import leoGlobals as g

directives = ("markup",)  # A tuple with one string.


#@+others
#@> init
def init():
    """Return True if the plugin has loaded successfully."""
    g.registerHandler("start1", addPluginDirectives)
    return True


#@ addPluginDirectives
def addPluginDirectives(tag, keywords):
    """Add all new directives to g.globalDirectiveList"""

    # global directives

    for s in directives:
        if s.startswith('@'):
            s = s[1:]
        if s not in g.globalDirectiveList:
            g.globalDirectiveList.append(s)


#@-others
#@@language python
#@@tabwidth -4
#@-leo
