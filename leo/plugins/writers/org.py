#@+leo-ver=cub-1-thin
#@0 [ekr.20140726091031.18079] @f ../plugins/writers/org.py
"""The @auto write code for Emacs org-mode (.org) files."""

from collections.abc import Callable
from leo.core import leoGlobals as g  # Required.
from leo.core.leoCommands import Commands as Cmdr
from leo.core.leoNodes import Position
from leo.plugins.writers import basewriter


#@+others
#@> class OrgModeWriter(BaseWriter)
class OrgModeWriter(basewriter.BaseWriter):
    """The writer class for .org files."""

    def __init__(self, c: Cmdr) -> None:
        super().__init__(c)
        self.tc = self.load_nodetags()

    #@+others
    #@> orgw.load_nodetags
    def load_nodetags(self) -> Callable | None:
        """
        Load the nodetags.py plugin if necessary.
        Return c.theTagController.
        """
        c = self.c
        if not getattr(c, 'theTagController', None):
            g.app.pluginsController.loadOnePlugin('nodetags.py', verbose=False)
        return getattr(c, 'theTagController', None)

    #@ orgw.write
    def write(self, root: Position) -> None:
        """Write all the *descendants* of an @auto-org-mode node."""
        root_level = root.level()
        self.write_root(root)
        for p in root.subtree():
            if g.app.force_at_auto_sentinels:  # pragma: no cover
                self.put_node_sentinel(p, '#')
            indent = p.level() - root_level
            self.put('%s %s' % ('*' * indent, p.h))
            for s in p.b.splitlines(False):
                self.put(s)
        root.setVisited()

    #@ orgw.write_root
    def write_root(self, root: Position) -> None:
        """Write the root @auto-org node."""
        lines = [z for z in g.splitLines(root.b) if not g.isDirective(z)]
        for s in lines:
            self.put(s)

    #@-others


#@-others
writer_dict = {
    '@auto': [
        '@auto-org-mode',
        '@auto-org',
    ],
    'class': OrgModeWriter,
    'extensions': [
        '.org',
    ],
}
#@@language python
#@@tabwidth -4
#@-leo
