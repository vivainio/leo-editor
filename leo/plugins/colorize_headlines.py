#@+leo-ver=cub-1-thin
#@0 [ville.20090310191936.10] @f ../plugins/colorize_headlines.py
"""Manipulates appearance of individual tree widget items. (Qt only).

This plugin is mostly an example of how to change the appearance of headlines. As
such, it does a relatively mundane chore of highlighting @thin, @auto, @shadow
nodes in bold.

"""

# By VMV.
#@+<< imports >>
#@> << imports >>
from leo.core import leoGlobals as g
from leo.core import leoPlugins  # Uses leoPlugins.TryNext.


#@-<< imports >>
#@+others
#@ init
def init():
    """Return True if the plugin has loaded successfully."""
    ok = g.app.gui.guiName() == "qt"
    if ok:
        g.visit_tree_item.add(colorize_headlines_visitor)
    return ok


#@ colorize_headlines_visitor
def colorize_headlines_visitor(c, p, item):
    """Changes @thin, @auto, @shadow to bold"""
    t = p.h.split(None, 1)
    if t and t[0] in ['@file', '@thin', '@auto', '@shadow']:
        f = item.font(0)
        f.setBold(True)
        item.setFont(0, f)
    raise leoPlugins.TryNext


#@-others
#@@language python
#@@tabwidth -4
#@-leo
