#@+leo-ver=cub-1-thin
#@0 [ekr.20101110093301.5818] @f ../plugins/mod_framesize.py
"""Sets a hardcoded frame size.

Prevents Leo from setting custom frame size (e.g. from an external .leo
document)

"""


#@@language python
#@@tabwidth -4
#@+others
#@> init
def init():
    """Return True if the plugin has loaded successfully."""
    from leo.core import leoGlobals as g
    from leo.plugins import qt_frame

    ok = g.app.gui.guiName() == "qt"
    if ok:
        qt_frame.LeoQtFrame.setTopGeometry = setTopGeometry_mod_framesize  # type:ignore
        g.plugin_signon(__name__)
    return ok


#@ setTopGeometry_mod_framesize
def setTopGeometry_mod_framesize(self, *args):
    """Monkeypatced version of setTopGeometry"""

    self.top.resize(1000, 700)


#@-others
#@-leo
