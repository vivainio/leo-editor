#@+leo-ver=cub-1-thin
#@0 [ekr.20150514040100.1] @f ../commands/controlCommands.py
"""Leo's control commands."""

#@+<< controlCommands imports & annotations >>
#@> << controlCommands imports & annotations >>
from __future__ import annotations
from collections.abc import Callable
import shlex
import subprocess
from typing import TYPE_CHECKING
from leo.core import leoGlobals as g
from leo.commands.baseCommands import BaseEditCommandsClass

if TYPE_CHECKING:  # pragma: no cover
    from leo.core.leoCommands import Commands as Cmdr
    from leo.core.leoGui import LeoKeyEvent

#@-<< controlCommands imports & annotations >>


def cmd(name: str) -> Callable:
    """Command decorator for the ControlCommandsClass class."""
    return g.new_cmd_decorator(name, ['c', 'controlCommands'])


#@+others
#@ class ControlCommandsClass
class ControlCommandsClass(BaseEditCommandsClass):
    def __init__(self, c: Cmdr) -> None:
        """Ctor for ControlCommandsClass."""
        # pylint: disable=super-init-not-called
        self.c = c

    #@+others
    #@> executeSubprocess
    def executeSubprocess(self, event: LeoKeyEvent | None, command: str) -> None:
        """Execute a command in a separate process."""
        trace = False
        k = self.c.k
        try:
            proc = subprocess.Popen(
                shlex.split(command),
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL if trace else subprocess.PIPE,
                shell=True,
            )
            out, err = proc.communicate()
            for line in g.splitLines(g.toUnicode(out)):
                g.es_print(line.rstrip())
        except Exception:
            g.es_exception()
        k.keyboardQuit()  # Inits vim mode too.
        g.es(f"Done: {command}")

    #@ print plugins info...
    @cmd('show-plugin-handlers')
    def printPluginHandlers(self, event: LeoKeyEvent | None = None) -> None:
        """Print the handlers for each plugin."""
        g.app.pluginsController.printHandlers(self.c)

    def printPlugins(self, event: LeoKeyEvent | None = None) -> None:
        """
        Print the file name responsible for loading a plugin.

        This is the first .leo file containing an @enabled-plugins node
        that enables the plugin.
        """
        g.app.pluginsController.printPlugins(self.c)

    @cmd('show-plugins-info')
    def printPluginsInfo(self, event: LeoKeyEvent | None = None) -> None:
        """
        Print the file name responsible for loading a plugin.

        This is the first .leo file containing an @enabled-plugins node
        that enables the plugin.
        """
        g.app.pluginsController.printPluginsInfo(self.c)

    #@ setSilentMode
    @cmd('set-silent-mode')
    def setSilentMode(self, event: LeoKeyEvent | None = None) -> None:
        """
        Set the mode to be run silently, without the minibuffer.
        The only use for this command is to put the following in an @mode node::

            --> set-silent-mode
        """
        self.c.k.silentMode = True

    #@ shellCommand (improved)
    @cmd('shell-command')
    def shellCommand(self, event: LeoKeyEvent | None = None) -> None:
        """Execute a shell command."""
        k = self.c.k
        k.setLabelBlue('shell-command: ')
        k.get1Arg(event, self.shellCommand1)

    def shellCommand1(self, event: LeoKeyEvent | None = None) -> None:
        k = self.c.k
        if command := g.toUnicode(k.arg):
            self.executeSubprocess(event, command)

    #@ shellCommandOnRegion
    @cmd('shell-command-on-region')
    def shellCommandOnRegion(self, event: LeoKeyEvent | None = None) -> None:
        """Execute a command taken from the selected text in a separate process."""
        c = self.c
        k = c.k
        w = event.w if event else c.frame.body.wrapper
        if g.isTextWrapper(w):
            if w.hasSelection():
                command = w.getSelectedText()
                self.executeSubprocess(event, command)
            else:
                g.es('No text selected')
        k.keyboardQuit()

    #@ actOnNode
    @cmd('act-on-node')
    def actOnNode(self, event: LeoKeyEvent | None = None) -> None:
        """
        Executes node-specific action, typically defined in a plugins as
        follows::

            import leo.core.leoPlugins

            def act_print_upcase(c: Cmdr, p: Position, event: LeoKeyEvent | None = None) -> None:
                if not p.h.startswith('@up'):
                    raise leo.core.leoPlugins.TryNext
                p.h = p.h.upper()

            g.act_on_node.add(act_print_upcase)

        This will upcase the headline when it starts with ``@up``.
        """
        g.act_on_node(self.c, self.c.p, event)

    #@ shutdown, saveBuffersKillEmacs & setShutdownHook
    @cmd('save-buffers-kill-leo')
    def shutdown(self, event: LeoKeyEvent | None = None) -> None:
        """Quit Leo, prompting to save any unsaved files first."""
        g.app.onQuit(event)  # PR #4773: Bug fix.

    saveBuffersKillLeo = shutdown

    #@ suspend & iconifyFrame
    @cmd('suspend')
    def suspend(self, event: LeoKeyEvent | None = None) -> None:
        """Minimize the present Leo window."""
        self.c.frame.top.iconify()

    @cmd('iconify-frame')
    def iconifyFrame(self, event: LeoKeyEvent | None = None) -> None:
        """Minimize the present Leo window."""
        self.suspend(event)

    #@-others


#@-others
#@-leo
