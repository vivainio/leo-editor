#@+leo-ver=cub-1-thin
#@0 [tbrown.20171028115144.5] @f ../plugins/editpane/leotextedit.py
#@+<<leotextedit imports >>
#@> <<leotextedit imports >>
from leo.core import leoGlobals as g

assert g
from leo.core.leoQt import QtGui, QtWidgets
from leo.core.leoColorizer import JEditColorizer  # LeoHighlighter


#@-<<leotextedit imports >>
#@+others
#@ DBG
def DBG(text):
    """DBG - temporary debugging function

    Args:
        text (str): text to print
    """
    # print(f"LEP: {text}")


#@ class LEP_LeoTextEdit
class LEP_LeoTextEdit(QtWidgets.QTextEdit):
    """LEP_LeoTextEdit - Leo LeoEditorPane editor"""

    lep_type = "EDITOR"
    lep_name = "Leo Text Edit"

    #@+others
    #@> __init__
    def __init__(self, c, lep=None, *args, **kwargs):
        """set up"""
        super().__init__(*args, **kwargs)
        self.c = c
        self.lep = lep
        self.textChanged.connect(self.text_changed)
        self.highlighter = JEditColorizer(c, self)

    #@ focusInEvent
    def focusInEvent(self, event: QtGui.QFocusEvent) -> None:
        QtWidgets.QTextEdit.focusInEvent(self, event)
        DBG("focusin()")
        self.lep.edit_widget_focus()

    #@ focusOutEvent
    def focusOutEvent(self, event: QtGui.QFocusEvent) -> None:
        QtWidgets.QTextEdit.focusOutEvent(self, event)
        DBG("focusout()")

    #@ new_text
    def new_text(self, text):
        """new_text - update for new text

        Args:
            text (str): new text
        """
        self.setPlainText(text)

    #@ text_changed
    def text_changed(self):
        """text_changed - text editor text changed"""
        if QtWidgets.QApplication.focusWidget() == self:
            DBG("text changed, focused")
            self.lep.text_changed(self.toPlainText())

        else:
            DBG("text changed, NOT focused")

    #@ update_text
    def update_text(self, text):
        """update_text - update for current text

        Args:
            text (str): current text
        """
        DBG("update editor text")
        self.setPlainText(text)

    #@-others


#@-others
#@@language python
#@@tabwidth -4
#@-leo
