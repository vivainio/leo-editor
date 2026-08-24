#@+leo-ver=cub-1-thin
#@0 [ekr.20040915073259.1] @f ../plugins/maximizeNewWindows.py
"""Maximizes all new windows."""

# Original written by Jaakko Kourula.
# Edited by EKR.

#@+<< imports >>
#@> << imports >>
from leo.core import leoGlobals as g
from leo.core import leoPlugins

#@-<< imports >>


#@+others
#@ init
def init():
    """Return True if the plugin has loaded successfully."""
    leoPlugins.registerHandler("after-create-leo-frame", maximize_window)
    g.plugin_signon(__name__)
    return True


#@ maximize_window
def maximize_window(tag, keywords):
    c = keywords.get('c')

    if c and c.exists and c.frame and not c.frame.isNullFrame:
        gui = g.app.gui.guiName()
        if gui == 'qt':
            c.frame.top.showMaximized()


#@-others
#@@language python
#@@tabwidth -4
#@-leo
