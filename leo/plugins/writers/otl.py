#@+leo-ver=cub-1-thin
#@0 [ekr.20140726091031.18078] @f ../plugins/writers/otl.py
"""The @auto write code for vimoutline (.otl) files."""

from leo.core import leoGlobals as g
from leo.core.leoNodes import Position
from leo.plugins.writers import basewriter


#@+others
#@> class OtlWriter(BaseWriter)
class OtlWriter(basewriter.BaseWriter):
    """The writer class for .otl files."""

    #@+others
    #@> otlw.write
    def write(self, root: Position) -> None:
        """Write all the *descendants* of an @auto-otl node."""
        self.write_root(root)
        for child in root.children():
            n = child.level()
            for p in child.self_and_subtree():
                if g.app.force_at_auto_sentinels:  # pragma: no cover
                    self.put_node_sentinel(p, '#')
                indent = '\t' * (p.level() - n)
                self.put('%s%s' % (indent, p.h))
                for s in p.b.splitlines(False):
                    self.put('%s: %s' % (indent, s))
        root.setVisited()

    #@ otlw.write_root
    def write_root(self, root: Position) -> None:
        """Write the root @auto-org node."""
        lines = [z for z in g.splitLines(root.b) if not g.isDirective(z)]
        for s in lines:  # pragma: no cover (the root node usually contains no extra text).
            self.put(s)

    #@-others


#@-others
writer_dict = {
    '@auto': [
        '@auto-otl',
        '@auto-vim-outline',
    ],
    'class': OtlWriter,
    'extensions': [
        '.otl',
    ],
}
#@@language python
#@@tabwidth -4
#@-leo
