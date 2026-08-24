#@+leo-ver=cub-1-thin
#@0 [ekr.20150514040140.1] @f ../commands/keyCommands.py
"""Leo's key-handling commands."""
# This file *is* used. Do not delete it!

#@+<< keyCommands imports and abbreviations >>
#@> << keyCommands imports and abbreviations >>
from __future__ import annotations
from typing import TYPE_CHECKING
from leo.core import leoGlobals as g
from leo.commands.baseCommands import BaseEditCommandsClass

if TYPE_CHECKING:  # pragma: no cover
    from leo.core.leoGui import LeoKeyEvent
#@-<< keyCommands imports and abbreviations >>


#@+others
#@ class KeyHandlerCommandsClass
class KeyHandlerCommandsClass(BaseEditCommandsClass):
    """User commands to access the keyHandler class."""

    #@+others
    #@> menuShortcutPlaceHolder
    @g.command('menu-shortcut')
    def menuShortcutPlaceHolder(self, event: LeoKeyEvent | None = None) -> None:
        """
        This will never be called.
        A placeholder for the show-bindings command.
        """

    #@-others


#@-others
#@-leo
