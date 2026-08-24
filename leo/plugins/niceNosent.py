#@+leo-ver=cub-1-thin
#@0 [ekr.20040331151007] @f ../plugins/niceNosent.py
#@+<< docstring >>
#@> << docstring >>
"""Ensures that all descendants of @file-nosent nodes end
with exactly one newline, replaces all tabs with spaces, and
adds a newline before class and functions in the derived file.

"""
#@-<< docstring >>

import os

from leo.core import leoGlobals as g
from leo.core.leoNodes import Position

NSPACES = ' ' * 4
nosentNodes: list[Position] = []


#@+others
#@ init
def init():
    """Return True if the plugin has loaded successfully."""
    ok = not g.unitTesting
    if ok:
        g.registerHandler("save1", onPreSave)
        g.registerHandler("save2", onPostSave)
        g.plugin_signon(__name__)
    return ok


#@ onPreSave
def onPreSave(tag=None, keywords=None):
    """Before saving an @nosent file, make sure that all nodes have a blank line at the end."""

    # global nosentNodes
    c = keywords.get('c')
    if c:
        for p in c.all_positions():
            if p.isAtNoSentinelsFileNode() and p.isDirty():
                nosentNodes.append(p.copy())
                for p2 in p.self_and_subtree():
                    s = p2.b
                    lastline = s.split('\n')[-1]
                    if lastline.strip():
                        p2.b = s + '\n'


#@ onPostSave
def onPostSave(tag=None, keywords=None):
    """After saving an @nosent file, replace all tabs with spaces."""

    global nosentNodes
    c = keywords.get('c')
    if c:
        for p in nosentNodes:
            g.red("node %s found" % p.h)
            # Use os.path.normpath to give system separators.
            fname = os.path.normpath(c.fullPath(p))  # #1914.
            f = open(fname, "r")
            lines = f.readlines()
            f.close()
            #@+<< add a newline before def or class >>
            #@> << add a newline before def or class >>
            for i, s in enumerate(lines):
                ls = s.lstrip()
                if ls.startswith(("def ", "class ")):
                    try:
                        if lines[i - 1].strip() != "":
                            lines[i] = "\n" + lines[i]
                    except IndexError:
                        pass
            #@-<< add a newline before def or class >>
            #@+<< replace tabs with spaces >>
            #@ << replace tabs with spaces >>
            s = ''.join(lines)
            fh = open(fname, "w")
            fh.write(s.replace("\t", NSPACES))
            fh.close()
            #@-<< replace tabs with spaces >>
    nosentNodes = []


#@-others
#@@language python
#@@tabwidth -4
#@-leo
