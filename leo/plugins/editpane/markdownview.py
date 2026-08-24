#@+leo-ver=cub-1-thin
#@0 [tbrown.20171028115144.4] @f ../plugins/editpane/markdownview.py
#@+<< markdownview imports >>
#@> << markdownview imports >>
import markdown
from leo.core import leoGlobals as g

assert g

# FIXME: for now, prefer the older WebKit over WebEngine.  WebEngine is
# probably superior, but needs --disable-web-security passed to the
# QApplication to load local images without a server.
try:
    from leo.plugins.editpane.webkitview import LEP_WebKitView as HtmlView
except ImportError:
    from leo.plugins.editpane.webengineview import LEP_WebEngineView as HtmlView

from leo.plugins.editpane.plaintextview import LEP_PlainTextView as TextView


#@-<< markdownview imports >>
#@+others
#@ to_html
def to_html(text):
    """to_html - convert to HTML

    Args:
        text (str): markdown text to convert

    Returns:
        str: html
    """

    return markdown.markdown(
        text,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ],
    )


#@ class LEP_MarkdownView
class LEP_MarkdownView(HtmlView):
    """LEP_MarkdownView -"""

    lep_type = "MARKDOWN"
    lep_name = "Markdown(.py) View"

    #@+others
    #@> LEP_MarkdownView.__init__
    def __init__(self, c=None, lep=None, *args, **kwargs):
        """set up"""
        kwargs['c'] = c
        kwargs['lep'] = lep
        super().__init__(*args, **kwargs)
        self.c = c
        self.lep = lep

    #@ LEP_MarkdownView.new_text
    def new_text(self, text):
        """new_text - update for new text

        Args:
            text (str): new text
        """
        self.setHtml(to_html(text))

    #@ LEP_MarkdownView.update_text
    def update_text(self, text):
        """update_text - update for current text

        Args:
            text (str): current position
        """
        # h = self.horizontalScrollBar().value()
        # v = self.verticalScrollBar().value()
        self.new_text(text)
        # self.horizontalScrollBar().setValue(h)
        # self.verticalScrollBar().setValue(v)

    #@-others


#@< class LEP_MarkdownHtmlView
class LEP_MarkdownHtmlView(TextView):
    """LEP_MarkdownHtmlView - view the HTML for markdown"""

    lep_type = "MARKDOWN-HTML"
    lep_name = "Markdown(.py) Html View"

    #@+others
    #@> LEP_MarkdownHtmlView.__init__
    def __init__(self, c=None, lep=None, *args, **kwargs):
        """set up"""
        kwargs['c'] = c
        kwargs['lep'] = lep
        super().__init__(*args, **kwargs)
        self.c = c
        self.lep = lep

    #@ LEP_MarkdownHtmlView.new_text
    def new_text(self, text):
        """new_text - update for new text

        Args:
            text (str): new text
        """
        self.setPlainText(to_html(text))

    #@-others


#@-others
#@@language python
#@@tabwidth -4
#@-leo
