#@+leo-ver=cub-1-thin
#@0 [ekr.20121126095734.12418] @f ../plugins/threadutil.py
#@@language python
#@@tabwidth -4
from collections import deque
import logging
import sys
import time
import traceback
from typing import Any
from leo.core import leoGlobals as g
from leo.core.leoQt import QtCore, QtWidgets

# Fail fast, right after all imports.
g.assertUi('qt')  # May raise g.UiTypeException, caught by the plugins manager.
log = None


#@+others
#@>  top-level
#@> async_syscmd
def async_syscmd(cmd, onfinished):
    proc = QtCore.QProcess()

    def cmd_handler(exitstatus):
        out = proc.readAllStandardOutput()
        err = proc.readAllStandardError()
        onfinished(exitstatus, out, err)

    proc.finished.connect(cmd_handler)
    proc.start(cmd)


#@ enq_task
def enq_task(r):
    _tq.add(r)


#@ init
def init():
    """Return True if the plugin has loaded successfully."""
    g.procs = SysProcessRunner()
    g.procs.default_cb = leo_echo_cb
    return True


#@ later
def later(f):
    QtCore.QTimer.singleShot(0, f)


#@ leo_echo_cb
def leo_echo_cb(out, err, code, ent):
    arg = ent['arg']
    g.es("> " + arg[0] + " " + repr(arg[1:]))
    if out:
        g.es(out)
    if err:
        g.es_error(err)


#@ log_filedes
garbage: list[Any] = []


def log_filedes(f, level):
    def reader():
        line = f.readline()
        if not line:
            raise StopIteration
        return line

    def output(line):
        if log:
            log.log(level, line.rstrip())

    def finished():
        if log:
            log.log(logging.INFO, "<EOF>")

    rr = Repeater(reader)
    rr.fragment.connect(output)
    rr.finished.connect(finished)
    garbage.append(rr)
    rr.start()


#@ main
def main():
    # stupid test
    a = QtWidgets.QApplication([])
    b = QtWidgets.QPushButton("Say hello", None)
    g.procs.add(['ls', '/tmp'])
    g.procs.add(['ls', '-la'])
    b.show()
    a.exec()


#@< class NowOrLater
class NowOrLater:
    #@+others
    #@> NowOrLater.__init__
    def __init__(self, worker, gran=1.0):
        """worker takes list of tasks, does something for it"""

        self.w = worker
        self.l = []
        self.lasttime = 1.0
        self.granularity = gran
        self.scheduled = False

    #@ NowOrLater.add
    def add(self, task):
        now = time.time()
        self.l.append(task)
        # if last called one sec ago, call now

        def callit():
            try:
                self.lasttime = time.time()
                work = self.l
                self.l = []
                self.w(work)
            except Exception:
                typ, val, tb = sys.exc_info()
                print('')
                print('threadutil.py: unexpected exception in NowOrLater.callit')
                print('')
                # Like g.es_exception()
                lines = traceback.format_exception(typ, val, tb)
                for line in lines:
                    print(line.rstrip())
            finally:
                self.scheduled = False

        if (now - self.lasttime) > self.granularity:
            callit()
        else:
            if not self.scheduled:
                QtCore.QTimer.singleShot(int(self.granularity * 1000), callit)  # #2402
                self.scheduled = True
            else:
                pass

    #@-others


#@< class Repeater
class Repeater(QtCore.QThread):
    """execute f forever, signal on every run"""

    fragment = QtCore.pyqtSignal(object)

    #@+others
    #@> __init__
    def __init__(self, f, parent=None):
        super().__init__(parent)
        self.f = f

    #@ run
    def run(self):
        while 1:
            try:
                res = self.f()
            except StopIteration:
                return
            except Exception:
                typ, val, tb = sys.exc_info()
                print('')
                print('threadutil.py: unexpected exception in Repeater.run')
                print('')
                # Like g.es_exception()
                lines = traceback.format_exception(typ, val, tb)
                for line in lines:
                    print(line.rstrip())
                return
            self.fragment.emit(res)

    #@-others


#@< class RRunner
class RRunner(QtCore.QThread):
    #@+others
    #@> __init__
    def __init__(self, f, parent=None):
        super().__init__(parent)
        self.f = f

    #@ run
    def run(self):
        try:
            self.res = self.f()
        except Exception:
            typ, val, tb = sys.exc_info()
            print('')
            print('threadutil.py: unexpected exception in RRunner.run')
            print('')
            # Like g.es_exception()
            lines = traceback.format_exception(typ, val, tb)
            for line in lines:
                print(line.rstrip())

    #@-others


#@< class SysProcessRunner
class SysProcessRunner:
    def __init__(self):
        # dict of lists (queues)
        self.q = {}
        self.cur = {}
        self.default_cb = None

    def add(self, argv, key="", cb=None):
        """argv = [program, arg1, ...]"""
        ent = {'arg': argv, 'cb': cb}
        self.q.setdefault(key, deque()).append(ent)
        self.sched()

    def sched(self):
        for k, q in self.q.items():
            if q and k not in self.cur:
                ent = q.popleft()
                self.cur[k] = ent
                self.run_one(ent, k)

    def run_one(self, ent, key):
        p = ent['proc'] = QtCore.QProcess()

        def fini(code, status):
            del self.cur[key]
            out = str(p.readAllStandardOutput())
            err = str(p.readAllStandardError())
            cb = ent['cb'] or self.default_cb
            later(self.sched)
            if cb:
                cb(out, err, status, ent)

        cmd = ent['arg'][0]
        args = ent['arg'][1:]
        p.start(cmd, args)
        p.finished.connect(fini)


#@ class ThreadQueue
class ThreadQueue:
    #@+others
    #@> __init__
    def __init__(self):
        """Ctor for ThreadQueue class."""
        self.threads = []

    #@ add
    def add(self, r):
        empty = not self.threads
        self.threads.append(r)
        r.finished.connect(self.pop)
        if empty:
            r.start()

    #@ pop
    def pop(self):
        if self.threads:
            ne = self.threads.pop()
            ne.start()

    #@-others


#@< class UnitWorker
class UnitWorker(QtCore.QThread):
    """Work on one work item at a time, start new one when it's done"""

    resultReady = QtCore.pyqtSignal()

    #@+others
    #@> __init__
    def __init__(self):
        super().__init__()
        self.cond = QtCore.QWaitCondition()
        self.mutex = QtCore.QMutex()
        self.input = None

    #@ set_worker
    def set_worker(self, f):
        self.worker = f

    #@ set_output_f
    def set_output_f(self, f):
        self.output_f = f

    #@ set_input
    def set_input(self, inp):
        self.input = inp
        self.cond.wakeAll()

    #@ do_work
    def do_work(self, inp):
        try:
            self.output = self.worker(inp)
        except Exception:
            typ, val, tb = sys.exc_info()
            print('')
            print('threadutil.py: unexpected exception in UnitWorker.do_work.')
            print('')
            # Like g.es_exception()
            lines = traceback.format_exception(typ, val, tb)
            for line in lines:
                print(line.rstrip())
            self.output = ''

        self.resultReady.emit()

        def L():
            self.output_f(self.output)

        later(L)

    #@ run
    def run(self):
        m = self.mutex
        while 1:
            m.lock()
            self.cond.wait(m)
            inp = self.input
            self.input = None
            m.unlock()
            if inp is not None:
                self.do_work(inp)

    #@-others


#@-others
_tq = ThreadQueue()
init()
if __name__ == "__main__":
    main()
#@-leo
