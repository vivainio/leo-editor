#@+leo-ver=cub-1-thin
#@0 [ville.20120503224623.3574] @f ../plugins/leomylyn.py
"""Provides an experience like Mylyn:http://en.wikipedia.org/wiki/Mylyn for Leo.

It "scores" the nodes based on how interesting they probably are for you,
allowing you to focus on your "working set".

Scoring is based on how much you edit the nodes.

"""

# By VMV.
from leo.core import leoGlobals as g


#@+others
#@> init
def init():
    """Return True if the plugin has loaded successfully."""
    ok = g.app.gui.guiName() == "qt"
    g.plugin_signon(__name__)
    g._mylyn = ctr = MylynController()
    ctr.set_handlers()
    return ok


#@ class MylynController
class MylynController:
    #@+others
    #@> __init__
    def __init__(self):
        self.scoring = {}

    #@ add_score
    def add_score(self, v, points):
        cur = self.scoring.get(v, 0)
        cur += points
        self.scoring[v] = cur

    #@ children_hnd
    def children_hnd(self, tag, kw):
        print(tag, kw)
        ns = kw["nodes"]
        for v in ns:
            self.add_score(v, 100)

    #@ content_hnd
    def content_hnd(self, tag, kw):
        print(tag, kw)
        ns = kw["nodes"]
        for v in ns:
            self.add_score(v, 1)

    #@ set_handlers (leomylyn.py)
    def set_handlers(self):
        g.registerHandler("childrenModified", self.children_hnd)
        g.registerHandler("contentModified", self.content_hnd)

        @g.command("mylyn-scores")
        def mylyn_scores_f(*a):
            for k, v in self.scoring.items():
                g.es(str(k) + " " + str(v))

    #@-others


#@-others
#@@language python
#@@tabwidth -4
#@-leo
