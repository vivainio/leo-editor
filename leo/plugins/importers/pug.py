#@+leo-ver=cub-1-thin
#@0 [ekr.20250501.100] @f ../plugins/importers/pug.py
"""The @auto importer for Pug (HTML template language)."""

from __future__ import annotations
from typing import TYPE_CHECKING
from leo.plugins.importers.base_importer import Importer

if TYPE_CHECKING:
    from leo.core.leoCommands import Commands as Cmdr
    from leo.core.leoNodes import Position


#@+others
#@> class Pug_Importer(Importer)
class Pug_Importer(Importer):
    """A simple importer for Pug files."""

    language = 'pug'
    block_patterns: tuple = tuple()  # No block patterns: import as single node.


#@-others


def do_import(c: Cmdr, parent: Position, s: str) -> None:
    """The importer callback for pug."""
    Pug_Importer(c).import_from_string(parent, s)


importer_dict = {
    'extensions': [
        '.pug',
        '.jade',
    ],
    'func': do_import,
}
#@@language python
#@@tabwidth -4
#@-leo
