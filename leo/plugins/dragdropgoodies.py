#@+leo-ver=cub-1-thin
#@0 [ville.20110115234843.8742] @f ../plugins/dragdropgoodies.py
#@+<< docstring >>
#@> << docstring >>
"""A plugin containing utils relating to drag and drop."""

#@-<< docstring >>
#@+<< imports >>
#@ << imports >>
from leo.core import leoGlobals as g

#
# Fail fast, right after all imports.
g.assertUi('qt')  # May raise g.UiTypeException, caught by the plugins manager.
#@-<< imports >>


#@+others
#@ init
def init():
    ok = g.app.gui.guiName() == "qt"
    if ok:
        if (
            0
        ):  # Use this if you want to create the commander class before the frame is fully created.
            g.registerHandler('before-create-leo-frame', onCreate)
        else:  # Use this if you want to create the commander class after the frame is fully created.
            g.registerHandler('after-create-leo-frame', onCreate)

        g.registerHandler('outlinedrop', onDrop)
        g.plugin_signon(__name__)
    return ok


#@ onDrop
def onDrop(tag, keys):
    print("ta", tag)
    ev = keys['dropevent']
    formats = keys['formats']
    md = ev.mimeData()

    mime_data_dump(md)

    print("fo", formats)

    return False


#@ mimeDataDump
def mime_data_dump(md):
    for fo in md.formats():
        da = str(md.data(fo))
        print("FO", fo)
        print(da)
        print("END")


#@ onCreate
def onCreate(tag, keys):
    c = keys.get('c')
    if c:
        pluginController(c)


#@ class pluginController
class pluginController:
    #@+others
    #@> __init__
    def __init__(self, c):
        pass

    #@-others


#@-others
#@@language python
#@@tabwidth -4
#@-leo
