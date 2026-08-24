#@+leo-ver=cub-1-thin
#@0 [ekr.20141116100154.2] @f ../plugins/writers/dart.py
"""The @auto write code for dart."""

from leo.core import leoGlobals as g  # Required
from leo.core.leoNodes import Position
from leo.plugins.writers import basewriter


#@+others
#@> class DartWriter(BaseWriter)
class DartWriter(basewriter.BaseWriter):
    """The writer class for .dart files."""

    #@+others
    #@> dart.write
    def write(self, root: Position) -> None:
        """Write all the *descendants* of an .dart node."""
        root_level = root.level()
        for p in root.subtree():
            indent = p.level() - root_level
            self.put('%s %s' % ('*' * indent, p.h))
            for s in p.b.splitlines(False):
                if not g.isDirective(s):
                    self.put(s)
        root.setVisited()

    #@-others


#@-others
writer_dict = {
    '@auto': [],
    'class': DartWriter,
    'extensions': [
        '.dart',
    ],
}
#@@language python
#@@tabwidth -4
#@-leo
