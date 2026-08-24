#! /usr/bin/env python
#@+leo-ver=cub-1-thin
#@0 [ekr.20070227091955.1] @f leoBridge.py
#@@first
"""A module to allow full access to Leo commanders from outside Leo."""

#@@language python
#@@tabwidth -4
#@+<< about the leoBridge module >>
#@> << about the leoBridge module >>
#@@language rest
# A **host** program is a Python program separate from Leo. Host programs may
# be created by Leo, but at the time they are run host programs must not be
# part of Leo in any way. So if they are run from Leo, they must be run in a
# separate process.
#
# The leoBridge module gives host programs access to all aspects of Leo,
# including all of Leo's source code, the contents of any .leo file, all
# configuration settings in .leo files, etc.
#
# Host programs will use the leoBridge module like this::
#
#     from leo.core import leoBridge
#     bridge = leoBridge.controller(gui='nullGui',verbose=False)
#     if bridge.isOpen():
#         g = bridge.globals()
#         c = bridge.openLeoFile(path)
#
# Notes:
#
# - The leoBridge module imports no modules at the top level.
#
# - leoBridge.controller creates a singleton *bridge controller* that grants
#   access to Leo's objects, including fully initialized g and c objects. In
#   particular, the g.app and g.app.gui vars are fully initialized.
#
# - By default, leoBridge.controller creates a null gui so that no Leo
#   windows appear on the screen.
#
# - As shown above, the host program should gain access to Leo's leoGlobals
#   module using bridge.globals(). The host program should not import
#   leo.core.leoGlobals as leoGlobals directly.
#
# - bridge.openLeoFile(path) returns a completely standard Leo commander.
#   Host programs can use these commanders as described in Leo's scripting
#   chapter.
#@-<< about the leoBridge module >>
#@+<< leoBridge imports & annotations >>
#@ << leoBridge imports & annotations >>
# This module must import *no* Leo modules at the outer level!
from __future__ import annotations
import os
import sys
import time
import traceback
from typing import Any, TYPE_CHECKING
from types import ModuleType

if TYPE_CHECKING:  # pragma: no cover
    from leo.core.leoCommands import Commands as Cmdr

    Args = Any
    KWargs = Any
#@-<< leoBridge imports & annotations >>

gBridgeController = None  # The singleton bridge controller.


#@+others
#@ function: controller
def controller(
    gui: str = 'nullGui',
    loadPlugins: bool = True,
    readSettings: bool = True,
    silent: bool = False,
    tracePlugins: bool = False,
    useCaches: bool = True,
    verbose: bool = False,
) -> BridgeController:
    """Create an singleton instance of a bridge controller."""
    global gBridgeController
    if not gBridgeController:
        gBridgeController = BridgeController(
            gui, loadPlugins, readSettings, silent, tracePlugins, useCaches, verbose
        )
    return gBridgeController


