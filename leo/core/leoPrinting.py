#@+leo-ver=cub-1-thin
#@0 [ekr.20150419124739.1] @f leoPrinting.py
"""
Support the commands in Leo's File:Print menu.
Adapted from printing plugin.
"""

#@+<< leoPrinting imports & annotations >>
#@> << leoPrinting imports & annotations >>
from __future__ import annotations
from collections.abc import Callable
from typing import TYPE_CHECKING
from leo.core import leoGlobals as g

# Qt imports. May fail from the bridge.
try:  # #1973
    from leo.core.leoQt import printsupport, QtGui
    from leo.core.leoQt import DialogCode
except Exception:
    printsupport = QtGui = None  # type:ignore
    DialogCode = None

if TYPE_CHECKING:  # pragma: no cover
    from leo.core.leoCommands import Commands as Cmdr
    from leo.core.leoGui import LeoKeyEvent
    from leo.core.leoNodes import Position, VNode
#@-<< leoPrinting imports & annotations >>


def cmd(name: str) -> Callable:
    """Command decorator for the PrintingController class."""
    return g.new_cmd_decorator(name, ['c', 'printingController'])


#@+others
#@ class PrintingController
class PrintingController:
    """A class supporting the commands in Leo's File:Print menu."""

    #@+others
    #@> pr.__init__ & helpers
    def __init__(self, c: Cmdr) -> None:
        """Ctor for PrintingController class."""
        self.c = c
        self.reload_settings()

    def reload_settings(self) -> None:
        c = self.c
        self.font_size = c.config.getString('printing-font-size') or '12'
        self.font_family = c.config.getString('printing-font-family') or 'DejaVu Sans Mono'
        self.stylesheet = self.construct_stylesheet()

    reloadSettings = reload_settings

    #@> pr.construct stylesheet
    def construct_stylesheet(self) -> str:
        """Return the Qt stylesheet to be used for printing."""
        family, size = self.font_family, self.font_size
        table = (
            # Clearer w/o f-strings.
            f"h1 {{font-family: {family}}}",
            f"pre {{font-family: {family}; font-size: {size}pt}}",
        )
        return '\n'.join(table)

    #@< pr.Doc constructors
    #@> pr.complex document
    def complex_document(self, nodes: list[VNode], heads: bool = False) -> QtGui.QTextDocument:
        """Create a complex document."""
        doc = QtGui.QTextDocument()
        doc.setDefaultStyleSheet(self.stylesheet)
        contents = ''
        for n in nodes:
            if heads:
                contents += f"<h1>{self.sanitize_html(n.h)}</h1>\n"
            contents += f"<pre>{self.sanitize_html(n.b)}</pre>\n"
        doc.setHtml(contents)
        return doc

    #@ pr.document
    def document(self, text: str, head: str | None = None) -> QtGui.QTextDocument:
        """Create a Qt document."""
        doc = QtGui.QTextDocument()
        doc.setDefaultStyleSheet(self.stylesheet)
        text = self.sanitize_html(text)
        if head:
            head = self.sanitize_html(head)
            contents = f"<h1>{head}</h1>\n<pre>{text}</pre>"
        else:
            contents = f"<pre>{text}<pre>"
        doc.setHtml(contents)
        return doc

    #@ pr.html_document
    def html_document(self, text: str) -> QtGui.QTextDocument:
        """Create an HTML document."""
        doc = QtGui.QTextDocument()
        doc.setDefaultStyleSheet(self.stylesheet)
        doc.setHtml(text)
        return doc

    #@< pr.Helpers
    #@> pr.expand
    def expand(self, p: Position) -> str:
        """Return the entire script at node p."""
        return p.script

    #@ pr.getBodies
    def getBodies(self, p: Position) -> str:
        """Return a concatenated version of the tree at p"""
        return '\n'.join([p2.b for p2 in p.self_and_subtree(copy=False)])

    #@ pr.getNodes
    def getNodes(self, p: Position) -> str:
        """Return the entire script at node p."""
        result = [p.b]
        for p in p.subtree():
            result.extend(['', f"Node: {p.h}", ''])
            result.append(p.b)
        return '\n'.join(result)

    #@ pr.sanitize html
    def sanitize_html(self, html: str) -> str:
        """Generate html escapes."""
        return html.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    #@< pr.Preview
    #@> pr.preview_body
    @cmd('preview-body')
    def preview_body(self, event: LeoKeyEvent | None = None) -> None:
        """Preview the body of the selected node."""
        doc = self.document(self.c.p.b)
        self.preview_doc(doc)

    #@ pr.preview_html
    @cmd('preview-html')
    def preview_html(self, event: LeoKeyEvent | None = None) -> None:
        """
        Preview the body of the selected text as html. The body must be valid
        html, including <html> and <body> elements.
        """
        doc = self.html_document(self.c.p.b)
        self.preview_doc(doc)

    #@ pr.preview_expanded_body
    @cmd('preview-expanded-body')
    def preview_expanded_body(self, event: LeoKeyEvent | None = None) -> None:
        """Preview the selected node's body, expanded"""
        doc = self.document(self.expand(self.c.p))
        self.preview_doc(doc)

    #@ pr.preview_expanded_html
    @cmd('preview-expanded-html')
    def preview_expanded_html(self, event: LeoKeyEvent | None = None) -> None:
        """
        Preview all the expanded bodies of the selected node as html. The
        expanded text must be valid html, including <html> and <body> elements.
        """
        doc = self.html_document(self.expand(self.c.p))
        self.preview_doc(doc)

    #@ pr.preview_marked_bodies
    @cmd('preview-marked-bodies')
    def preview_marked_bodies(self, event: LeoKeyEvent | None = None) -> None:
        """Preview the bodies of the marked nodes."""
        nodes = [p.v for p in self.c.all_positions() if p.isMarked()]
        doc = self.complex_document(nodes)
        self.preview_doc(doc)

    #@ pr.preview_marked_html
    @cmd('preview-marked-html')
    def preview_marked_html(self, event: LeoKeyEvent | None = None) -> None:
        """
        Preview the concatenated bodies of the marked nodes. The concatenated
        bodies must be valid html, including <html> and <body> elements.
        """
        nodes = [p.v for p in self.c.all_positions() if p.isMarked()]
        s = '\n'.join([z.b for z in nodes])
        doc = self.html_document(s)
        self.preview_doc(doc)

    #@ pr.preview_marked_nodes
    @cmd('preview-marked-nodes')
    def preview_marked_nodes(self, event: LeoKeyEvent | None = None) -> None:
        """Preview the marked nodes."""
        nodes = [p.v for p in self.c.all_positions() if p.isMarked()]
        doc = self.complex_document(nodes, heads=True)
        self.preview_doc(doc)

    #@ pr.preview_node
    @cmd('preview-node')
    def preview_node(self, event: LeoKeyEvent | None = None) -> None:
        """Preview the selected node."""
        p = self.c.p
        doc = self.document(p.b, head=p.h)
        self.preview_doc(doc)

    #@ pr.preview_tree_bodies
    @cmd('preview-tree-bodies')
    def preview_tree_bodies(self, event: LeoKeyEvent | None = None) -> None:
        """Preview the bodies in the selected tree."""
        doc = self.document(self.getBodies(self.c.p))
        self.preview_doc(doc)

    #@ pr.preview_tree_nodes
    @cmd('preview-tree-nodes')
    def preview_tree_nodes(self, event: LeoKeyEvent | None = None) -> None:
        """Preview the entire tree."""
        p = self.c.p
        doc = self.document(self.getNodes(p), head=p.h)
        self.preview_doc(doc)

    #@ pr_preview_tree_html
    @cmd('preview-tree-html')
    def preview_tree_html(self, event: LeoKeyEvent | None = None) -> None:
        """
        Preview all the bodies of the selected node as html. The concatenated
        bodies must valid html, including <html> and <body> elements.
        """
        doc = self.html_document(self.getBodies(self.c.p))
        self.preview_doc(doc)

    #@< pr.Print
    #@> pr.print_body
    @cmd('print-body')
    def print_body(self, event: LeoKeyEvent | None = None) -> None:
        """Print the selected node's body"""
        doc = self.document(self.c.p.b)
        self.print_doc(doc)

    #@ pr.print_html
    @cmd('print-html')
    def print_html(self, event: LeoKeyEvent | None = None) -> None:
        """
        Print the body of the selected text as html. The body must be valid
        html, including <html> and <body> elements.
        """
        doc = self.html_document(self.c.p.b)
        self.print_doc(doc)

    #@ pr.print_expanded_body
    @cmd('print-expanded-body')
    def print_expanded_body(self, event: LeoKeyEvent | None = None) -> None:
        """Print the selected node's body, expanded"""
        doc = self.document(self.expand(self.c.p))
        self.print_doc(doc)

    #@ pr.print_expanded_html
    @cmd('print-expanded-html')
    def print_expanded_html(self, event: LeoKeyEvent | None = None) -> None:
        """
        Preview all the expanded bodies of the selected node as html. The
        expanded text must be valid html, including <html> and <body> elements.
        """
        doc = self.html_document(self.expand(self.c.p))
        self.print_doc(doc)

    #@ pr.print_marked_bodies
    @cmd('print-marked-bodies')
    def print_marked_bodies(self, event: LeoKeyEvent | None = None) -> None:
        """Print the body text of marked nodes."""
        nodes = [p.v for p in self.c.all_positions() if p.isMarked()]
        doc = self.complex_document(nodes)
        self.print_doc(doc)

    #@ pr.print_marked_html
    @cmd('print-marked-html')
    def print_marked_html(self, event: LeoKeyEvent | None = None) -> None:
        """
        Print the concatenated bodies of the marked nodes. The concatenated
        bodies must be valid html, including <html> and <body> elements.
        """
        nodes = [p.v for p in self.c.all_positions() if p.isMarked()]
        s = '\n'.join([z.b for z in nodes])
        doc = self.html_document(s)
        self.print_doc(doc)

    #@ pr.print_marked_nodes
    @cmd('print-marked-nodes')
    def print_marked_nodes(self, event: LeoKeyEvent | None = None) -> None:
        """Print all the marked nodes"""
        nodes = [p.v for p in self.c.all_positions() if p.isMarked()]
        doc = self.complex_document(nodes, heads=True)
        self.print_doc(doc)

    #@ pr.print_node
    @cmd('print-node')
    def print_node(self, event: LeoKeyEvent | None = None) -> None:
        """Print the selected node"""
        doc = self.document(self.c.p.b, head=self.c.p.h)
        self.print_doc(doc)

    #@ pr.print_tree_bodies
    @cmd('print-tree-bodies')
    def print_tree_bodies(self, event: LeoKeyEvent | None = None) -> None:
        """Print all the bodies in the selected tree."""
        doc = self.document(self.getBodies(self.c.p))
        self.print_doc(doc)

    #@ pr.print_tree_html
    @cmd('print-tree-html')
    def print_tree_html(self, event: LeoKeyEvent | None = None) -> None:
        """
        Print all the bodies of the selected node as html. The concatenated
        bodies must valid html, including <html> and <body> elements.
        """
        doc = self.html_document(self.getBodies(self.c.p))
        self.print_doc(doc)

    #@ pr.print_tree_nodes
    @cmd('print-tree-nodes')
    def print_tree_nodes(self, event: LeoKeyEvent | None = None) -> None:
        """Print all the nodes of the selected tree."""
        doc = self.document(self.getNodes(self.c.p), head=self.c.p.h)
        self.print_doc(doc)

    #@< pr.Top level
    #@> pr.print_doc
    def print_doc(self, doc: QtGui.QTextDocument) -> None:
        """Print the document."""
        if not printsupport:
            g.trace('Qt.printsupport not found.')
            return
        dialog = printsupport.QPrintDialog()
        dialog.setStyleSheet(self.stylesheet)
        result = dialog.exec()
        if result == DialogCode.Accepted:
            doc.print(dialog.printer())

    #@ pr.preview_doc
    def preview_doc(self, doc: QtGui.QTextDocument) -> None:
        """Preview the document."""
        dialog = printsupport.QPrintPreviewDialog()
        dialog.setSizeGripEnabled(True)
        dialog.setStyleSheet(self.stylesheet)
        dialog.paintRequested.connect(doc.print)
        dialog.exec()

    #@-others


#@-others
#@@language python
#@@tabwidth -4
#@-leo
