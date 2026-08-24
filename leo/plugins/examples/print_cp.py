#@+leo-ver=cub-1-thin
#@0 [ekr.20060621123339] @f ../plugins/examples/print_cp.py
"""
A plugin showing how to convert an @button node to a plugin.

This plugin registers the 'print-cp' minibuffer command.
"""

from leo.core import leoGlobals as g


#@+others
#@> init
def init():
    """Return True if the plugin has loaded successfully."""
    if g.app.gui is None:
        g.app.createQtGui(__file__)
    ok = g.app.gui.guiName().startswith('qt')
    if ok:
        # g.registerHandler('after-create-leo-frame',onCreate)
        g.registerHandler(('new', 'open2'), onCreate)
    return ok


#@ onCreate
def onCreate(tag, keys):
    c = keys.get('c')
    if c:
        pluginController(c)


#@ class pluginController
class pluginController:
    #@+others
    #@> __init__ (pluginController, print_cp.py)
    def __init__(self, c):
        self.c = c
        c.k.registerCommand('print-cp', self.print_cp)
        script = "c.doCommandByName('print-cp')"
        g.app.gui.makeScriptButton(c, script=script, buttonText='Print c & p', bg='red')

    #@ print_cp
    def print_cp(self, event=None):
        c = self.c
        p = c.p
        g.red('c: %s' % (c.fileName()))
        g.red('p: %s' % (p.h))

    #@-others


#@-others
#@-leo
