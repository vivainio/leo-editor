#@+leo-ver=cub-1-thin
#@0 [ekr.20250329033400.1] @f leoAPI.py
"""
Abstract base classes and Protocol classes for Leo's gui.
"""

#@+<< leoAPI.py: imports and annotations >>
#@> << leoAPI.py: imports and annotations >>
from __future__ import annotations
from typing import TYPE_CHECKING
from leo.core import leoGlobals as g
from leo.plugins.qt_text import QTextMixin

if TYPE_CHECKING:
    from leo.core.leoCommands import Commands as Cmdr
#@-<< leoAPI.py: imports and annotations >>


#@+others
#@ class StringTextWrapper(QTextMixin)
class StringTextWrapper(QTextMixin):
    """A class that represents Leo's body pane as a Python string."""

    #@+others
    #@> StringTextWrapper.__init__, __repr__ & getName
    def __init__(self, c: Cmdr | None, name: str) -> None:
        """Ctor for the StringTextWrapper class."""
        super().__init__(c)
        self.c = c
        self.name = name
        self.ins = 0
        self.sel = 0, 0
        self.s = ''
        self.virtualInsertPoint = 0
        self.widget = None  # This ivar must exist, and be None.

    def __repr__(self) -> str:
        return f"<StringTextWrapper: {id(self)} {self.name}>"

    def getName(self) -> str:
        """StringTextWrapper."""
        return self.name or ''  # Essential.

    #@ StringTextWrapper: Clipboard
    def clipboard_clear(self) -> None:
        g.app.gui.replaceClipboardWith('')

    def clipboard_append(self, s: str) -> None:
        s1 = g.app.gui.getTextFromClipboard()
        g.app.gui.replaceClipboardWith(s1 + s)

    #@ StringTextWrapper: Do-nothings
    # For StringTextWrapper.

    def disable(self) -> None:
        pass

    def enable(self, enabled: bool = True) -> None:
        pass

    def flashCharacter(
        self,
        i: int,
        bg: str = 'white',
        fg: str = 'red',
        flashes: int = 3,
        delay: int = 75,
    ) -> None:
        pass

    def getXScrollPosition(self) -> int:
        return 0

    def getYScrollPosition(self) -> int:
        return 0

    def see(self, i: int) -> None:
        pass

    def seeInsertPoint(self) -> None:
        pass

    def setFocus(self) -> None:
        pass

    def setStyleClass(self, name: str) -> None:
        pass

    def setXScrollPosition(self, i: int) -> None:
        pass

    def setYScrollPosition(self, i: int) -> None:
        pass

    #@ StringTextWrapper: Text
    #@> StringTextWrapper.appendText
    def appendText(self, s: str) -> None:
        """StringTextWrapper."""
        self.s = self.s + g.toUnicode(s)  # defensive
        self.ins = len(self.s)
        self.sel = self.ins, self.ins

    #@ StringTextWrapper.delete
    def delete(self, i: int, j: int | None = None) -> None:
        """StringTextWrapper."""
        if j is None:
            j = i + 1
        # This allows subclasses to use this base class method.
        if i > j:
            i, j = j, i
        s = self.getAllText()
        self.setAllText(s[:i] + s[j:])
        # Bug fix: 2011/11/13: Significant in external tests.
        self.setSelectionRange(i, i, insert=i)

    #@ StringTextWrapper.deleteTextSelection
    def deleteTextSelection(self) -> None:
        """StringTextWrapper."""
        i, j = self.getSelectionRange()
        self.delete(i, j)

    #@ StringTextWrapper.get
    def get(self, i: int, j: int | None = None) -> str:
        """StringTextWrapper."""
        if j is None:
            j = i + 1
        s = self.s[i:j]
        return g.toUnicode(s)

    #@ StringTextWrapper.getAllText
    def getAllText(self) -> str:
        """StringTextWrapper."""
        s = self.s
        return g.checkUnicode(s)

    #@ StringTextWrapper.getInsertPoint
    def getInsertPoint(self) -> int:
        """StringTextWrapper."""
        i = self.ins
        if i is None:
            if self.virtualInsertPoint is None:
                i = 0
            else:
                i = self.virtualInsertPoint
        self.virtualInsertPoint = i
        return i

    #@ StringTextWrapper.getLastIndex
    def getLastIndex(self) -> int:
        """Return the length of the self.s"""
        return len(self.s)

    #@ StringTextWrapper.getSelectedText
    def getSelectedText(self) -> str:
        """StringTextWrapper."""
        i, j = self.sel
        s = self.s[i:j]
        return g.checkUnicode(s)

    #@ StringTextWrapper.getSelectionRange
    def getSelectionRange(self, sort: bool = True) -> tuple[int, int]:
        """Return the selected range of the widget."""
        sel = self.sel

        # Check if sel contains None values (can be set by leoFind.py's 'save' and 'restore' methods).
        if len(sel) == 2 and (sel[0] is None or sel[1] is None):
            return 0, 0

        if len(sel) == 2 and sel[0] >= 0 and sel[1] >= 0:
            i, j = sel
            if sort and i > j:
                sel = j, i  # Bug fix: 10/5/07
            return sel
        i = self.ins
        return i, i

    #@ StringTextWrapper.hasSelection
    def hasSelection(self) -> bool:
        """StringTextWrapper."""
        i, j = self.getSelectionRange()
        return i != j

    #@ StringTextWrapper.insert
    def insert(self, i: int, s: str) -> int:
        """StringTextWrapper."""
        self.s = self.s[:i] + s + self.s[i:]
        i += len(s)
        self.ins = i
        self.sel = i, i
        return i  # PR #4812

    #@ StringTextWrapper.selectAllText
    def selectAllText(self, insert: int | None = None) -> None:
        """StringTextWrapper."""
        self.setSelectionRange(0, len(self.s), insert=insert)

    #@ StringTextWrapper.setAllText
    def setAllText(self, s: str) -> None:
        """StringTextWrapper."""
        self.s = s
        i = len(self.s)
        self.ins = i
        self.sel = i, i

    #@ StringTextWrapper.setInsertPoint
    def setInsertPoint(self, i: int, s: str | None = None) -> None:
        """StringTextWrapper."""
        self.virtualInsertPoint = i
        self.ins = i
        self.sel = i, i

    #@ StringTextWrapper.setSelectionRange
    def setSelectionRange(self, i: int, j: int, insert: int | None = None) -> None:
        """StringTextWrapper."""
        # Note: leoFind.py may set those to None. See its 'save' and 'restore' methods.
        self.sel = i, j
        self.ins = j if insert is None else insert

    #@ StringTextWrapper.toPythonIndexRowCol
    def toPythonIndexRowCol(self, index: int) -> tuple[int, int]:
        """StringTextWrapper."""
        s = self.getAllText()
        row, col = g.convertPythonIndexToRowCol(s, index)
        return row, col

    #@-others


#@-others
#@@language python
#@@tabwidth -4
#@@pagewidth 60
#@-leo
