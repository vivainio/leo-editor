#@+leo-ver=cub-1-thin
#@0 [tbrown.20090513125417.5244] @f ../plugins/interact.py
#@+<< docstring >>
#@> << docstring >>
"""Adds buttons so Leo can interact with command line environments.

:20100226: see also leoscreen.py for a simpler approach.

Currently implements `bash` shell and `psql` (postresql SQL db shell).

Single-line commands can be entered in the headline with a blank body,
multi-line commands can be entered in the body with a descriptive
title in the headline.  Press the `bash` or `psql` button to send
the command to the appropriate interpreter.

The output from the command is **always** stored in a new node added
as the first child of the command node.  For multi-line commands
this new node is selected.  For single-line command this new node
is not shown, instead the body text of the command node is updated
to reflect the most recent output.  Comment delimiter magic is used
to allow single-line and multi-line commands to maintain their
single-line and multi-line flavors.

Both the new child nodes and the updated body text of single-line
commands are timestamped.

For the `bash` button the execution directory is either the directory
containing the `.leo` file, or any other path as specified by ancestor
`@path` nodes.

Currently the `psql` button just connects to the default database.  ";"
is required at the end of SQL statements.

Requires `pexpect` module.
"""
#@-<< docstring >>

#@@language python
#@@tabwidth -4

import os
import time
from typing import Any

# By Terry Brown, 2009-05-12
from leo.core import leoGlobals as g
from leo.plugins.mod_scripting import scriptingController

try:
    import pexpect
except ImportError:
    pass


#@+others
#@ init
def init():
    """Return True if the plugin has loaded successfully."""
    g.registerHandler('after-create-leo-frame', onCreate)
    g.plugin_signon(__name__)
    return True


#@ onCreate
def onCreate(tag, keywords):
    InteractController(keywords['c'])


#@ class Interact
class Interact:
    #@+others
    #@> __init__
    def __init__(self, c):
        self.c = c

    #@ available
    def available(self):
        raise NotImplementedError

    #@ run
    def run(self, p):
        raise NotImplementedError

    #@ buttonText
    def buttonText(self):
        raise NotImplementedError

    #@ statusText
    def statusText(self):
        raise NotImplementedError

    #@-others


#@< class InteractPSQL
class InteractPSQL(Interact):
    prompt = '__psql-leo__'

    #@+others
    #@> __init__
    def __init__(self, c):
        super().__init__(c)
        self.leftover: Any = None  # Hard to annotate.
        prompts = ' '.join(['--set PROMPT%d=%s' % (i, self.prompt) for i in range(1, 4)])
        prompts += ' --pset pager=off'
        self._available = True
        try:
            self.psqlLink = pexpect.spawn('psql %s' % prompts)
            self.leftover = ''
            for i in self.psqlReader(self.psqlLink):
                pass  # eat the initial output as it isn't interesting
        except pexpect.ExceptionPexpect:
            self._available = False

    #@ available
    def available(self):
        return self._available

    #@ buttonText
    def buttonText(self):
        return "psql"

    #@ statusText
    def statusText(self):
        return "send headline or body to psql session"

    #@ run
    def run(self, p):
        c = self.c
        q = p.b
        if not q.strip() or p.b.strip().startswith('--- '):
            q = p.h
        if p.h.strip().startswith('--'):
            q = None

        if q is None:
            g.es('No valid / uncommented query')
        else:
            self.psqlLink.send(q.strip() + '\n')
            ans = []
            maxlen = 100
            for d in self.psqlReader(self.psqlLink):
                if d.strip():
                    ans.append(d)
                    if len(ans) > maxlen:
                        del ans[maxlen - 10]
                        ans[maxlen - 10] = '   ... skipping ...'
            n = p.insertAsNthChild(0)
            n.h = '-- ' + time.asctime()
            n.b = '\n'.join(ans)
            if p.b.strip().startswith('--- ') or not p.b.strip():
                p.b = '-' + n.h + '\n\n' + n.b
                p.contract()
            else:
                c.selectPosition(n)
            c.redraw()

    #@ psqlReader
    def psqlReader(self, proc):
        cnt = 0
        timeout = False
        while not timeout:
            dat = []
            try:
                dat = self.leftover + proc.read_nonblocking(size=10240, timeout=1)
                self.leftover = ''
                if not dat.endswith('\n'):
                    if '\n' in dat:
                        dat, self.leftover = dat.rsplit('\n', 1)
                    else:
                        time.sleep(0.5)
                        self.leftover = dat
                        dat = None
                if dat:
                    dat = dat.split("\n")
            except pexpect.TIMEOUT:
                timeout = True

            if dat:
                for d in dat:
                    cnt += 1
                    yield d.replace(self.prompt, '# ')

    #@-others


