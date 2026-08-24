#@+leo-ver=cub-1-thin
#@0 [ekr.20120420054855.14241] @f leoSessions.py
"""Support for sessions in Leo."""

from __future__ import annotations
from typing import TYPE_CHECKING
from leo.core import leoGlobals as g

if TYPE_CHECKING:  # pragma: no cover
    from leo.core.leoCommands import Commands as Cmdr
    from leo.core.leoGui import LeoKeyEvent


#@+others
#@> class SessionManager
class SessionManager:
    """A class managing session data and related commands."""

    #@+others
    #@> SessionManager.clear_session
    def clear_session(self, c: Cmdr) -> None:
        """Close all tabs except the presently selected tab."""
        for frame in g.app.windowList:
            if frame.c != c:
                frame.c.close()

    #@ SessionManager.error
    # def error (self,s):
    # # Do not use g.trace or g.es here.
    # print(s)
    #@ SessionManager.get_session
    def get_session(self) -> list[str]:
        """Return a list of UNLs for open tabs."""
        result: list[str] = []
        # Fix #1118, part 2.
        if not getattr(g.app.gui, 'frameFactory', None):
            return result
        if mf := getattr(g.app.gui.frameFactory, 'masterFrame', None):
            outlines = [mf.widget(i).leo_c for i in range(mf.count())]
        else:
            outlines = [i.c for i in g.app.windowList]
        for c in outlines:
            if c.fileName():
                unl = c.p.get_full_gnx_UNL()
                if not g.isValidUnl(unl):
                    continue
                fn = g.getUNLFilePart(unl)
                exists = fn and g.os_path_exists(fn)
                if not exists:
                    continue
                result.append(unl)
        return result

    #@ SessionManager.get_session_path
    def get_session_path(self) -> str | None:
        """Return the path to the session file."""
        for path in (g.app.homeLeoDir, g.app.homeDir):
            if g.os_path_exists(path):
                return g.finalize_join(path, 'leo.session')
        return None

    #@ SessionManager.load_session
    def load_session(self, c: Cmdr | None = None, unls: list[str] | None = None) -> None:
        """
        Open a tab for each item in UNLs & select the indicated node in each.

        unls is the list returned by SessionManager.load_snapshot()
        """
        if not unls:
            return
        unls = [z.strip() for z in unls or [] if z.strip()]
        for unl in unls:
            if not g.isValidUnl(unl):
                continue
            fn = g.getUNLFilePart(unl)
            exists = fn and g.os_path_exists(fn)
            if not exists:
                continue
            if 'startup' in g.app.debug:
                g.trace('loading session file:', fn)
            # This selects the proper position.
            g.openWithFileName(fn, gui=g.app.gui, old_c=c)

    #@ SessionManager.load_snapshot
    def load_snapshot(self) -> list[str] | None:
        """
        Load a snapshot of a session from the leo.session file.

        Return a list of unls.
        """
        try:
            session = g.app.db['session']
            if 'startup' in g.app.debug:
                g.printObj(session, tag='load_snapshot: session data')
            return session
        except KeyError:
            print('SessionManager.load_snapshot: no previous session')
        except Exception:
            g.trace('Unexpected exception in SessionManager.load_snapshot')
            g.es_exception()
        return None

    #@ SessionManager.save_snapshot
    def save_snapshot(self) -> None:
        """
        Save a snapshot of the present session to the leo.session file.

        Called automatically during shutdown.
        """
        if g.app.batchMode or g.app.inBridge or g.unitTesting:
            return
        try:
            session = self.get_session()
            if 'shutdown' in g.app.debug:
                g.printObj(session, tag='save_snapshot: session data')
            if not session:
                return  # #2433: don't save an empty session.
            g.app.db['session'] = session
        except Exception:
            g.trace('Unexpected exception in SessionManager.save_snapshot')
            g.es_exception()

    #@-others


#@< Commands (leoSession.py)
#@> session-clear
@g.command('session-clear')
def session_clear_command(event: LeoKeyEvent | None = None) -> None:
    """Close all tabs except the presently selected tab."""
    c = event.get('c') if event else None
    m = g.app.sessionManager
    if c and m:
        m.clear_session(c)


#@ session-create
@g.command('session-create')
def session_create_command(event: LeoKeyEvent | None = None) -> None:
    """Create a new @session node."""
    c = event.get('c') if event else None
    m = g.app.sessionManager
    if c and m:
        aList = m.get_session()
        p2 = c.p.insertAfter()
        p2.b = "\n".join(aList)
        p2.h = "@session"
        c.redraw()


#@ session-refresh
@g.command('session-refresh')
def session_refresh_command(event: LeoKeyEvent | None = None) -> None:
    """Refresh the current @session node."""
    c = event.get('c') if event else None
    m = g.app.sessionManager
    if c and m:
        aList = m.get_session()
        c.p.b = "\n".join(aList)
        c.redraw()


#@ session-restore
@g.command('session-restore')
def session_restore_command(event: LeoKeyEvent | None = None) -> None:
    """Open a tab for each item in the @session node & select the indicated node in each."""
    c = event.get('c') if event else None
    m = g.app.sessionManager
    if c and m:
        if c.p.h.startswith('@session'):
            aList = c.p.b.split("\n")
            m.load_session(c, aList)
        else:
            print('Please select an "@session" node')


#@ session-snapshot-load
@g.command('session-snapshot-load')
def session_snapshot_load_command(event: LeoKeyEvent | None = None) -> None:
    """Load a snapshot of a session from the leo.session file."""
    c = event.get('c') if event else None
    m = g.app.sessionManager
    if c and m:
        aList = m.load_snapshot()
        m.load_session(c, aList)


#@ session-snapshot-save
@g.command('session-snapshot-save')
def session_snapshot_save_command(event: LeoKeyEvent | None = None) -> None:
    """Save a snapshot of the present session to the leo.session file."""
    if m := g.app.sessionManager:
        m.save_snapshot()


#@-others
#@@language python
#@@tabwidth -4
#@@pagewidth 70
#@-leo