#@ class BridgeController
class BridgeController:
    """Creates a way for host programs to access Leo."""

    #@+others
    #@> bridge.ctor
    def __init__(
        self,
        guiName: str,
        loadPlugins: bool,
        readSettings: bool,
        silent: bool,
        tracePlugins: bool,
        useCaches: bool,
        verbose: bool,
        vs_code_flag: bool = False,  # #2098.
    ) -> None:
        """Ctor for the BridgeController class."""
        self.g: ModuleType | None = None  # leo.core.leoGlobals.
        self.guiName = guiName or 'nullGui'
        self.loadPlugins = loadPlugins
        self.readSettings = readSettings
        self.silentMode = silent
        self.tracePlugins = tracePlugins
        self.useCaches = useCaches
        self.verbose = verbose
        self.vs_code_flag = vs_code_flag  # #2098
        self.mainLoop = False  # True only if a non-null-gui mainloop is active.
        self.initLeo()

    #@ bridge.globals
    def globals(self) -> ModuleType | None:
        """Return a fully initialized leoGlobals module."""
        return self.g if self.isOpen() else None

    #@ bridge.initLeo & helpers
    def initLeo(self) -> None:
        """
        Init the Leo app to which this class gives access.
        This code is based on leo.run().
        """
        if not self.isValidPython():
            return
        t1 = time.process_time()
        #@+<< initLeo imports >>
        #@-<< initLeo imports >>
        g.app.recentFilesManager = leoApp.RecentFilesManager()
        g.app.loadManager = lm = leoApp.LoadManager()
        g.app.jupytextManager = leoJupytext.JupytextManager()
        lm.computeStandardDirectories()
        # #2519: Call sys.exit if leoID does not exist.
        g.app.setLeoID(useDialog=False, verbose=True)
        # Can be done early. Uses only g.app.loadDir & g.app.homeDir.
        lm.createAllImporterData()  # #1965.
        g.app.inBridge = True  # Support for g.getScript.
        g.app.nodeIndices = leoNodes.NodeIndices(g.app.leoID)
        g.app.config = leoConfig.GlobalConfigManager()
        if self.useCaches:
            g.app.setGlobalDb()  # #556.
        else:
            g.app.db = g.NullObject()
            g.app.global_cacher = g.NullObject()
        if self.readSettings:
            # reads only standard settings files, using a null gui.
            # uses lm.files[0] to compute the local directory
            # that might contain myLeoSettings.leo.
            lm.readGlobalSettingsFiles()
        else:
            # Bug fix: 2012/11/26: create default global settings dicts.
            settings_d, bindings_d = lm.createDefaultSettingsDicts()
            lm.globalSettingsDict = settings_d
            lm.globalBindingsDict = bindings_d
        self.createGui()  # Create the gui *before* loading plugins.
        if self.verbose:
            self.reportDirectories()
        self.adjustSysPath()
        # Kill all event handling if plugins not loaded.
        if not self.loadPlugins:

            def dummyDoHook(tag: str, *args: Args, **keys: KWargs) -> None:
                pass

            g.doHook = dummyDoHook  # type:ignore
        g.doHook("start1")  # Load plugins.
        g.app.computeSignon()
        g.app.initing = False
        g.doHook("start2", c=None, p=None, v=None, fileName=None)
        t2 = time.process_time()
        if self.verbose:
            print(f"bridge.initLeo: {t2 - t1:.2f} sec.")

    #@ bridge.isOpen
    def isOpen(self) -> bool:
        """Return True if the bridge is open."""
        g = self.g
        return bool(g and g.app and g.app.gui)

    #@ bridge.openLeoFile & helpers
    def openLeoFile(self, fileName: str | None) -> Cmdr | None:
        """Open a .leo file, or create a new Leo frame if no fileName is given."""
        g = self.g
        g.app.silentMode = self.silentMode
        useLog = False
        if not self.isOpen():
            return None
        t1 = time.process_time()
        if self.useCaches:
            self.reopen_cachers()
        else:
            g.app.db = g.NullObject()
        fileName = self.completeFileName(fileName)
        c = g.openWithFileName(fileName)  # #2489.
        if not self.useCaches:
            c.db = g.NullObject()
        # New in Leo 5.1. An alternate fix for bug #130.
        # When using a bridge Leo might open a file, modify it,
        # close it, reopen it and change it all within one second.
        # In that case, this code must properly compute the next
        # available gnx by scanning the entire outline.
        g.app.nodeIndices.compute_last_index(c)
        if useLog:
            g.app.gui.log = log = c.frame.log
            log.isNull = False
            log.enabled = True
        t2 = time.process_time()
        if self.verbose:
            print(f"bridge.open:    {t2 - t1:.2f} sec. {g.shortFileName(fileName)} ")
        return c

    #@> bridge.completeFileName
    def completeFileName(self, fileName: str | None) -> str:
        g = self.g
        if not (fileName and fileName.strip()):
            return ''
        fileName = g.finalize_join(os.getcwd(), fileName)
        head, ext = g.os_path_splitext(fileName)
        if not ext:
            fileName = fileName + ".leo"
        return fileName

    #@ bridge.reopen_cachers
    def reopen_cachers(self) -> None:
        from leo.core import leoCache

        g = self.g
        try:
            g.app.db.get('dummy')
        except Exception:
            g.app.global_cacher = leoCache.GlobalCacher()
            g.app.db = g.app.global_cacher.db

    #@-others


#@-others
#@-leo
