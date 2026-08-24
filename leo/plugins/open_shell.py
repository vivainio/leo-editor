#@+leo-ver=cub-1-thin
#@0 [EKR.20040517080049.4] @f ../plugins/open_shell.py
#@+<< docstring >>
#@> << docstring >>
"""
Creates an 'Extensions' menu containing two commands:
Open Console Window and Open Explorer.

The Open Console Window command opens xterm on Linux.
The Open Explorer command Opens a Windows explorer window.

This allows quick navigation to facilitate testing and navigating large systems
with complex directories.

Please submit bugs / feature requests to etaekema@earthlink.net

Current limitations:
- Not tested on Mac OS X ...
- On Linux, xterm must be in your path.

"""
#@-<< docstring >>

# Written by Ed Taekema.  Modified by EKR
import os
import subprocess
import sys
from leo.core import leoGlobals as g

# Changes these as required.
if sys.platform == "win32":
    pathToExplorer = 'c:/windows/explorer.exe'
    pathToCmd = 'c:/windows/system32/cmd.exe'
else:
    # Set these as needed...
    pathToExplorer = ''
    pathToCmd = ''


#@+others
#@ init
def init():
    """Return True if the plugin has loaded successfully."""
    # Ok for unit testing: creates a new menu.
    g.registerHandler("after-create-leo-frame", onCreate)
    g.plugin_signon(__name__)
    return True


#@ onCreate
def onCreate(tag, keywords):
    c = keywords.get('c')
    if c:
        controller = pluginController(c)
        controller.load_menu()


#@ class pluginController
class pluginController:
    #@+others
    #@> ctor
    def __init__(self, c):
        self.c = c

    #@ load_menu
    def load_menu(self):
        c = self.c
        if sys.platform == "win32":
            table = (
                ("&Open Console Window", None, self.launchCmd),
                ("Open &Explorer",       None, self.launchExplorer),
            )  # fmt: skip
        else:
            table = (
                ("Open &xterm", None, self.launchxTerm),
            )  # fmt: skip
        c.frame.menu.createNewMenu("E&xtensions", "top")
        c.frame.menu.createMenuItemsFromTable("Extensions", table)

    #@ _getpath (open_shell.py)
    def _getpath(self, p):
        c = self.c
        path = c.fullPath(p)  # #1914
        # Use os.path.normpath to give system separators.
        return os.path.normpath(g.os_path_dirname(path))  # #1914

    #@ _getCurrentNodePath
    def _getCurrentNodePath(self):
        c = self.c
        p = c.p
        d = self._getpath(p)
        return d

    #@ launchCmd
    def launchCmd(self, event=None):
        # global pathToCmd

        d = self._getCurrentNodePath()
        myCmd = 'cd ' + d
        subprocess.Popen(['/k ', myCmd], executable=pathToCmd)

    #@ launchExplorer
    def launchExplorer(self, event=None):
        # global pathToExplorer

        d = self._getCurrentNodePath()
        subprocess.Popen([' ', d], executable=pathToExplorer)

    #@ launchxTerm
    def launchxTerm(self, event=None):
        d = self._getCurrentNodePath()
        curdir = os.getcwd()
        os.chdir(d)
        subprocess.Popen(['-title Leo'], executable='xterm')
        os.chdir(curdir)

    #@-others


#@-others
#@@language python
#@@tabwidth -4

#@-leo
