#@+leo-ver=cub-1-thin
#@0 [ekr.20101110095202.5882] @f ../plugins/zenity_file_dialogs.py
"""Replaces the tk file dialogs on Linux with external
calls to the zenity gtk dialog package.

This plugin is more a proof of concept demo than
a useful tool.  The dialogs presented do not take
filters and starting folders can not be specified.

Despite this, some Linux users might prefer it to the
tk dialogs.

"""

import subprocess
from leo.core import leoGlobals as g
from leo.core import leoPlugins

trace = False


#@+others
#@> testForZenity
def testForZenity():
    command = ['which', 'zenity']
    o = subprocess.Popen(command, stdout=subprocess.PIPE)
    o.wait()
    o.communicate()[0].rstrip()
    ret = o.returncode
    return not ret


#@ init
def init():
    """Return True if the plugin has loaded successfully."""
    if g.unitTesting:
        return False
    ok = testForZenity()
    if ok:
        leoPlugins.registerHandler('start2', onStart2)
        g.plugin_signon(__name__)
    else:
        g.trace('failed to load zenity')
    return ok


#@ onStart2
def onStart2(tag, keywords):
    """Replace tkfile open/save method with external calls to zenity."""
    g.funcToMethod(runOpenFileDialog, g.app.gui)
    g.funcToMethod(runSaveFileDialog, g.app.gui)


#@ callZenity
def callZenity(title: str, save: bool = False, test: bool = False) -> bytes | None:
    command = ['zenity', '--file-selection', '--title=%s' % title]
    if save:
        command.append('--save')
    # if multiple:
    # command.append('--multiple')
    o = subprocess.Popen(command, stdout=subprocess.PIPE)
    o.wait()
    filename = o.communicate()[0].rstrip()
    ret = o.returncode
    if ret:
        return None
    # if multiple:
    # return filename.split('|')
    return filename


#@ runOpenFileDialog
def runOpenFileDialog(
    title,
    *,
    filetypes: list[tuple[str, str]] | None = None,
    defaultextension='',  # Not used.
):
    """Call zenity's open file(s) dialog."""
    # initialdir = g.app.globalOpenDir or g.os_path_abspath(os.getcwd())
    return callZenity(title)


#@ runSaveFileDialog
def runSaveFileDialog(
    title='',
    *,
    filetypes: list[tuple[str, str]] | None = None,
    defaultextension='',  # Not used.
) -> bytes | None:
    """Call zenity's save file dialog."""
    # initialdir=g.app.globalOpenDir or g.os_path_abspath(os.getcwd())
    return callZenity(title, save=True)


#@-others
#@@language python
#@@tabwidth -4
#@-leo