#@< class InteractBASH
class InteractBASH(Interact):
    prompt = '__bash-leo__'

    #@+others
    #@> __init__
    def __init__(self, c):
        super().__init__(c)
        self._available = True
        self.leftover: Any = None  # Hard to annotate.
        try:
            self.bashLink = pexpect.spawn('bash -i')
            self.bashLink.setwinsize(30, 256)
            # stop bash emitting chars for long lines
            self.bashLink.send("PS1='> '\n")
            self.bashLink.send("unalias ls\n")
            self.leftover = ''
            for i in self.bashReader(self.bashLink):
                # eat the initial output as it isn't interesting
                # and in includes chrs leo can't encode currently
                pass
        except pexpect.ExceptionPexpect:
            self._available = False

    #@ buttonText
    def buttonText(self):
        return "bash"

    #@ statusText
    def statusText(self):
        return "send headline or body to bash session"

    #@ available
    def available(self):
        return self._available

    #@ run
    def run(self, p):
        c = self.c
        q = p.b
        if not q.strip() or p.b.strip().startswith('### '):
            q = p.h
        if p.h.strip().startswith('#'):
            q = None

        if q is None:
            g.es('No valid / uncommented statement')
        else:
            path = self.getPath(c, p)
            if not path:
                path = os.path.dirname(c.fileName())
            if path:
                self.bashLink.send('cd %s\n' % path)
            self.bashLink.send(q.strip() + '\n')
            ans = []
            maxlen = 100
            for d in self.bashReader(self.bashLink):
                if d.strip():
                    ans.append(d)
                    if len(ans) > maxlen:
                        del ans[maxlen - 10]
                        ans[maxlen - 10] = '   ... skipping ...'
            n = p.insertAsNthChild(0)
            n.h = '## ' + time.asctime()
            n.b = '\n'.join(ans)
            if p.b.strip().startswith('### ') or not p.b.strip():
                p.b = '#' + n.h + '\n\n' + n.b
                p.contract()
            else:
                c.selectPosition(n)
            c.redraw()

    #@ bashReader
    def bashReader(self, proc):
        cnt = 0
        timeout = False
        while not timeout:
            dat = []
            try:
                dat = self.leftover + proc.read_nonblocking(size=10240, timeout=1)
                self.leftover = ''
                if not dat.endswith('\n'):
                    if '\n' in dat:
                        dat, self.leftover = dat.rsplit('\n', 1)
                    else:
                        time.sleep(0.5)
                        self.leftover = dat
                        dat = None
                if dat:
                    dat = dat.split("\n")
            except pexpect.TIMEOUT:
                timeout = True

            if dat:
                for d in dat:
                    cnt += 1
                    yield d.replace(self.prompt, '# ')  # '%4d: %s' % (cnt,d)

    #@ getPath (interact.py)
    def getPath(self, c, p):
        for n in p.self_and_parents():
            if n.h.startswith('@path'):
                break
        else:
            return None  # must have a full fledged @path in parents

        return c.getPath(p)

    #@-others


#@< class InteractController
class InteractController:
    """quickMove binds to a controller, adds menu entries for
    creating buttons, and creates buttons as needed
    """

    #@+others
    #@> __init__

    def __init__(self, c):
        self.c = c
        self.addButton(InteractPSQL)
        self.addButton(InteractBASH)

    #@ addToFirstChildButton
    def addToFirstChildButton(self, event=None):
        self.addButton(first=True)

    #@ addToLastChildButton
    def addToLastChildButton(self, event=None):
        self.addButton(first=False)

    #@ addButton (interact.py)
    def addButton(self, first):
        """Add a button for an interact class."""
        c = self.c
        sc = scriptingController(c)
        mb = InteractButton(c, class_=first)
        if mb.available():
            sc.createIconButton(
                args=None,
                text=mb.interactor.buttonText(),
                command=mb.run,
                statusLine=mb.interactor.statusText(),
                kind='interact',
            )

    #@-others


#@< class InteractButton
class InteractButton:
    """contains target data and function for moving node"""

    #@+others
    #@> __init__

    def __init__(self, c, class_):
        self.c = c
        self.interactor = class_(c)

    #@ run
    def run(self):
        """Move the current position to the last child of self.target."""

        c = self.c
        p = c.p
        self.interactor.run(p)
        c.redraw()

    #@ available
    def available(self):
        return self.interactor.available()

    #@-others


#@-others
#@-leo
