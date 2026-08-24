#@+leo-ver=cub-1-thin
#@0 [ville.20091009202416.10040] @f ../plugins/leoremote.py
#@+<< docstring >>
#@-<< docstring >>
#@+<< imports >>
#@-<< imports >>
#@+others
#@> << docstring >> (leoremote.py)
"""Remote control for Leo.

    NOTE: as of 2015-07-29 the http://localhostL:8130/_/exec/ mode of
    the mod_http plug-in is intended to replace this module's functionality.

    2016/12/23: Use g.exec_file, so this module *might* work with Python 3.

    Executing the leoserve-start command will cause Leo to to listen on a local
    socket for commands from other processes.

Example client::

    from leo.external import lproto
    import os

    addr = open(os.path.expanduser('~/.leo/leoserv_sockname')).read()
    print("will connect to",addr)
    pc  = lproto.LProtoClient(addr)
    pc.send(\"""
        g.es("hello world from remote")
        c = g.app.commanders()[0]
    \""")

    # note how c persists between calls
    pc.send('''c.doCommandByName('stickynote')''')

"""

#@ << imports >> (leoremote.py)
import os
import socket  # For a test of its capabilities.
import tempfile
from typing import Any
from leo.external import lproto
from leo.core import leoGlobals as g


#@ init
def init():
    """Return True if the plugin has loaded successfully."""
    ok = True
    if ok:
        g.plugin_signon(__name__)
    # serve_thread()
    # g.app.remoteserver = ss = LeoSocketServer()
    return ok


#@ g.command('leoserv-start')
@g.command('leoserv-start')
def leoserv_start(event):
    # c = event['c']
    g.app.leoserv = lps = lproto.LProtoServer()

    def dispatch_script(msg, ses):
        # print("leoremote.py: dispatch script", msg)
        fd, pth = tempfile.mkstemp(suffix='.py')
        f = os.fdopen(fd, "w")
        f.write(msg)
        f.close()
        # first run
        if 'pydict' not in ses:
            ses['pydict'] = {'g': g}
        # print("run file",pth)
        d = ses['pydict']
        g.exec_file(pth, d)
        # print("run done")

    lps.set_receiver(dispatch_script)
    # EKR: 2011/10/12
    uniqid: Any
    if hasattr(socket, 'AF_UNIX'):
        uniqid = 'leoserv-%d' % os.getpid()
    else:
        uniqid = '172.16.0.0', 1
    lps.listen(uniqid)
    fullpath = lps.srv.fullServerName()
    socket_file = os.path.expanduser('~/.leo/leoserv_sockname')
    open(socket_file, 'w').write(fullpath)
    print('leoremote.py: file:   %s' % socket_file)
    print('leoremote.py: server: %s' % fullpath)


#@ script execution
def run_remote_script(fname):
    # c and p are ambiguous for remote script
    print("rrs")
    d = {'g': g}
    g.exec_file(fname, d)


#@-others
#@@language python
#@@tabwidth -4
#@-leo
