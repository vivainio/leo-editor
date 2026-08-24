#@+leo-ver=cub-1-thin
#@0 [ekr.20150514154159.1] @f leoHistory.py
#@+<< leoHistory imports & annotations >>
#@> << leoHistory imports & annotations >>
from __future__ import annotations
from typing import TYPE_CHECKING
from leo.core import leoGlobals as g

if TYPE_CHECKING:  # pragma: no cover
    from leo.core.leoChapters import Chapter
    from leo.core.leoCommands import Commands as Cmdr
    from leo.core.leoNodes import Position

assert g
#@-<< leoHistory imports & annotations >>


#@+others
#@ class NodeHistory
class NodeHistory:
    """A class encapsulating knowledge of visited nodes."""

    def __init__(self, c: Cmdr) -> None:
        """Ctor for NodeHistory class."""
        self.c = c
        self.beadList: list[tuple[Position, Chapter | None]] = []
        self.beadPointer = -1
        self.skipBeadUpdate = False

    #@+others
    #@> NodeHistory.dump
    def dump(self) -> None:
        """Dump the beadList"""
        if g.unitTesting or not self.beadList:
            return
        # print(f"NodeHistory.beadList: {self.c.shortFileName()}:")
        for i, data in enumerate(self.beadList):
            p, chapter = data
            p_s = p.h if p else 'no p'
            chapter_s = f"chapter: {chapter.name} " if chapter else ''
            mark_s = '**' if i == self.beadPointer else '  '
            print(f"{mark_s} {chapter_s} {p_s}")
        print('')

    #@ NodeHistory.goNext
    def goNext(self) -> None:
        """Select the next node, if possible."""
        c = self.c
        if self.beadPointer + 1 >= len(self.beadList):
            return
        self.beadPointer += 1
        p, chapter = self.beadList[self.beadPointer]
        if c.positionExists(p):
            p, chapter = self.beadList[self.beadPointer]
            self.update(p)
            self.select(p, chapter)
        else:
            del self.beadList[self.beadPointer]
            self.beadPointer -= 1

    #@ NodeHistory.goPrev
    def goPrev(self) -> None:
        """Select the previously visited node, if possible."""
        c = self.c
        if self.beadPointer <= 0:
            return
        self.beadPointer -= 1
        p, chapter = self.beadList[self.beadPointer]
        if c.positionExists(p):
            p, chapter = self.beadList[self.beadPointer]
            self.update(p)
            self.select(p, chapter)
        else:
            del self.beadList[self.beadPointer]
            self.beadPointer += 1

    #@ NodeHistory.select
    def select(self, p: Position, chapter: Chapter | None) -> None:
        """Select p in the given chapter."""
        c, cc = self.c, self.c.chapterController
        assert c.positionExists(p), repr(p)
        oldChapter = cc.getSelectedChapter()
        if oldChapter != chapter:
            cc.selectChapterForPosition(p, chapter=chapter)
        c.selectPosition(p)  # Calls cc.selectChapterForPosition

    #@ NodeHistory.update
    def update(self, p: Position) -> None:
        """
        Update the beadList while p is being selected.
        """
        c, cc = self.c, self.c.chapterController
        if not p or not c.positionExists(p):
            return

        # Don't add @chapter nodes.
        # These are selected during the transitions to a new chapter.
        if p.h.startswith('@chapter '):
            return

        # #3800: Do nothing if p is the top of the bead list.
        last_p = self.beadList[-1][0] if self.beadList else None
        if last_p == p:
            return

        # #3800: Remove p from the bead list, adjusting the bead pointer.
        n_deleted = 0
        for z in self.beadList:
            if z[0].v == p.v:
                n_deleted += 1
        self.beadList = [z for z in self.beadList if z[0].v != p.v]
        self.beadPointer -= n_deleted

        # #3800: Insert an entry in the *middle* of the bead list, *not* at the end.
        data = (p.copy(), cc.getSelectedChapter())
        self.beadList.insert(self.beadPointer + 1, data)
        self.beadPointer += 1

    #@-others


#@-others
#@@language python
#@@tabwidth -4
#@@pagewidth 70
#@-leo
