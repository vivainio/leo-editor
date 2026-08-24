#@+leo-ver=cub-1-thin
#@0 [tbrown.20171028115144.1] @f ../plugins/editpane/plaintextview.py
from leo.core.leoQt import QtWidgets


#@+others
#@> class LEP_PlainTextView
class LEP_PlainTextView(QtWidgets.QTextBrowser):
    """LEP_PlainTextView - simplest possible LeoEditorPane viewer"""

    lep_type = "TEXT"
    lep_name = "Plain Text View"

    #@+others
    #@> __init__
    def __init__(self, c=None, lep=None, *args, **kwargs):
        """set up"""
        super().__init__(*args, **kwargs)
        self.c = c
        self.lep = lep
        self.setStyleSheet("* {background: #998; color: #222; }")

    #@ new_text
    def new_text(self, text):
        """new_text - update for new text

        Args:
            text (str): new text
        """
        self.setPlainText(text)

    #@ update_text
    def update_text(self, text):
        """update_text - update for current text

        Args:
            text (str): current text
        """
        h = self.horizontalScrollBar().value()
        v = self.verticalScrollBar().value()
        self.new_text(text)
        self.horizontalScrollBar().setValue(h)
        self.verticalScrollBar().setValue(v)

    #@-others


#@< class LEP_PlainTextViewB
class LEP_PlainTextViewB(LEP_PlainTextView):
    """LEP_PlainTextViewB - copy of LEP_PlainTextView with different
    background color to test multiple viewers
    """

    lep_name = "Plain Text View 'B'"

    #@+others
    #@> LEP_PlainTextViewB.__init__
    def __init__(self, c=None, lep=None, *args, **kwargs):
        """set up"""
        kwargs['c'] = c
        kwargs['lep'] = lep
        super().__init__(*args, **kwargs)
        self.setStyleSheet("* {background: #899; color: #222; }")

    #@-others


#@-others
#@@language python
#@@tabwidth -4
#@-leo
