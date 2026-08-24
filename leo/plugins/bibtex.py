#@+leo-ver=cub-1-thin
#@0 [timo.20050213160555] @f ../plugins/bibtex.py
#@+<< docstring >>
#@> << docstring >>
#@@nocolor-node
#@@wrap
r"""Creates a BibTex file from an  '@bibtex <filename>' tree.

Nodes of the form '@<x> key' create entries in the file.

When the user creates a new node (presses enter in headline text) the plugin
automatically inserts a template for the entry in the body pane.

The 'templates' dict in the <\< globals >\> section defines the template. The
default, the template creates all required entries.

Double-clicking the @bibtex node writes the file. For example, the following
outline::

    -@bibtex biblio.bib
     +@book key,
      author = {A. Uthor},
      year = 1999

creates the following 'biblio.bib' file::

    @book{key,
    author = {A. Uthor},
    year= 1999}

@string nodes define strings and may contain multiple entries. The plugin writes
 all @string nodes at the start of the file. For example, the following
 outline::

    -@bibtext biblio.bib
     +@string
      j1 = {Journal1}
     +@article AUj1
      author = {A. Uthor},
      journal = j1
     +@string
      j2 = {Journal2}
      j3 = {Journal3}

creates the following file::

    @string{j1 = {Journal1}}
    @string{j2 = {Journal2}}
    @string{j3 = {Journal3}}

    @article{AUj1,
    author = {A. Uthor},
    journal = j1}

Headlines that do not start with '@' are organizer nodes: the plugin does not
write organizer nodes, but does write descendant nodes.

BibTeX files can be imported by creating an empty node with '@bibtex filename'
in the headline. Double-clicking it will read the file and parse it into a
@bibtex tree. No syntax checks are made: the file is expected to be a valid
BibTeX file.

"""

#@-<< docstring >>
from leo.core import leoGlobals as g

# By Timo Honkasalo: contributed under the same license as Leo.py itself.
# 2017/02/23: Rewritten by EKR
#@+<< define templates dict>>
#@-<< define templates dict>>
entrytypes = list(templates.keys())
entrytypes.append('@string')


#@+<< to do >>
#@-<< to do >>
#@+others
#@ init (bibtex.py)
def init():
    """Return True if the plugin has loaded successfully."""
    ok = not g.unitTesting
    if ok:
        # Register the handlers...
        g.registerHandler("headdclick1", onIconDoubleClick)
        g.registerHandler("headkey2", onHeadKey)
        g.plugin_signon(__name__)
    return ok


#@ onHeadKey
def onHeadKey(tag, keywords):
    """
    Write template for the entry in body pane.

    If body pane is empty, get template for the entry from a dictionary
    'templates ' and write it in the body pane.

    20141127 - note headkey2 now only fires on `Enter`, no need
    to check which key brought us here.
    """
    # c = keywords.get("c")
    # To do: check for duplicate keys here.
    p = keywords.get("p")
    if not p:
        return
    h = p.h.strip()
    i = h.find(' ')
    kind = h[:i]
    if kind in templates.keys() and not p.b.strip():
        # Fix bug 142: plugin overwrites body text.
        # Iterate on p2, not p!
        for p2 in p.parents():
            if p2.h.startswith('@bibtex ') and not p.b.strip():
                # write template, but only for new nodes.
                p.b = templates.get(kind)
                # c.frame.body.wrapper.setInsertPoint(16)
                return


#@ onIconDoubleClick
#
# this does not check for proper filename syntax.
# path is the current dir, or the place @folder points to
# this should probably be changed to @path or so.


def onIconDoubleClick(tag, keywords):
    """
    Read or write a bibtex file when the node is double-clicked.

    Write the @bibtex tree as bibtex file when the root node is double-clicked.
    If it has no child nodes, read bibtex file.
    """
    p = keywords.get("p") or keywords.get("v")
    c = keywords.get("c")
    if not c or not p:
        return
    h = p.h.strip()
    if g.match_word(h, 0, "@bibtex"):
        base = g.os_path_dirname(c.fileName() or '')
        fn = g.finalize_join(base, h[8:])
        if p.hasChildren():
            writeTreeAsBibTex(c, fn, p)
        else:
            readBibTexFileIntoTree(c, fn, p)


#@ readBibTexFileIntoTree
def readBibTexFileIntoTree(c, fn, p):
    """Import a BibTeX file into a @bibtex tree."""
    root = p.copy()
    g.es('reading:', fn)
    s, _e = g.readFileIntoString(fn)
    if s is None:
        return
    aList: list[tuple] = []  # A list of tuples (h, b).
    strings: list[str] = []
    entries: list[tuple] = []
    s = '\n' + ''.join([z.lstrip() for z in g.splitLines(s)])
    for line in s.split('\n@')[1:]:
        kind, rest = line[:6], line[7:].strip()
        if kind == 'string':
            strings.append(rest[:-1] + '\n')
        else:
            i = min(line.find(','), line.find('\n'))
            h = '@' + line[:i]
            h = h.replace('{', ' ').replace('(', ' ').replace('\n', '')
            b = line[i + 1 :].rstrip().lstrip('\n')[:-1]
            entries.append(
                (h, b),
            )
    if strings:
        h, b = '@string', ''.join(strings)
        aList.append(
            (h, b),
        )
    aList.extend(entries)
    for h, b in aList:
        p = root.insertAsLastChild()
        p.b, p.h = b, h
    root.expand()
    c.redraw()


#@ writeTreeAsBibTex
def writeTreeAsBibTex(c, fn, root):
    """Write root's *subtree* to bibFile."""
    strings, entries = [], []
    for p in root.subtree():
        h = p.h
        if h.lower() == '@string':
            strings.extend(
                [('@string{%s}\n\n' % z.rstrip()) for z in g.splitLines(p.b) if z.strip()]
            )
        else:
            i = h.find(' ')
            kind, rest = h[:i].lower(), h[i + 1 :].rstrip()
            if kind in entrytypes:
                entries.append('%s{%s,\n%s}\n\n' % (kind, rest, p.b.rstrip()))
    if strings or entries:
        g.es('writing:', fn)
        encoding = c.getEncoding(root)
        with open(fn, 'wb') as f:
            s = ''.join(strings + entries)
            f.write(g.toEncodedString(s, encoding=encoding))


#@-others
#@@language python
#@@tabwidth -4
#@-leo
