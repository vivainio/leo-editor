#@+leo-ver=cub-1-thin
#@0 [ekr.20140526082700.18440] @f leoRope.py
#@+<< leoRope imports >>
#@> << leoRope imports >>
import time
import importlib
from leo.core import leoGlobals as g

# Third-party imports.
try:
    from rope import refactor
    from rope.base import project, simplify

    has_rope = True
except Exception:
    has_rope = False
if has_rope:
    importlib.reload(project)
    importlib.reload(simplify)
    importlib.reload(refactor)


#@-<< leoRope imports >>
#@+others
#@ class RopeController
class RopeController:
    #@+others
    #@> ctor
    def __init__(self, c):
        self.c = c
        if has_rope:
            self.proj = project.Project(g.app.loadDir)
        else:
            self.proj = None

    #@ modules (RopeController)
    def modules(self):
        """Return full path names of all Leo modules."""
        aList = g.glob_glob(g.os_path_join(g.app.loadDir, '*.py'))
        return sorted(aList)

    #@ path
    def path(self, fn):
        return g.os_path_join(g.app.loadDir, fn)

    #@ refactor
    def refactor(self):
        """Perform refactorings."""
        proj = self.proj
        if not proj:
            g.es_print('rope not found')
            return
        m = proj.get_resource(self.path('leoAtFile.py'))
        s = m.read()
        # Important: get an offset in actual code.
        s = simplify.real_code(s)
        tag1 = 'atFile'
        tag2 = g.pep8_class_name(tag1)
        offset = s.find(tag1)
        if offset > -1:
            changes = refactor.rename.Rename(proj, m, offset).get_changes(tag2)
            g.trace(changes.get_description())
        else:
            g.trace('not found', tag1)
        # prog.do(changes)

    #@ run
    def run(self):
        """run the refactorings."""
        if proj := self.proj:
            proj.validate(proj.root)
            self.refactor()
            proj.close()
        else:
            g.es_print('rope not found')

    #@-others


#@< test
def test(c):
    g.cls()
    t1 = time.time()
    RopeController(c).run()
    print(f"done: {g.timeSince(t1)} sec.")


#@-others
#@@language python
#@@tabwidth -4
#@@pagewidth 70
#@-leo
