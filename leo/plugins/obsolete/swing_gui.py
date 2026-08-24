# -*- coding: utf-8 -*-
#@+leo-ver=cub-1-thin
#@0 [ekr.20081121105001.595] @f ./obsolete/swing_gui.py
#@@first

'''The plugin part of the swing gui code.'''

# This code has not been tested since and will certainly not work as is.

#@@language python
#@@tabwidth -4
#@@pagewidth 80

#@+<< swing imports >>
#@> << swing imports >>
import leo.core.leoGlobals as g

import leo.core.leoChapters as leoChapters
import leo.core.leoColor as leoColor
import leo.core.leoFrame as leoFrame
import leo.core.leoGui as leoGui
import leo.core.leoKeys as leoKeys
import leo.core.leoMenu as leoMenu
import leo.core.leoNodes as leoNodes

import javax.swing as swing
import java.awt as awt
import java.lang

import os

# import string
import sys
import threading
import time
#@-<< swing imports >>


#@+others
#@ startJyleo
def startJyleo():
    import java.awt as awt

    print('*** run:jyLeo', sys.platform)  # e.g., java1.6.0_02

    if 1:
        g.app.splash = None
    else:
        g.app.splash = splash = leoSwingFrame.leoSplash()
        awt.EventQueue.invokeAndWait(splash)

    gct = leoSwingUtils.GCEveryOneMinute()
    gct.run()

    tk = awt.Toolkit.getDefaultToolkit()
    tk.setDynamicLayout(True)


#@ leoSwingDialog
#@>  class leoSwingDialog
class leoSwingDialog:
    """The base class for all Leo swing dialogs"""

    #@+others
    #@> __init__ (tkDialog)
    def __init__(self, c, title="", resizeable=True, canClose=True, show=True):
        """Constructor for the leoSwingDialog class."""

        self.answer = None  # Value returned from run()
        self.c = c  # For use by delayed focus methods in c.frame.
        self.resizeable = resizeable
        self.title = title
        self.modal = None

        self.buttonsFrame = None  # Frame to hold typical dialog buttons.
        self.defaultButtonCommand = (
            None  # Command to call when user closes the window by clicking the close box.
        )
        self.frame = None  # The outermost frame.
        self.root = None  # g.app.root
        self.showFlag = show
        self.top = None  # The toplevel Tk widget.
        self.focus_widget = None  # The widget to get the first focus.
        self.canClose = canClose

    #@ cancelButton, noButton, okButton, yesButton
    def cancelButton(self):
        """Do default click action in cancel button."""

        self.answer = "cancel"
        self.top.destroy()

    def noButton(self):
        """Do default click action in no button."""

        self.answer = "no"
        self.top.destroy()

    def okButton(self):
        """Do default click action in ok button."""

        self.answer = "ok"
        self.top.destroy()

    def yesButton(self):
        """Do default click action in yes button."""

        self.answer = "yes"
        self.top.destroy()

    #@ center
    def center(self):
        """Center any leoSwingDialog."""

        g.app.gui.center_dialog(self.top)

    #@ createButtons
    def createButtons(self, buttons):
        """Create a row of buttons.

        buttons is a list of dictionaries containing the properties of each button."""

        assert self.frame
        self.buttonsFrame = f = Tk.Frame(self.top)
        f.pack(side="top", padx=30)

        # Buttons is a list of dictionaries, with an empty dictionary at the end if there is only one entry.
        buttonList = []
        for d in buttons:
            text = d.get("text", "<missing button name>")
            isDefault = d.get("default", False)
            underline = d.get("underline", 0)
            command = d.get("command", None)
            bd = g.choose(isDefault, 4, 2)

            b = Tk.Button(f, width=6, text=text, bd=bd, underline=underline, command=command)
            b.pack(side="left", padx=5, pady=10)
            buttonList.append(b)

            if isDefault and command:
                self.defaultButtonCommand = command

        return buttonList

    #@ createMessageFrame
    def createMessageFrame(self, message):
        """Create a frame containing a Tk.Label widget."""

        label = Tk.Label(self.frame, text=message)
        label.pack(pady=10)

    #@ createTopFrame
    def createTopFrame(self):
        """Create the Tk.Toplevel widget for a leoSwingDialog."""

        if g.app.unitTesting:
            return

        self.root = g.app.root
        # g.trace("leoSwingDialog",'root',self.root)

        self.top = Tk.Toplevel(self.root)
        self.top.title(self.title)

        if not self.resizeable:
            self.top.resizable(0, 0)  # neither height or width is resizable.

        self.frame = Tk.Frame(self.top)
        self.frame.pack(side="top", expand=1, fill="both")

        if not self.canClose:
            self.top.protocol("WM_DELETE_WINDOW", self.onClose)

        # Do this at idle time.
        def attachIconCallback(top=self.top):
            g.app.gui.attachLeoIcon(top)

        ### self.top.after_idle(attachIconCallback)

    #@ onClose
    def onClose(self):
        """Disable all attempts to close this frame with the close box."""

        pass

    #@ run (tkDialog)
    def run(self, modal):
        """Run a leoSwingDialog."""

        if g.app.unitTesting:
            return None

        c = self.c
        self.modal = modal

        self.center()  # Do this after all packing complete.
        if self.showFlag:
            self.top.lift()
        else:
            self.top.withdraw()

        # Get all keystrokes.
        if self.modal:
            self.top.grab_set()  # Make the dialog a modal dialog.

        if self.focus_widget == None:
            self.focus_widget = self.top

        c and c.widgetWantsFocusNow(self.focus_widget)

        self.root.wait_window(self.top)

        if self.modal:
            return self.answer
        else:
            return None

    #@-others


#@< class swingAboutLeo
class swingAboutLeo(leoSwingDialog):
    """A class that creates the swing About Leo dialog."""

    #@+others
    #@> swingAboutLeo.__init__
    def __init__(self, c, version, theCopyright, url, email):
        """Create a swing About Leo dialog."""

        leoSwingDialog.__init__(self, c, "About Leo", resizeable=True)  # Initialize the base class.

        if g.app.unitTesting:
            return

        self.copyright = theCopyright
        self.email = email
        self.url = url
        self.version = version

        c.inCommand = False  # Allow the app to close immediately.

        self.createTopFrame()
        self.createFrame()

    #@ swingAboutLeo.createFrame
    def createFrame(self):
        """Create the frame for an About Leo dialog."""

        if g.app.unitTesting:
            return

        frame = self.frame
        theCopyright = self.copyright
        email = self.email
        url = self.url
        version = self.version

        # Calculate the approximate height & width. (There are bugs in Tk here.)
        lines = string.split(theCopyright, '\n')
        height = len(lines) + 8  # Add lines for version,url,email,spacing.
        width = 0
        for line in lines:
            width = max(width, len(line))
        width = max(width, len(url))
        width += 10  # 9/9/02

        frame.pack(padx=6, pady=4)

        self.text = w = g.app.gui.plainTextWidget(
            frame, height=height, width=width, bd=0, bg=frame.cget("background")
        )
        w.pack(pady=10)

        try:
            bitmap_name = g.os_path_join(g.app.loadDir, "..", "Icons", "Leoapp.GIF")  # 5/12/03
            image = Tk.PhotoImage(file=bitmap_name)
            w.image_create("1.0", image=image, padx=10)
        except Exception:
            pass  # This can sometimes happen for mysterious reasons.

        w.insert("end", version)  # ,tag="version")
        w.tag_add('version', 'end-%dc' % (len(version) + 1), 'end-1c')
        w.insert("end", theCopyright)  # ,tag="copyright")
        w.tag_add('copyright', 'end-%dc' % (len(theCopyright) + 1), 'end-1c')
        w.insert("end", '\n')
        w.insert("end", url)
        w.tag_add('url', 'end-%dc' % (len(url) + 1), 'end-1c')
        w.insert("end", '\n')
        w.insert("end", email)
        w.tag_add('url', 'end-%dc' % (len(email) + 1), 'end-1c')

        w.tag_config("version", justify="center")
        w.tag_config("copyright", justify="center", spacing1="3")
        w.tag_config("url", underline=1, justify="center", spacing1="10")

        w.tag_bind("url", "<Button-1>", self.onAboutLeoUrl)
        w.tag_bind("url", "<Enter>", self.setArrowCursor)
        w.tag_bind("url", "<Leave>", self.setDefaultCursor)

        w.tag_config("email", underline=1, justify="center", spacing1="10")
        w.tag_bind("email", "<Button-1>", self.onAboutLeoEmail)
        w.tag_bind("email", "<Enter>", self.setArrowCursor)
        w.tag_bind("email", "<Leave>", self.setDefaultCursor)

        w.configure(state="disabled")

    #@ swingAboutLeo.onAboutLeoEmail
    def onAboutLeoEmail(self, event=None):
        """Handle clicks in the email link in an About Leo dialog."""

        # __pychecker__ = '--no-argsused' # the event param must be present.

        try:
            import webbrowser

            webbrowser.open("mailto:" + self.email)
        except:
            g.es("not found: " + self.email)

    #@ swingAboutLeo.onAboutLeoUrl
    def onAboutLeoUrl(self, event=None):
        """Handle clicks in the url link in an About Leo dialog."""

        # __pychecker__ = '--no-argsused' # the event param must be present.

        try:
            import webbrowser

            webbrowser.open(self.url)
        except:
            g.es("not found: " + self.url)

    #@ swingAboutLeo: setArrowCursor, setDefaultCursor
    def setArrowCursor(self, event=None):
        """Set the cursor to an arrow in an About Leo dialog."""

        # __pychecker__ = '--no-argsused' # the event param must be present.

        self.text.configure(cursor="arrow")

    def setDefaultCursor(self, event=None):
        """Set the cursor to the default cursor in an About Leo dialog."""

        # __pychecker__ = '--no-argsused' # the event param must be present.

        self.text.configure(cursor="xterm")

    #@-others


#@< class swingAskLeoID
class swingAskLeoID(leoSwingDialog):
    """A class that creates the swing About Leo dialog."""

    #@+others
    #@> swingAskLeoID.__init__
    def __init__(self, c=None):
        """Create the Leo Id dialog."""

        # Initialize the base class: prevent clicks in the close box from closing.
        leoSwingDialog.__init__(self, c, "Enter unique id", resizeable=False, canClose=False)

        if g.app.unitTesting:
            return

        self.id_entry = None
        self.answer = None

        self.createTopFrame()
        self.top.bind("<Key>", self.onKey)

        message = (
            "leoID.txt not found\n\n"
            + "Please enter an id that identifies you uniquely.\n"
            + "Your cvs login name is a good choice.\n\n"
            + "Your id must contain only letters and numbers\n"
            + "and must be at least 3 characters in length."
        )
        self.createFrame(message)
        self.focus_widget = self.id_entry

        buttons = ({"text": "OK", "command": self.onButton, "default": True},)  # Singleton tuple.
        buttonList = self.createButtons(buttons)
        self.ok_button = buttonList[0]
        self.ok_button.configure(state="disabled")

    #@ swingAskLeoID.createFrame
    def createFrame(self, message):
        """Create the frame for the Leo Id dialog."""

        if g.app.unitTesting:
            return

        f = self.frame

        label = Tk.Label(f, text=message)
        label.pack(pady=10)

        self.id_entry = text = Tk.Entry(f, width=20)
        text.pack()

    #@ swingAskLeoID.onButton
    def onButton(self):
        """Handle clicks in the Leo Id close button."""

        s = self.id_entry.get().strip()
        if len(s) < 3:  # Require at least 3 characters in an id.
            return

        self.answer = g.app.leoID = s

        self.top.destroy()  # terminates wait_window
        self.top = None

    #@ swingAskLeoID.onKey
    def onKey(self, event):
        """Handle keystrokes in the Leo Id dialog."""

        #@+<< eliminate invalid characters >>
        #@> << eliminate invalid characters >>
        e = self.id_entry
        s = e.get().strip()
        i = 0
        ok = True
        while i < len(s):
            ch = s[i]
            if not ch.isalnum():
                e.delete(str(i))
                s = e.get()
                ok = False
            else:
                i += 1
        if not ok:
            return
        #@-<< eliminate invalid characters >>
        #@+<< enable the ok button if there are 3 or more valid characters >>
        #@ << enable the ok button if there are 3 or more valid characters >>
        e = self.id_entry
        b = self.ok_button

        if len(e.get().strip()) >= 3:
            b.configure(state="normal")
        else:
            b.configure(state="disabled")
        #@-<< enable the ok button if there are 3 or more valid characters >>

        ch = event.char.lower()
        if ch in ('\n', '\r'):
            self.onButton()
        return "break"

    #@-others


#@<2 class swingAskOk
class swingAskOk(leoSwingDialog):
    """A class that creates a swing dialog with a single OK button."""

    #@+others
    #@> class swingAskOk.__init__
    def __init__(self, c, title, message=None, text="Ok", resizeable=False):
        """Create a dialog with one button"""

        leoSwingDialog.__init__(self, c, title, resizeable)  # Initialize the base class.

        if g.app.unitTesting:
            return

        self.text = text
        self.createTopFrame()
        self.top.bind("<Key>", self.onKey)

        if message:
            self.createMessageFrame(message)

        buttons = ({"text": text, "command": self.okButton, "default": True},)  # Singleton tuple.
        self.createButtons(buttons)

    #@ class swingAskOk.onKey
    def onKey(self, event):
        """Handle Key events in askOk dialogs."""

        ch = event.char.lower()

        if ch in (self.text[0].lower(), '\n', '\r'):
            self.okButton()

        return "break"

    #@-others


#@< class swingAskOkCancelNumber
class swingAskOkCancelNumber(leoSwingDialog):
    """Create and run a modal swing dialog to get a number."""

    #@+others
    #@> swingAskOKCancelNumber.__init__
    def __init__(self, c, title, message):
        """Create a number dialog"""

        leoSwingDialog.__init__(self, c, title, resizeable=False)  # Initialize the base class.

        if g.app.unitTesting:
            return

        self.answer = -1
        self.number_entry = None

        self.createTopFrame()
        self.top.bind("<Key>", self.onKey)

        self.createFrame(message)
        self.focus_widget = self.number_entry

        buttons = (
            {"text": "Ok", "command": self.okButton, "default": True},
            {"text": "Cancel", "command": self.cancelButton},
        )
        buttonList = self.createButtons(buttons)
        self.ok_button = buttonList[0]  # Override the default kind of Ok button.

    #@ swingAskOKCancelNumber.createFrame
    def createFrame(self, message):
        """Create the frame for a number dialog."""

        if g.app.unitTesting:
            return

        c = self.c

        lab = Tk.Label(self.frame, text=message)
        lab.pack(pady=10, side="left")

        self.number_entry = w = Tk.Entry(self.frame, width=20)
        w.pack(side="left")

        c.set_focus(w)

    #@ swingAskOKCancelNumber.okButton, cancelButton
    def okButton(self):
        """Handle clicks in the ok button of a number dialog."""

        s = self.number_entry.get().strip()

        try:
            self.answer = int(s)
        except:
            self.answer = -1  # Cancel the operation.

        self.top.destroy()

    def cancelButton(self):
        """Handle clicks in the cancel button of a number dialog."""

        self.answer = -1
        self.top.destroy()

    #@ swingAskOKCancelNumber.onKey
    def onKey(self, event):
        #@+<< eliminate non-numbers >>
        #@> << eliminate non-numbers >>
        e = self.number_entry
        s = e.get().strip()

        i = 0
        while i < len(s):
            ch = s[i]
            if not ch.isdigit():
                e.delete(str(i))
                s = e.get()
            else:
                i += 1
        #@-<< eliminate non-numbers >>

        ch = event.char.lower()

        if ch in ('o', '\n', '\r'):
            self.okButton()
        elif ch == 'c':
            self.cancelButton()

        return "break"

    #@-others


#@<2 class swingAskOkCancelString
class swingAskOkCancelString(leoSwingDialog):
    """Create and run a modal swing dialog to get a string."""

    #@+others
    #@> swingAskOKCancelString.__init__
    def __init__(self, c, title, message):
        """Create a number dialog"""

        leoSwingDialog.__init__(self, c, title, resizeable=False)  # Initialize the base class.

        if g.app.unitTesting:
            return

        self.answer = -1
        self.number_entry = None

        self.createTopFrame()
        self.top.bind("<Key>", self.onKey)

        self.createFrame(message)
        self.focus_widget = self.number_entry

        buttons = (
            {"text": "Ok", "command": self.okButton, "default": True},
            {"text": "Cancel", "command": self.cancelButton},
        )
        buttonList = self.createButtons(buttons)
        self.ok_button = buttonList[0]  # Override the default kind of Ok button.

    #@ swingAskOkCancelString.createFrame
    def createFrame(self, message):
        """Create the frame for a number dialog."""

        if g.app.unitTesting:
            return

        c = self.c

        lab = Tk.Label(self.frame, text=message)
        lab.pack(pady=10, side="left")

        self.number_entry = w = Tk.Entry(self.frame, width=20)
        w.pack(side="left")

        c.set_focus(w)

    #@ swingAskOkCancelString.okButton, cancelButton
    def okButton(self):
        """Handle clicks in the ok button of a string dialog."""

        self.answer = self.number_entry.get().strip()
        self.top.destroy()

    def cancelButton(self):
        """Handle clicks in the cancel button of a string dialog."""

        self.answer = ''
        self.top.destroy()

    #@ swingAskOkCancelString.onKey
    def onKey(self, event):
        ch = event.char.lower()

        if ch in ('o', '\n', '\r'):
            self.okButton()
        elif ch == 'c':
            self.cancelButton()

        return "break"

    #@-others


#@< class swingAskYesNo
class swingAskYesNo(leoSwingDialog):
    """A class that creates a swing dialog with two buttons: Yes and No."""

    #@+others
    #@> swingAskYesNo.__init__
    def __init__(self, c, title, message=None, resizeable=False):
        """Create a dialog having yes and no buttons."""

        leoSwingDialog.__init__(self, c, title, resizeable)  # Initialize the base class.

        if g.app.unitTesting:
            return

        self.createTopFrame()
        self.top.bind("<Key>", self.onKey)

        if message:
            self.createMessageFrame(message)

        buttons = (
            {"text": "Yes", "command": self.yesButton, "default": True},
            {"text": "No", "command": self.noButton},
        )
        self.createButtons(buttons)

    #@ swingAskYesNo.onKey
    def onKey(self, event):
        """Handle keystroke events in dialogs having yes and no buttons."""

        ch = event.char.lower()

        if ch in ('y', '\n', '\r'):
            self.yesButton()
        elif ch == 'n':
            self.noButton()

        return "break"

    #@-others


#@< class swingAskYesNoCancel
class swingAskYesNoCancel(leoSwingDialog):
    """A class to create and run swing dialogs having three buttons.

    By default, these buttons are labeled Yes, No and Cancel."""

    #@+others
    #@> askYesNoCancel.__init__
    def __init__(
        self,
        c,
        title,
        message=None,
        yesMessage="Yes",
        noMessage="No",
        defaultButton="Yes",
        resizeable=False,
    ):
        """Create a dialog having three buttons."""

        leoSwingDialog.__init__(
            self, c, title, resizeable, canClose=False
        )  # Initialize the base class.

        if g.app.unitTesting:
            return

        self.yesMessage, self.noMessage = yesMessage, noMessage
        self.defaultButton = defaultButton

        self.createTopFrame()
        self.top.bind("<Key>", self.onKey)

        if message:
            self.createMessageFrame(message)

        buttons = (
            {"text": yesMessage, "command": self.yesButton, "default": yesMessage == defaultButton},
            {"text": noMessage, "command": self.noButton, "default": noMessage == defaultButton},
            {"text": "Cancel", "command": self.cancelButton, "default": "Cancel" == defaultButton},
        )
        self.createButtons(buttons)

    #@ askYesNoCancel.onKey
    def onKey(self, event):
        """Handle keystrokes in dialogs with three buttons."""

        ch = event.char.lower()

        if ch in ('\n', '\r'):
            ch = self.defaultButton[0].lower()

        if ch == self.yesMessage[0].lower():
            self.yesButton()
        elif ch == self.noMessage[0].lower():
            self.noButton()
        elif ch == 'c':
            self.cancelButton()

        return "break"

    #@ askYesNoCancel.noButton & yesButton
    def noButton(self):
        """Handle clicks in the 'no' (second) button in a dialog with three buttons."""

        self.answer = self.noMessage.lower()
        self.top.destroy()

    def yesButton(self):
        """Handle clicks in the 'yes' (first) button in a dialog with three buttons."""

        self.answer = self.yesMessage.lower()
        self.top.destroy()

    #@-others


#@< class swingListboxDialog
class swingListBoxDialog(leoSwingDialog):
    """A base class for swing dialogs containing a Tk Listbox"""

    #@+others
    #@> swingListboxDialog.__init__
    def __init__(self, c, title, label):
        """Constructor for the base listboxDialog class."""

        leoSwingDialog.__init__(self, c, title, resizeable=True)  # Initialize the base class.

        if g.app.unitTesting:
            return

        self.createTopFrame()
        self.top.protocol("WM_DELETE_WINDOW", self.destroy)

        # Initialize common ivars.
        self.label = label
        self.positionList = []
        self.buttonFrame = None

        # Fill in the frame.
        self.createFrame()
        self.fillbox()

        # Make the common bindings after creating self.box.

        self.box.bind("<Double-Button-1>", self.go)

    #@ addStdButtons
    def addStdButtons(self, frame):
        """Add stanadard buttons to a listBox dialog."""

        # Create the ok and cancel buttons.
        self.ok = ok = Tk.Button(frame, text="Go", width=6, command=self.go)
        self.hide = hide = Tk.Button(frame, text="Hide", width=6, command=self.hide)

        ok.pack(side="left", pady=2, padx=5)
        hide.pack(side="left", pady=2, padx=5)

    #@ createFrame
    def createFrame(self):
        """Create the essentials of a listBoxDialog frame

        Subclasses will add buttons to self.buttonFrame"""

        if g.app.unitTesting:
            return

        self.outerFrame = f = Tk.Frame(self.frame)
        f.pack(expand=1, fill="both")

        if self.label:
            labf = Tk.Frame(f)
            labf.pack(pady=2)
            lab = Tk.Label(labf, text=self.label)
            lab.pack()

        f2 = Tk.Frame(f)
        f2.pack(expand=1, fill="both")

        self.box = box = Tk.Listbox(f2, height=20, width=30)
        box.pack(side="left", expand=1, fill="both")

        bar = Tk.Scrollbar(f2)
        bar.pack(side="left", fill="y")

        bar.config(command=box.yview)
        box.config(yscrollcommand=bar.set)

    #@ destroy
    def destroy(self, event=None):
        """Hide, do not destroy, a listboxDialog window

        subclasses may override to really destroy the window"""

        # __pychecker__ = '--no-argsused' # event not used, but must be present.

        self.top.withdraw()  # Don't allow this window to be destroyed.

    #@ hide
    def hide(self):
        """Hide a list box dialog."""

        self.top.withdraw()

    #@ fillbox
    def fillbox(self, event=None):
        """Fill a listbox from information.

        Overridden by subclasses"""

        # __pychecker__ = '--no-argsused' # the event param must be present.

        pass

    #@ go
    def go(self, event=None):
        """Handle clicks in the "go" button in a list box dialog."""

        # __pychecker__ = '--no-argsused' # the event param must be present.

        c = self.c
        box = self.box

        # Work around an old Python bug.  Convert strings to ints.
        items = box.curselection()
        try:
            items = map(int, items)
        except ValueError:
            pass

        if items:
            n = items[0]
            p = self.positionList[n]
            c.beginUpdate()
            try:
                c.expandAllAncestors(p)
                c.selectPosition(p, updateBeadList=True)
            finally:
                # A case could be made for updateBeadList=False
                c.endUpdate()

    #@-others


#@<2 leoSwingFrame
#@> class leoSwingFrame
class leoSwingFrame(leoFrame.leoFrame):
    #@+others
    #@>  Birth & Death (swingFrame)
    #@> __init__ (swingFrame)
    def __init__(self, title, gui):
        g.trace('swingFrame', g.callers(20))

        # Init the base class.
        leoFrame.leoFrame.__init__(self, gui)

        self.use_chapters = False  ###

        self.title = title

        leoSwingFrame.instances += 1

        self.c = None  # Set in finishCreate.
        self.iconBarClass = self.swingIconBarClass
        self.statusLineClass = self.swingStatusLineClass
        self.iconBar = None

        self.trace_status_line = None  # Set in finishCreate.

        #@+<< set the leoSwingFrame ivars >>
        #@-<< set the leoSwingFrame ivars >>

    #@ __repr__ (swingFrame)
    def __repr__(self):
        return "<leoSwingFrame: %s>" % self.title

    #@ swingFrame.finishCreate & helpers
    def finishCreate(self, c):
        f = self
        f.c = c
        g.trace('swingFrame')

        self.trace_status_line = c.config.getBool('trace_status_line')
        self.use_chapters = False and c.config.getBool('use_chapters')  ###
        self.use_chapter_tabs = False and c.config.getBool('use_chapter_tabs')  ###

        # This must be done after creating the commander.
        f.splitVerticalFlag, f.ratio, f.secondary_ratio = f.initialRatios()

        f.createOuterFrames()

        ### f.createIconBar()

        f.createSplitterComponents()

        ### f.createStatusLine()
        f.createFirstTreeNode()
        f.menu = leoSwingMenu(f)
        # c.finishCreate calls f.createMenuBar later.
        c.setLog()
        g.app.windowList.append(f)
        f.miniBufferWidget = f.createMiniBufferWidget()
        c.bodyWantsFocus()

    #@> createOuterFrames
    def createOuterFrames(self):
        f = self
        c = f.c

        def exit(event):
            java.lang.System.exit(0)

        f.top = w = swing.JFrame('jyLeo!', size=(700, 700), windowClosing=exit)
        w.contentPane.layout = awt.FlowLayout()

    #@ createSplitterComponents (removed frame.bodyCtrl ivar)
    def createSplitterComponents(self):
        f = self
        c = f.c

        g.trace()

        f.createLeoSplitters(f.outerFrame)

        if 0:
            # Create the canvas, tree, log and body.
            if f.use_chapters:
                c.chapterController = cc = leoChapters.chapterController(c)

            if self.use_chapters and self.use_chapter_tabs:
                cc.tt = leoSwingTreeTab(c, f.split2Pane1, cc)

            f.canvas = f.createCanvas(f.split2Pane1)
            f.tree = leoSwingTree.leoSwingTree(c, f, f.canvas)
            f.log = leoSwingLog(f, f.split2Pane2)
            f.body = leoSwingBody(f, f.split1Pane2)

        f.body = leoSwingBody(f, f.top)
        f.tree = leoSwingTree(c, f, f.top)
        f.log = leoSwingLog(f, f.top)

        # Configure.
        f.setTabWidth(c.tab_width)
        f.reconfigurePanes()
        f.body.setFontFromConfig()
        f.body.setColorFromConfig()

    #@ createFirstTreeNode
    def createFirstTreeNode(self):
        f = self
        c = f.c

        t = leoNodes.tnode()
        v = leoNodes.vnode(t)
        p = leoNodes.position(v, [])
        v.initHeadString("NewHeadline")
        p.moveToRoot(oldRoot=None)
        # c.setRootPosition(p) # New in 4.4.2.
        c.editPosition(p)

    #@< swingFrame.createCanvas & helpers
    def createCanvas(self, parentFrame, pack=True):
        c = self.c

        scrolls = c.config.getBool('outline_pane_scrolls_horizontally')
        scrolls = g.choose(scrolls, 1, 0)
        canvas = self.createTkTreeCanvas(parentFrame, scrolls, pack)
        self.setCanvasColorFromConfig(canvas)

        return canvas

    #@> f.createTkTreeCanvas & callbacks
    def createTkTreeCanvas(self, parentFrame, scrolls, pack):
        frame = self

        canvas = Tk.Canvas(parentFrame, name="canvas", bd=0, bg="white", relief="flat")

        treeBar = Tk.Scrollbar(parentFrame, name="treeBar")

        # New in Leo 4.4.3 b1: inject the ivar into the canvas.
        canvas.leo_treeBar = treeBar

        # Bind mouse wheel event to canvas
        if sys.platform != "win32":  # Works on 98, crashes on XP.
            canvas.bind("<MouseWheel>", frame.OnMouseWheel)
            if 1:  # New in 4.3.
                #@+<< workaround for mouse-wheel problems >>
                #@> << workaround for mouse-wheel problems >>
                # Handle mapping of mouse-wheel to buttons 4 and 5.

                def mapWheel(e):
                    if e.num == 4:  # Button 4
                        e.delta = 120
                        return frame.OnMouseWheel(e)
                    elif e.num == 5:  # Button 5
                        e.delta = -120
                        return frame.OnMouseWheel(e)

                canvas.bind("<ButtonPress>", mapWheel, add=1)
                #@-<< workaround for mouse-wheel problems >>

        canvas['yscrollcommand'] = self.setCallback
        treeBar['command'] = self.yviewCallback
        treeBar.pack(side="right", fill="y")
        if scrolls:
            treeXBar = Tk.Scrollbar(parentFrame, name='treeXBar', orient="horizontal")
            canvas['xscrollcommand'] = treeXBar.set
            treeXBar['command'] = canvas.xview
            treeXBar.pack(side="bottom", fill="x")

        if pack:
            canvas.pack(expand=1, fill="both")

        canvas.bind("<Button-1>", frame.OnActivateTree)

        # Handle mouse wheel in the outline pane.
        if sys.platform == "linux2":  # This crashes tcl83.dll
            canvas.bind("<MouseWheel>", frame.OnMouseWheel)
        if 0:
            #@+<< do scrolling by hand in a separate thread >>
            #@ << do scrolling by hand in a separate thread >>
            # New in 4.3: replaced global way with scrollWay ivar.
            ev = threading.Event()

            def run(self=self, canvas=canvas, ev=ev):
                while 1:
                    ev.wait()
                    if self.scrollWay == 'Down':
                        canvas.yview("scroll", 1, "units")
                    else:
                        canvas.yview("scroll", -1, "units")
                    time.sleep(0.1)

            t = threading.Thread(target=run)
            t.setDaemon(True)
            t.start()

            def scrollUp(event):
                scrollUpOrDown(event, 'Down')

            def scrollDn(event):
                scrollUpOrDown(event, 'Up')

            def scrollUpOrDown(event, theWay):
                if event.widget != canvas:
                    return
                if 0:  # This seems to interfere with scrolling.
                    if canvas.find_overlapping(event.x, event.y, event.x, event.y):
                        return
                ev.set()
                self.scrollWay = theWay

            def off(event, ev=ev, canvas=canvas):
                if event.widget != canvas:
                    return
                ev.clear()

            if 1:  # Use shift-click
                # Shift-button-1 scrolls up, Shift-button-2 scrolls down
                canvas.bind_all('<Shift Button-3>', scrollDn)
                canvas.bind_all('<Shift Button-1>', scrollUp)
                canvas.bind_all('<Shift ButtonRelease-1>', off)
                canvas.bind_all('<Shift ButtonRelease-3>', off)
            else:  # Use plain click.
                canvas.bind_all('<Button-3>', scrollDn)
                canvas.bind_all('<Button-1>', scrollUp)
                canvas.bind_all('<ButtonRelease-1>', off)
                canvas.bind_all('<ButtonRelease-3>', off)
            #@-<< do scrolling by hand in a separate thread >>

        # g.print_bindings("canvas",canvas)
        return canvas

    #@< f.setCanvasColorFromConfig
    def setCanvasColorFromConfig(self, canvas):
        c = self.c

        bg = c.config.getColor("outline_pane_background_color") or 'white'

        try:
            canvas.configure(bg=bg)
        except:
            g.es("exception setting outline pane background color")
            g.es_exception()

    #@< swingFrame.createLeoSplitters & helpers
    #
    # 1. self.splitVerticalFlag tells the alignment of the main splitter and
    # 2. not self.splitVerticalFlag tells the alignment of the secondary splitter.
    #
    # Only the general-purpose divideAnySplitter routine doesn't know about these
    # invariants. So most of this code is specialized for Leo's window. OTOH, creating
    # a single splitter window would be much easier than this code.
    #@@c

    def createLeoSplitters(self, parentFrame):
        # Splitter 1 is the main splitter containing splitter2 and the body pane.
        f1, bar1, split1Pane1, split1Pane2 = self.createLeoSwingSplitter(
            parentFrame, self.splitVerticalFlag, 'splitter1'
        )

        self.f1, self.bar1 = f1, bar1
        self.split1Pane1, self.split1Pane2 = split1Pane1, split1Pane2

        # Splitter 2 is the secondary splitter containing the tree and log panes.
        f2, bar2, split2Pane1, split2Pane2 = self.createLeoSwingSplitter(
            split1Pane1, not self.splitVerticalFlag, 'splitter2'
        )

        self.f2, self.bar2 = f2, bar2
        self.split2Pane1, self.split2Pane2 = split2Pane1, split2Pane2

    #@> createLeoSwingSplitter
    def createLeoSwingSplitter(self, parent, verticalFlag, componentName):
        c = self.c

        return None, None, None, None

    #@ bindBar
    def bindBar(self, bar, verticalFlag):
        if verticalFlag == self.splitVerticalFlag:
            bar.bind("<B1-Motion>", self.onDragMainSplitBar)

        else:
            bar.bind("<B1-Motion>", self.onDragSecondarySplitBar)

    #@ divideAnySplitter
    # This is the general-purpose placer for splitters.
    # It is the only general-purpose splitter code in Leo.

    def divideAnySplitter(self, frac, verticalFlag, bar, pane1, pane2):
        pass

    #@ divideLeoSplitter
    # Divides the main or secondary splitter, using the key invariant.
    def divideLeoSplitter(self, verticalFlag, frac):
        if self.splitVerticalFlag == verticalFlag:
            self.divideLeoSplitter1(frac, verticalFlag)
            self.ratio = frac  # Ratio of body pane to tree pane.
        else:
            self.divideLeoSplitter2(frac, verticalFlag)
            self.secondary_ratio = frac  # Ratio of tree pane to log pane.

    # Divides the main splitter.
    def divideLeoSplitter1(self, frac, verticalFlag):
        self.divideAnySplitter(frac, verticalFlag, self.bar1, self.split1Pane1, self.split1Pane2)

    # Divides the secondary splitter.
    def divideLeoSplitter2(self, frac, verticalFlag):
        self.divideAnySplitter(frac, verticalFlag, self.bar2, self.split2Pane1, self.split2Pane2)

    #@ onDrag...
    def onDragMainSplitBar(self, event):
        self.onDragSplitterBar(event, self.splitVerticalFlag)

    def onDragSecondarySplitBar(self, event):
        self.onDragSplitterBar(event, not self.splitVerticalFlag)

    def onDragSplitterBar(self, event, verticalFlag):
        # x and y are the coordinates of the cursor relative to the bar, not the main window.
        bar = event.widget
        x = event.x
        y = event.y
        top = bar.winfo_toplevel()

        if verticalFlag:
            # Panes arranged vertically; horizontal splitter bar
            wRoot = top.winfo_rooty()
            barRoot = bar.winfo_rooty()
            wMax = top.winfo_height()
            offset = float(barRoot) + y - wRoot
        else:
            # Panes arranged horizontally; vertical splitter bar
            wRoot = top.winfo_rootx()
            barRoot = bar.winfo_rootx()
            wMax = top.winfo_width()
            offset = float(barRoot) + x - wRoot

        # Adjust the pixels, not the frac.
        if offset < 3:
            offset = 3
        if offset > wMax - 2:
            offset = wMax - 2
        # Redraw the splitter as the drag is occuring.
        frac = float(offset) / wMax
        # g.trace(frac)
        self.divideLeoSplitter(verticalFlag, frac)

    #@ placeSplitter
    def placeSplitter(self, bar, pane1, pane2, verticalFlag):
        if verticalFlag:
            # Panes arranged vertically; horizontal splitter bar
            pane1.place(relx=0.5, rely=0, anchor="n", relwidth=1.0, relheight=0.5)
            pane2.place(relx=0.5, rely=1.0, anchor="s", relwidth=1.0, relheight=0.5)
            bar.place(relx=0.5, rely=0.5, anchor="c", relwidth=1.0)
        else:
            # Panes arranged horizontally; vertical splitter bar
            # adj gives tree pane more room when tiling vertically.
            adj = g.choose(verticalFlag != self.splitVerticalFlag, 0.65, 0.5)
            pane1.place(rely=0.5, relx=0, anchor="w", relheight=1.0, relwidth=adj)
            pane2.place(rely=0.5, relx=1.0, anchor="e", relheight=1.0, relwidth=1.0 - adj)
            bar.place(rely=0.5, relx=adj, anchor="c", relheight=1.0)

    #@< Destroying the swingFrame
    #@> destroyAllObjects
    def destroyAllObjects(self):
        """Clear all links to objects in a Leo window."""

        frame = self
        c = self.c
        tree = frame.tree
        body = self.body

        # g.printGcAll()

        # Do this first.
        #@+<< clear all vnodes and tnodes in the tree >>
        #@-<< clear all vnodes and tnodes in the tree >>

        # Destroy all ivars in subcommanders.
        g.clearAllIvars(c.atFileCommands)
        if c.chapterController:  # New in Leo 4.4.3 b1.
            g.clearAllIvars(c.chapterController)
        g.clearAllIvars(c.fileCommands)
        g.clearAllIvars(c.keyHandler)  # New in Leo 4.4.3 b1.
        g.clearAllIvars(c.importCommands)
        g.clearAllIvars(c.tangleCommands)
        g.clearAllIvars(c.undoer)

        g.clearAllIvars(c)
        g.clearAllIvars(body.colorizer)
        g.clearAllIvars(body)
        g.clearAllIvars(tree)

        # This must be done last.
        frame.destroyAllPanels()
        g.clearAllIvars(frame)

    #@ destroyAllPanels
    def destroyAllPanels(self):
        """Destroy all panels attached to this frame."""

        panels = (
            self.comparePanel,
            self.colorPanel,
            self.findPanel,
            self.fontPanel,
            self.prefsPanel,
        )

        for panel in panels:
            if panel:
                panel.top.destroy()

    #@ destroySelf (swingFrame)
    def destroySelf(self):
        # Remember these: we are about to destroy all of our ivars!
        top = self.top
        c = self.c

        # Indicate that the commander is no longer valid.
        c.exists = False

        # g.trace(self)

        # Important: this destroys all the objects of the commander too.
        self.destroyAllObjects()

        c.exists = False  # Make sure this one ivar has not been destroyed.

        top.destroy()

    #@<2 class swingStatusLineClass
    class swingStatusLineClass:
        '''A class representing the status line.'''

        #@+others
        #@>  ctor
        def __init__(self, c, parentFrame):
            self.c = c
            self.colorTags = []  # list of color names used as tags.
            self.enabled = False
            self.isVisible = False
            self.lastRow = self.lastCol = 0
            self.log = c.frame.log
            # if 'black' not in self.log.colorTags:
            #    self.log.colorTags.append("black")
            self.parentFrame = parentFrame
            self.statusFrame = Tk.Frame(parentFrame, bd=2)
            text = "line 0, col 0"
            width = len(text) + 4
            self.labelWidget = Tk.Label(self.statusFrame, text=text, width=width, anchor="w")
            self.labelWidget.pack(side="left", padx=1)

            bg = self.statusFrame.cget("background")
            self.textWidget = w = g.app.gui.bodyTextWidget(
                self.statusFrame,
                height=1,
                state="disabled",
                bg=bg,
                relief="groove",
                name='status-line',
            )
            self.textWidget.pack(side="left", expand=1, fill="x")
            w.bind("<Button-1>", self.onActivate)
            self.show()

            c.frame.statusFrame = self.statusFrame
            c.frame.statusLabel = self.labelWidget
            c.frame.statusText = self.textWidget

        #@ clear
        def clear(self):
            w = self.textWidget
            if not w:
                return

            w.configure(state="normal")
            w.delete(0, "end")
            w.configure(state="disabled")

        #@ enable, disable & isEnabled
        def disable(self, background=None):
            c = self.c
            w = self.textWidget
            if w:
                if not background:
                    background = self.statusFrame.cget("background")
                w.configure(state="disabled", background=background)
            self.enabled = False
            c.bodyWantsFocus()

        def enable(self, background="white"):
            # g.trace()
            c = self.c
            w = self.textWidget
            if w:
                w.configure(state="normal", background=background)
                c.widgetWantsFocus(w)
            self.enabled = True

        def isEnabled(self):
            return self.enabled

        #@ get
        def get(self):
            w = self.textWidget
            if w:
                return w.getAllText()
            else:
                return ""

        #@ getFrame
        def getFrame(self):
            return self.statusFrame

        #@ onActivate
        def onActivate(self, event=None):
            # Don't change background as the result of simple mouse clicks.
            background = self.statusFrame.cget("background")
            self.enable(background=background)

        #@ pack & show
        def pack(self):
            if not self.isVisible:
                self.isVisible = True
                self.statusFrame.pack(fill="x", pady=1)

        show = pack

        #@ put (leoSwingFrame:statusLineClass)
        def put(self, s, color=None):
            # g.trace('swingStatusLine',self.textWidget,s)

            w = self.textWidget
            if not w:
                g.trace('swingStatusLine', '***** disabled')
                return

            w.configure(state="normal")
            w.insert("end", s)

            if color:
                if color not in self.colorTags:
                    self.colorTags.append(color)
                    w.tag_config(color, foreground=color)
                w.tag_add(color, "end-%dc" % (len(s) + 1), "end-1c")
                w.tag_config("black", foreground="black")
                w.tag_add("black", "end")

            w.configure(state="disabled")

        #@ unpack & hide
        def unpack(self):
            if self.isVisible:
                self.isVisible = False
                self.statusFrame.pack_forget()

        hide = unpack

        #@ update (statusLine)
        def update(self):
            c = self.c
            bodyCtrl = c.frame.body.bodyCtrl

            if g.app.killed or not self.isVisible:
                return

            s = bodyCtrl.getAllText()
            index = bodyCtrl.getInsertPoint()
            row, col = g.convertPythonIndexToRowCol(s, index)
            if col > 0:
                s2 = s[index - col : index]
                s2 = g.toUnicode(s2)
                col = g.computeWidth(s2, c.tab_width)

            # Important: this does not change the focus because labels never get focus.
            self.labelWidget.configure(text="line %d, col %d" % (row, col))
            self.lastRow = row
            self.lastCol = col

        #@-others

    #@< class swingIconBarClass
    class swingIconBarClass:
        '''A class representing the singleton Icon bar'''

        #@+others
        #@>  ctor
        def __init__(self, c, parentFrame):
            self.c = c

            self.buttons = {}
            self.iconFrame = w = Tk.Frame(parentFrame, height="5m", bd=2, relief="groove")
            self.c.frame.iconFrame = self.iconFrame
            self.font = None
            self.parentFrame = parentFrame
            self.visible = False
            self.show()

        #@ add
        def add(self, *args, **keys):
            """Add a button containing text or a picture to the icon bar.

            Pictures take precedence over text"""

            c = self.c
            f = self.iconFrame
            text = keys.get('text')
            imagefile = keys.get('imagefile')
            image = keys.get('image')
            command = keys.get('command')
            bg = keys.get('bg')

            if not imagefile and not image and not text:
                return

            # First define n.
            try:
                g.app.iconWidgetCount += 1
                n = g.app.iconWidgetCount
            except:
                n = g.app.iconWidgetCount = 1

            if not command:

                def command():
                    print("command for widget %s" % (n))

            if imagefile or image:
                #@+<< create a picture >>
                #@> << create a picture >>
                try:
                    if imagefile:
                        # Create the image.  Throws an exception if file not found
                        imagefile = g.os_path_join(g.app.loadDir, imagefile)
                        imagefile = g.os_path_normpath(imagefile)
                        image = Tk.PhotoImage(master=g.app.root, file=imagefile)

                        # Must keep a reference to the image!
                        try:
                            refs = g.app.iconImageRefs
                        except:
                            refs = g.app.iconImageRefs = []

                        refs.append(
                            (imagefile, image),
                        )

                    if not bg:
                        bg = f.cget("bg")

                    b = Tk.Button(f, image=image, relief="flat", bd=0, command=command, bg=bg)
                    b.pack(side="left", fill="y")
                    return b

                except:
                    g.es_exception()
                    return None
                #@-<< create a picture >>
            elif text:
                b = Tk.Button(f, text=text, relief="groove", bd=2, command=command)
                if not self.font:
                    self.font = c.config.getFontFromParams(
                        "button_text_font_family",
                        "button_text_font_size",
                        "button_text_font_slant",
                        "button_text_font_weight",
                    )
                b.configure(font=self.font)
                if bg:
                    b.configure(bg=bg)
                b.pack(side="left", fill="none")
                return b

            return None

        #@< clear
        def clear(self):
            """Destroy all the widgets in the icon bar"""

            f = self.iconFrame

            for slave in f.pack_slaves():
                slave.destroy()
            self.visible = False

            f.configure(height="5m")  # The default height.
            g.app.iconWidgetCount = 0
            g.app.iconImageRefs = []

        #@ deleteButton (new in Leo 4.4.3)
        def deleteButton(self, w):
            w.pack_forget()

        #@ getFrame
        def getFrame(self):
            return self.iconFrame

        #@ pack (show)
        def pack(self):
            """Show the icon bar by repacking it"""

            if not self.visible:
                self.visible = True
                self.iconFrame.pack(fill="x", pady=2)

        show = pack

        #@ setCommandForButton (new in Leo 4.4.3)
        def setCommandForButton(self, b, command):
            b.configure(command=command)

        #@ unpack (hide)
        def unpack(self):
            """Hide the icon bar by unpacking it.

            A later call to show will repack it in a new location."""

            if self.visible:
                self.visible = False
                self.iconFrame.pack_forget()

        hide = unpack
        #@-others

    #@< Minibuffer methods
    #@> showMinibuffer
    def showMinibuffer(self):
        '''Make the minibuffer visible.'''

        frame = self

        if not frame.minibufferVisible:
            frame.minibufferFrame.pack(side='bottom', fill='x')
            frame.minibufferVisible = True

    #@ hideMinibuffer
    def hideMinibuffer(self):
        '''Hide the minibuffer.'''

        frame = self
        if frame.minibufferVisible:
            frame.minibufferFrame.pack_forget()
            frame.minibufferVisible = False

    #@ f.createMiniBufferWidget
    def createMiniBufferWidget(self):
        '''Create the minbuffer below the status line.'''

    #@ f.setMinibufferBindings
    def setMinibufferBindings(self):
        '''Create bindings for the minibuffer..'''

        f = self
        c = f.c
        k = c.k
        w = f.miniBufferWidget

        if not c.useTextMinibuffer:
            return

    #@< Configuration (swingFrame)
    #@> configureBar (swingFrame)
    def configureBar(self, bar, verticalFlag):
        c = self.c

        # Get configuration settings.
        w = c.config.getInt("split_bar_width")
        if not w or w < 1:
            w = 7
        relief = c.config.get("split_bar_relief", "relief")
        if not relief:
            relief = "flat"
        color = c.config.getColor("split_bar_color")
        if not color:
            color = "LightSteelBlue2"

        try:
            if verticalFlag:
                # Panes arranged vertically; horizontal splitter bar
                bar.configure(relief=relief, height=w, bg=color, cursor="sb_v_double_arrow")
            else:
                # Panes arranged horizontally; vertical splitter bar
                bar.configure(relief=relief, width=w, bg=color, cursor="sb_h_double_arrow")
        except:  # Could be a user error. Use all defaults
            g.es("exception in user configuration for splitbar")
            g.es_exception()
            if verticalFlag:
                # Panes arranged vertically; horizontal splitter bar
                bar.configure(height=7, cursor="sb_v_double_arrow")
            else:
                # Panes arranged horizontally; vertical splitter bar
                bar.configure(width=7, cursor="sb_h_double_arrow")

    #@ configureBarsFromConfig (swingFrame)
    def configureBarsFromConfig(self):
        c = self.c

        w = c.config.getInt("split_bar_width")
        if not w or w < 1:
            w = 7

        relief = c.config.get("split_bar_relief", "relief")
        if not relief or relief == "":
            relief = "flat"

        color = c.config.getColor("split_bar_color")
        if not color or color == "":
            color = "LightSteelBlue2"

        if self.splitVerticalFlag:
            bar1, bar2 = self.bar1, self.bar2
        else:
            bar1, bar2 = self.bar2, self.bar1

        try:
            bar1.configure(relief=relief, height=w, bg=color)
            bar2.configure(relief=relief, width=w, bg=color)
        except:  # Could be a user error.
            g.es("exception in user configuration for splitbar")
            g.es_exception()

    #@ reconfigureFromConfig (swingFrame)
    def reconfigureFromConfig(self):
        frame = self
        c = frame.c

        frame.tree.setFontFromConfig()
        ### frame.tree.setColorFromConfig()

        frame.configureBarsFromConfig()

        frame.body.setFontFromConfig()
        frame.body.setColorFromConfigt()

        frame.setTabWidth(c.tab_width)
        frame.log.setFontFromConfig()
        frame.log.setColorFromConfig()

        c.redraw_now()

    #@ setInitialWindowGeometry (swingFrame)
    def setInitialWindowGeometry(self):
        """Set the position and size of the frame to config params."""

        c = self.c

        h = c.config.getInt("initial_window_height") or 500
        w = c.config.getInt("initial_window_width") or 600
        x = c.config.getInt("initial_window_left") or 10
        y = c.config.getInt("initial_window_top") or 10

        if h and w and x and y:
            pass  ### self.setTopGeometry(w,h,x,y)

    #@ setTabWidth (swingFrame)
    def setTabWidth(self, w):
        pass

    #@ setWrap (swingFrame)
    def setWrap(self, p):
        c = self.c
        w = c.frame.body.bodyCtrl

        theDict = g.scanDirectives(c, p)
        if not theDict:
            return

        wrap = theDict.get("wrap")

        ### if self.body.wrapState == wrap: return

        self.body.wrapState = wrap
        # g.trace(wrap)

        ### Rewrite for swing.

    #@ setTopGeometry (swingFrame)
    def setTopGeometry(self, w, h, x, y, adjustSize=True):
        # Put the top-left corner on the screen.
        x = max(10, x)
        y = max(10, y)

        if adjustSize:
            top = self.top
            sw = top.winfo_screenwidth()
            sh = top.winfo_screenheight()

            # Adjust the size so the whole window fits on the screen.
            w = min(sw - 10, w)
            h = min(sh - 10, h)

            # Adjust position so the whole window fits on the screen.
            if x + w > sw:
                x = 10
            if y + h > sh:
                y = 10

        geom = "%dx%d%+d%+d" % (w, h, x, y)

        self.top.geometry(geom)

    #@ reconfigurePanes (use config bar_width) (swingFrame)
    def reconfigurePanes(self):
        c = self.c

        border = c.config.getInt('additional_body_text_border')
        if border == None:
            border = 0

        # The body pane needs a _much_ bigger border when tiling horizontally.
        border = g.choose(self.splitVerticalFlag, 2 + border, 6 + border)
        ### self.bodyCtrl.configure(bd=border)

        # The log pane needs a slightly bigger border when tiling vertically.
        border = g.choose(self.splitVerticalFlag, 4, 2)
        ### self.log.configureBorder(border)

    #@ resizePanesToRatio (swingFrame)
    def resizePanesToRatio(self, ratio, ratio2):
        # g.trace(ratio,ratio2,g.callers())

        self.divideLeoSplitter(self.splitVerticalFlag, ratio)
        self.divideLeoSplitter(not self.splitVerticalFlag, ratio2)

    #@< Event handlers (swingFrame)
    #@> frame.OnCloseLeoEvent
    # Called from quit logic and when user closes the window.
    # Returns True if the close happened.

    def OnCloseLeoEvent(self):
        f = self
        c = f.c

        if c.inCommand:
            # g.trace('requesting window close')
            c.requestCloseWindow = True
        else:
            g.app.closeLeoWindow(self)

    #@ frame.OnControlKeyUp/Down
    def OnControlKeyDown(self, event=None):
        # __pychecker__ = '--no-argsused' # event not used.

        self.controlKeyIsDown = True

    def OnControlKeyUp(self, event=None):
        # __pychecker__ = '--no-argsused' # event not used.

        self.controlKeyIsDown = False

    #@ OnActivateBody (swingFrame)
    def OnActivateBody(self, event=None):
        # __pychecker__ = '--no-argsused' # event not used.

        try:
            frame = self
            c = frame.c
            c.setLog()
            w = c.get_focus()
            if w != c.frame.body.bodyCtrl:
                frame.tree.OnDeactivate()
            c.bodyWantsFocus()
        except:
            g.es_event_exception("activate body")

        return 'break'

    #@ OnActivateLeoEvent, OnDeactivateLeoEvent
    def OnActivateLeoEvent(self, event=None):
        '''Handle a click anywhere in the Leo window.'''

        # __pychecker__ = '--no-argsused' # event.

        self.c.setLog()

    def OnDeactivateLeoEvent(self, event=None):
        pass  # This causes problems on the Mac.

    #@ OnActivateTree
    def OnActivateTree(self, event=None):
        try:
            frame = self
            c = frame.c
            c.setLog()

            if 0:  # Do NOT do this here!
                # OnActivateTree can get called when the tree gets DE-activated!!
                c.bodyWantsFocus()

        except:
            g.es_event_exception("activate tree")

    #@ OnBodyClick, OnBodyRClick (Events)
    def OnBodyClick(self, event=None):
        try:
            c = self.c
            p = c.currentPosition()
            if not g.doHook("bodyclick1", c=c, p=p, v=p, event=event):
                self.OnActivateBody(event=event)
            g.doHook("bodyclick2", c=c, p=p, v=p, event=event)
        except:
            g.es_event_exception("bodyclick")

    def OnBodyRClick(self, event=None):
        try:
            c = self.c
            p = c.currentPosition()
            if not g.doHook("bodyrclick1", c=c, p=p, v=p, event=event):
                pass  # By default Leo does nothing.
            g.doHook("bodyrclick2", c=c, p=p, v=p, event=event)
        except:
            g.es_event_exception("iconrclick")

    #@ OnBodyDoubleClick (Events)
    def OnBodyDoubleClick(self, event=None):
        try:
            c = self.c
            p = c.currentPosition()
            if event and not g.doHook("bodydclick1", c=c, p=p, v=p, event=event):
                c.editCommands.extendToWord(event)  # Handles unicode properly.
            g.doHook("bodydclick2", c=c, p=p, v=p, event=event)
        except:
            g.es_event_exception("bodydclick")

        return "break"  # Restore this to handle proper double-click logic.

    #@ OnMouseWheel (Tomaz Ficko)
    # Contributed by Tomaz Ficko.  This works on some systems.
    # On XP it causes a crash in tcl83.dll.  Clearly a Tk bug.

    def OnMouseWheel(self, event=None):
        try:
            if event.delta < 1:
                self.canvas.yview(Tk.SCROLL, 1, Tk.UNITS)
            else:
                self.canvas.yview(Tk.SCROLL, -1, Tk.UNITS)
        except:
            g.es_event_exception("scroll wheel")

        return "break"

    #@< Gui-dependent commands
    #@> Minibuffer commands... (swingFrame)

    #@> contractPane
    def contractPane(self, event=None):
        '''Contract the selected pane.'''

        f = self
        c = f.c
        w = c.get_requested_focus()
        wname = c.widget_name(w)

        # g.trace(wname)
        if not w:
            return

        if wname.startswith('body'):
            f.contractBodyPane()
        elif wname.startswith('log'):
            f.contractLogPane()
        elif wname.startswith('head') or wname.startswith('canvas'):
            f.contractOutlinePane()

    #@ expandPane
    def expandPane(self, event=None):
        '''Expand the selected pane.'''

        f = self
        c = f.c

        w = c.get_requested_focus()
        wname = c.widget_name(w)

        # g.trace(wname)
        if not w:
            return

        if wname.startswith('body'):
            f.expandBodyPane()
        elif wname.startswith('log'):
            f.expandLogPane()
        elif wname.startswith('head') or wname.startswith('canvas'):
            f.expandOutlinePane()

    #@ fullyExpandPane
    def fullyExpandPane(self, event=None):
        '''Fully expand the selected pane.'''

        f = self
        c = f.c

        w = c.get_requested_focus()
        wname = c.widget_name(w)

        # g.trace(wname)
        if not w:
            return

        if wname.startswith('body'):
            f.fullyExpandBodyPane()
        elif wname.startswith('log'):
            f.fullyExpandLogPane()
        elif wname.startswith('head') or wname.startswith('canvas'):
            f.fullyExpandOutlinePane()

    #@ hidePane
    def hidePane(self, event=None):
        '''Completely contract the selected pane.'''

        f = self
        c = f.c

        w = c.get_requested_focus()
        wname = c.widget_name(w)

        g.trace(wname)
        if not w:
            return

        if wname.startswith('body'):
            f.hideBodyPane()
            c.treeWantsFocus()
        elif wname.startswith('log'):
            f.hideLogPane()
            c.bodyWantsFocus()
        elif wname.startswith('head') or wname.startswith('canvas'):
            f.hideOutlinePane()
            c.bodyWantsFocus()

    #@ expand/contract/hide...Pane
    #
    #     f.splitVerticalFlag: use the primary   (tree/body) ratio.
    # not f.splitVerticalFlag: use the secondary (tree/log) ratio.
    #@@c

    def contractBodyPane(self, event=None):
        '''Contract the body pane.'''
        f = self
        r = min(1.0, f.ratio + 0.1)
        f.divideLeoSplitter(f.splitVerticalFlag, r)

    def contractLogPane(self, event=None):
        '''Contract the log pane.'''
        f = self
        r = min(1.0, f.ratio + 0.1)
        f.divideLeoSplitter(not f.splitVerticalFlag, r)

    def contractOutlinePane(self, event=None):
        '''Contract the outline pane.'''
        f = self
        r = max(0.0, f.ratio - 0.1)
        f.divideLeoSplitter(f.splitVerticalFlag, r)

    def expandBodyPane(self, event=None):
        '''Expand the body pane.'''
        self.contractOutlinePane()

    def expandLogPane(self, event=None):
        '''Expand the log pane.'''
        f = self
        r = max(0.0, f.ratio - 0.1)
        f.divideLeoSplitter(not f.splitVerticalFlag, r)

    def expandOutlinePane(self, event=None):
        '''Expand the outline pane.'''
        self.contractBodyPane()

    #@ fullyExpand/hide...Pane
    def fullyExpandBodyPane(self, event=None):
        '''Fully expand the body pane.'''
        f = self
        f.divideLeoSplitter(f.splitVerticalFlag, 0.0)

    def fullyExpandLogPane(self, event=None):
        '''Fully expand the log pane.'''
        f = self
        f.divideLeoSplitter(not f.splitVerticalFlag, 0.0)

    def fullyExpandOutlinePane(self, event=None):
        '''Fully expand the outline pane.'''
        f = self
        f.divideLeoSplitter(f.splitVerticalFlag, 1.0)

    def hideBodyPane(self, event=None):
        '''Completely contract the body pane.'''
        f = self
        f.divideLeoSplitter(f.splitVerticalFlag, 1.0)

    def hideLogPane(self, event=None):
        '''Completely contract the log pane.'''
        f = self
        f.divideLeoSplitter(not f.splitVerticalFlag, 1.0)

    def hideOutlinePane(self, event=None):
        '''Completely contract the outline pane.'''
        f = self
        f.divideLeoSplitter(f.splitVerticalFlag, 0.0)

    #@< Window Menu...
    #@> toggleActivePane
    def toggleActivePane(self, event=None):
        '''Toggle the focus between the outline and body panes.'''

        frame = self
        c = frame.c

        if c.get_focus() == frame.body.bodyCtrl:  # 2007:10/25
            c.treeWantsFocus()
        else:
            c.endEditing()
            c.bodyWantsFocus()

    #@ cascade
    def cascade(self, event=None):
        '''Cascade all Leo windows.'''

        x, y, delta = 10, 10, 10
        for frame in g.app.windowList:
            top = frame.top

            # Compute w,h
            top.update_idletasks()  # Required to get proper info.
            geom = top.geometry()  # geom = "WidthxHeight+XOffset+YOffset"
            dim, junkx, junky = string.split(geom, '+')
            w, h = string.split(dim, 'x')
            w, h = int(w), int(h)

            # Set new x,y and old w,h
            frame.setTopGeometry(w, h, x, y, adjustSize=False)

            # Compute the new offsets.
            x += 30
            y += 30
            if x > 200:
                x = 10 + delta
                y = 40 + delta
                delta += 10

    #@ equalSizedPanes
    def equalSizedPanes(self, event=None):
        '''Make the outline and body panes have the same size.'''

        frame = self
        frame.resizePanesToRatio(0.5, frame.secondary_ratio)

    #@ hideLogWindow
    def hideLogWindow(self, event=None):
        frame = self
        frame.divideLeoSplitter2(0.99, not frame.splitVerticalFlag)

    #@ minimizeAll
    def minimizeAll(self, event=None):
        '''Minimize all Leo's windows.'''

        self.minimize(g.app.pythonFrame)
        for frame in g.app.windowList:
            self.minimize(frame)
            self.minimize(frame.findPanel)

    def minimize(self, frame):
        if frame and frame.top.state() == "normal":
            frame.top.iconify()

    #@ toggleSplitDirection (swingFrame)
    # The key invariant: self.splitVerticalFlag tells the alignment of the main splitter.

    def toggleSplitDirection(self, event=None):
        '''Toggle the split direction in the present Leo window.'''

        # Switch directions.
        f = self

        # The key invariant: self.splitVerticalFlag
        # tells the alignment of the main splitter.
        f.splitVerticalFlag = not f.splitVerticalFlag
        f.toggleTkSplitDirection(f.splitVerticalFlag)

    #@> toggleTkSplitDirection
    def toggleTkSplitDirection(self, verticalFlag):
        # Abbreviations.
        frame = self
        bar1 = self.bar1
        bar2 = self.bar2
        split1Pane1, split1Pane2 = self.split1Pane1, self.split1Pane2
        split2Pane1, split2Pane2 = self.split2Pane1, self.split2Pane2
        # Reconfigure the bars.
        bar1.place_forget()
        bar2.place_forget()
        self.configureBar(bar1, verticalFlag)
        self.configureBar(bar2, not verticalFlag)
        # Make the initial placements again.
        self.placeSplitter(bar1, split1Pane1, split1Pane2, verticalFlag)
        self.placeSplitter(bar2, split2Pane1, split2Pane2, not verticalFlag)
        # Adjust the log and body panes to give more room around the bars.
        self.reconfigurePanes()
        # Redraw with an appropriate ratio.
        vflag, ratio, secondary_ratio = frame.initialRatios()
        self.resizePanesToRatio(ratio, secondary_ratio)

    #@< resizeToScreen
    def resizeToScreen(self, event=None):
        '''Resize the Leo window so it fill the entire screen.'''

        top = self.top

        w = top.winfo_screenwidth()
        h = top.winfo_screenheight()

        if sys.platform.startswith('win'):
            top.state('zoomed')
        elif sys.platform == 'darwin':
            # Must leave room to get at very small resizing area.
            geom = "%dx%d%+d%+d" % (w - 20, h - 55, 10, 25)
            top.geometry(geom)
        else:
            # Fill almost the entire screen.
            # Works on Windows. YMMV for other platforms.
            geom = "%dx%d%+d%+d" % (w - 8, h - 46, 0, 0)
            top.geometry(geom)

    #@< Help Menu...
    #@> leoHelp
    def leoHelp(self, event=None):
        '''Open Leo's offline tutorial.'''

        frame = self
        c = frame.c

        theFile = g.os_path_join(g.app.loadDir, "..", "doc", "sbooks.chm")

        if g.os_path_exists(theFile):
            os.startfile(theFile)
        else:
            answer = g.app.gui.runAskYesNoDialog(
                c, "Download Tutorial?", "Download tutorial (sbooks.chm) from SourceForge?"
            )

            if answer == "yes":
                try:
                    if 0:  # Download directly.  (showProgressBar needs a lot of work)
                        url = "http://umn.dl.sourceforge.net/sourceforge/leo/sbooks.chm"
                        import urllib

                        self.scale = None
                        urllib.urlretrieve(url, theFile, self.showProgressBar)
                        if self.scale:
                            self.scale.destroy()
                            self.scale = None
                    else:
                        url = "http://prdownloads.sourceforge.net/leo/sbooks.chm?download"
                        import webbrowser

                        os.chdir(g.app.loadDir)
                        webbrowser.open_new(url)
                except:
                    g.es("exception dowloading sbooks.chm")
                    g.es_exception()

    #@> showProgressBar
    def showProgressBar(self, count, size, total):
        # g.trace("count,size,total:",count,size,total)
        if self.scale == None:
            #@+<< create the scale widget >>
            #@> << create the scale widget >>
            top = Tk.Toplevel()
            top.title("Download progress")
            self.scale = scale = Tk.Scale(
                top, state="normal", orient="horizontal", from_=0, to=total
            )
            scale.pack()
            top.lift()
            #@-<< create the scale widget >>
        self.scale.set(count * size)
        self.scale.update_idletasks()

    #@<4 Delayed Focus (swingFrame)
    #
    # Important: This code never calls select, so there can be no race condition here
    # that alters text improperly.
    #@ Tk bindings... (swingFrame)
    def bringToFront(self):
        # g.trace(g.callers())
        self.top.deiconify()
        self.top.lift()

    def getFocus(self):
        """Returns the widget that has focus, or body if None."""
        try:
            # This method is unreliable while focus is changing.
            # The call to update_idletasks may help.  Or not.
            self.top.update_idletasks()
            f = self.top.focus_displayof()
        except Exception:
            f = None
        if f:
            return f
        else:
            return self.body.bodyCtrl

    def getTitle(self):
        return self.top.title()

    def setTitle(self, title):
        return self.top.title(title)

    def get_window_info(self):
        return g.app.gui.get_window_info(self.top)

    def iconify(self):
        self.top.iconify()

    def deiconify(self):
        self.top.deiconify()

    def lift(self):
        self.top.lift()

    def update(self):
        self.top.update()

    #@-others


#@< class leoSwingBody
class leoSwingBody(leoFrame.leoBody):
    #@+others
    #@>  Birth & death
    #@> swingBody. __init__
    def __init__(self, frame, parentFrame):
        g.trace('leoSwingBody')

        # Call the base class constructor.
        leoFrame.leoBody.__init__(self, frame, parentFrame)

        c = self.c
        p = c.currentPosition()
        self.editor_name = None
        self.editor_v = None

        self.trace_onBodyChanged = c.config.getBool('trace_onBodyChanged')
        self.bodyCtrl = self.createControl(parentFrame, p)
        self.colorizer = leoColor.colorizer(c)

    #@ swingBody.createBindings
    def createBindings(self, w=None):
        '''(swingBody) Create gui-dependent bindings.
        These are *not* made in nullBody instances.'''

    #@ swingBody.createControl
    def createControl(self, parentFrame, p):
        c = self.c

        g.trace('swingBody')

        # New in 4.4.1: make the parent frame a PanedWidget.
        self.numberOfEditors = 1
        name = '1'
        self.totalNumberOfEditors = 1

        orient = c.config.getString('editor_orientation') or 'horizontal'
        if orient not in ('horizontal', 'vertical'):
            orient = 'horizontal'

        w = self.createTextWidget(parentFrame, p, name)
        self.editorWidgets[name] = w

        return w

    #@ swingBody.createTextWidget
    def createTextWidget(self, parentFrame, p, name):
        c = self.c

        # parentFrame.configure(bg='LightSteelBlue1')

        wrap = c.config.getBool('body_pane_wraps')
        wrap = g.choose(wrap, "word", "none")

        # Setgrid=1 cause severe problems with the font panel.
        body = w = leoSwingTextWidget(
            parentFrame, name='body-pane', bd=2, bg="white", relief="flat", setgrid=0, wrap=wrap
        )

        # Inject ivars
        if name == '1':
            w.leo_p = None  # Will be set when the second editor is created.
        else:
            w.leo_p = p.copy()
            # pychecker complains body.leo_p does not exist.
        w.leo_active = True
        w.leo_bodyBar = bodyBar
        w.leo_bodyXBar = bodyXBar
        w.leo_chapter = None
        w.leo_frame = parentFrame
        w.leo_name = name
        w.leo_label = None
        w.leo_label_s = None
        w.leo_scrollBarSpot = None
        w.leo_insertSpot = None
        w.leo_selection = None

        return w

    #@< swingBody.setColorFromConfig
    def setColorFromConfig(self, w=None):
        c = self.c
        if w is None:
            w = self.bodyCtrl

        return  ###

        bg = c.config.getColor("body_text_background_color") or 'white'
        # g.trace(id(w),bg)

        try:
            w.configure(bg=bg)
        except:
            g.es("exception setting body text background color")
            g.es_exception()

        fg = c.config.getColor("body_text_foreground_color") or 'black'
        try:
            w.configure(fg=fg)
        except:
            g.es("exception setting body textforeground color")
            g.es_exception()

        bg = c.config.getColor("body_insertion_cursor_color")
        if bg:
            try:
                w.configure(insertbackground=bg)
            except:
                g.es("exception setting body pane cursor color")
                g.es_exception()

        sel_bg = c.config.getColor('body_text_selection_background_color') or 'Gray80'
        try:
            w.configure(selectbackground=sel_bg)
        except Exception:
            g.es("exception setting body pane text selection background color")
            g.es_exception()

        sel_fg = c.config.getColor('body_text_selection_foreground_color') or 'white'
        try:
            w.configure(selectforeground=sel_fg)
        except Exception:
            g.es("exception setting body pane text selection foreground color")
            g.es_exception()

        if sys.platform != "win32":  # Maybe a Windows bug.
            fg = c.config.getColor("body_cursor_foreground_color")
            bg = c.config.getColor("body_cursor_background_color")
            if fg and bg:
                cursor = "xterm" + " " + fg + " " + bg
                try:
                    w.configure(cursor=cursor)
                except:
                    import traceback

                    traceback.print_exc()

    #@ swingBody.setFontFromConfig
    def setFontFromConfig(self, w=None):
        c = self.c

        if not w:
            w = self.bodyCtrl

        font = c.config.getFontFromParams(
            "body_text_font_family",
            "body_text_font_size",
            "body_text_font_slant",
            "body_text_font_weight",
            c.config.defaultBodyFontSize,
        )

        self.fontRef = font  # ESSENTIAL: retain a link to font.
        ### w.configure(font=font)

        # g.trace("BODY",body.cget("font"),font.cget("family"),font.cget("weight"))

    #@ Focus (swingBody)
    def hasFocus(self):
        return self.bodyCtrl == self.frame.top.focus_displayof()

    def setFocus(self):
        self.c.widgetWantsFocus(self.bodyCtrl)

    #@ forceRecolor
    def forceFullRecolor(self):
        self.forceFullRecolorFlag = True

    #@ Tk bindings (swingBbody)
    #@> bind (new)
    def bind(self, *args, **keys):
        pass

    #@ Tags (Tk spelling) (swingBody)
    def tag_add(self, tagName, index1, index2):
        self.bodyCtrl.tag_add(tagName, index1, index2)

    def tag_bind(self, tagName, event, callback):
        self.bodyCtrl.tag_bind(tagName, event, callback)

    def tag_configure(self, colorName, **keys):
        self.bodyCtrl.tag_configure(colorName, keys)

    def tag_delete(self, tagName):
        self.bodyCtrl.tag_delete(tagName)

    def tag_names(self, *args):  # New in Leo 4.4.1.
        return self.bodyCtrl.tag_names(*args)

    def tag_remove(self, tagName, index1, index2):
        return self.bodyCtrl.tag_remove(tagName, index1, index2)

    #@ Configuration (Tk spelling) (swingBody)
    def cget(self, *args, **keys):
        body = self
        w = self.bodyCtrl
        val = w.cget(*args, **keys)

        if g.app.trace:
            g.trace(val, args, keys)

        return val

    def configure(self, *args, **keys):
        # g.trace(args,keys)

        body = self
        w = body.bodyCtrl
        return w.configure(*args, **keys)

    #@ Idle time... (swingBody)
    def scheduleIdleTimeRoutine(self, function, *args, **keys):
        pass  ### self.bodyCtrl.after_idle(function,*args,**keys)

    #@ Menus (swingBody)
    def bind(self, *args, **keys):
        pass  ### return self.bodyCtrl.bind(*args,**keys)

    #@ Text (now in base class) (swingBody)
    # def getAllText (self):              return self.bodyCtrl.getAllText()
    # def getInsertPoint(self):           return self.bodyCtrl.getInsertPoint()
    # def getSelectedText (self):         return self.bodyCtrl.getSelectedText()
    # def getSelectionRange (self,sort=True): return self.bodyCtrl.getSelectionRange(sort)
    # def hasTextSelection (self):        return self.bodyCtrl.hasSelection()
    # # def scrollDown (self):            g.app.gui.yscroll(self.bodyCtrl,1,'units')
    # # def scrollUp (self):              g.app.gui.yscroll(self.bodyCtrl,-1,'units')
    # def see (self,index):               self.bodyCtrl.see(index)
    # def seeInsertPoint (self):          self.bodyCtrl.seeInsertPoint()
    # def selectAllText (self,event=None):
    # w = g.app.gui.eventWidget(event) or self.bodyCtrl
    # return w.selectAllText()
    # def setInsertPoint (self,pos):      return self.bodyCtrl.getInsertPoint(pos)
    # def setSelectionRange (self,sel):
    # i,j = sel
    # self.bodyCtrl.setSelectionRange(i,j)
    #@< Editors (swingBody)
    #@> createEditorFrame
    def createEditorFrame(self, pane):
        f = Tk.Frame(pane)
        f.pack(side='top', expand=1, fill='both')
        return f

    #@ packEditorLabelWidget
    def packEditorLabelWidget(self, w):
        '''Create a Tk label widget.'''

        if not hasattr(w, 'leo_label') or not w.leo_label:
            # g.trace('w.leo_frame',id(w.leo_frame))
            w.pack_forget()
            w.leo_label = Tk.Label(w.leo_frame)
            w.leo_label.pack(side='top')
            w.pack(expand=1, fill='both')

    #@ setEditorColors
    def setEditorColors(self, bg, fg):
        pass

    #@-others


#@<2 class leoSwingKeys
class swingKeyHandlerClass(leoKeys.keyHandlerClass):
    '''swing overrides of base keyHandlerClass.'''

    def __init__(self, c, useGlobalKillbuffer=False, useGlobalRegisters=False):
        # g.trace('swingKeyHandlerClass',c)

        # Init the base class.
        leoKeys.keyHandlerClass.__init__(self, c, useGlobalKillbuffer, useGlobalRegisters)


#@ class leoSwingMenu
class leoSwingMenu(leoMenu.leoMenu):
    #@+others
    #@>  leoSwingMenu.__init__
    def __init__(self, frame):
        if 0:
            ld = io.File(g.app.loadDir)
            ijcl.addToSearchPath(ld)
            ijcl.beginLoading()
            self.font = frame.top.getFont()
            self.executor = java.util.concurrent.Executors.newCachedThreadPool()
            self.queue = java.util.concurrent.LinkedBlockingQueue()
            self.menu_changer = self.MenuChanger(self.queue)
            self.names_and_commands = {}
            self.keystrokes_and_actions = {}

        leoMenu.leoMenu.__init__(self, frame)

    #@ not ready yet
    if 0:
        #@+others
        #@> class MenuChanger
        class MenuChanger(java.lang.Runnable, java.util.concurrent.Callable):
            def __init__(self, queue):
                self.queue = queue

            def run(self):
                ft = java.util.concurrent.FutureTask(self)
                java.awt.EventQueue.invokeLater(ft)

            def call(self):
                menu, name, label, enabled = self.queue.take()
                target = None
                for z in menu.getMenuComponents():
                    if hasattr(z, "getText") and z.getText() == name:
                        target = z
                        break

                if target:
                    target.setText(label)
                    target.setEnabled(enabled)

        #@ print menu stuff...

        #@> defineLeoSwingPrintTable
        def defineLeoSwingPrintTable(self):
            self.printNodeTable = (
                ("Print Current Node", None, lambda event: self.lsp.printNode()),
                ("Print Current Node as HTML", None, lambda event: self.lsp.printNode(type="HTML")),
                ("Print Marked Nodes", None, lambda event: self.lsp.printMarkedNodes()),
                ("Print Marked Nodes as HTML", None, lambda event: self.lsp.printNode(type="HTML")),
            )

            for z in self.printNodeTable:
                self.names_and_commands[z[0]] = z[2]

        #@ createLeoSwingPrintMenu
        def createLeoSwingPrintMenu(self):
            fmenu = self.getMenu("File")

            components = fmenu.getMenuComponents()

            x = 0
            for z in components:
                if hasattr(z, 'getText') and z.getText() == "Recent Files...":
                    break
                x += 1

            spot = x + 1

            pmenu = swing.JMenu("Printing")

            pnodes = swing.JMenu("Print Nodes")
            pmenu.add(pnodes)
            for z in self.printNodeTable:
                item = swing.JMenuItem(z[0])
                item.actionPerformed = z[2]
                pnodes.add(item)

            sep = swing.JSeparator()
            fmenu.add(sep, spot)
            fmenu.add(pmenu, spot + 1)

            print_tree = swing.JMenuItem("Print Tree As Is")
            print_tree.actionPerformed = self.lsp.printTreeAsIs
            pmenu.add(print_tree)
            self.names_and_commands["Print Tree As Is"] = self.lsp.printTreeAsIs
            print_as_more = swing.JMenuItem("Print Outline in More Format")
            print_as_more.actionPerformed = self.lsp.printOutlineAsMore
            self.names_and_commands["Print Outline in More Formet"] = self.lsp.printOutlineAsMore
            pmenu.add(print_as_more)

        #@ createLeoSwingPrint
        def createLeoSwingPrint(self):
            c = self.c
            import leoSwingPrint

            lsp = leoSwingPrint.leoSwingPrint(c)
            menu = lsp.getAsMenu()

            fmenu = self.getMenu("File")

            components = fmenu.getMenuComponents()

            x = 0
            for z in components:
                if hasattr(z, 'getText') and z.getText() == "Recent Files...":
                    break
                x += 1

            spot = x + 1

            sep = swing.JSeparator()
            fmenu.add(sep, spot)
            fmenu.add(menu, spot + 1)

        #@< plugin menu stuff...
        #@> createPluginMenu
        def createPluginMenu(self):
            top = self.getMenu('top')
            oline = self.getMenu('Outline')
            ind = top.getComponentIndex(oline) + 1
            import leoSwingPluginManager

            self.plugin_menu = pmenu = leoSwingPluginManager.createPluginsMenu()
            # self.plugin_menu = pmenu = swing.JMenu( "Plugins" )
            top.add(pmenu, ind)

        #@ createPluginManager
        def createPluginManager(self, event):
            import leoSwingPluginManager as lspm

            lspm.topLevelMenu()

        #@ getPluginMenu
        def getPluginMenu(self):
            return self.plugin_menu

        #@< JythonShell stuff

        #@> openJythonShell
        def openJythonShell(self):
            js = ijcl.getJythonShell()
            jd = js.getDelegate()
            config = g.app.config
            c = self.c

            import leoSwingFrame

            getColorInstance = leoSwingFrame.getColorInstance

            colorconfig = js.getColorConfiguration()
            color = config.getColor(c, "jyshell_background")
            colorconfig.setBackgroundColor(getColorInstance(color, awt.Color.WHITE))

            color = config.getColor(c, "jyshell_foreground")
            colorconfig.setForegroundColor(getColorInstance(color, awt.Color.GRAY))

            color = config.getColor(c, "jyshell_keyword")
            colorconfig.setKeywordColor(getColorInstance(color, awt.Color.GREEN))

            color = config.getColor(c, "jyshell_local")
            colorconfig.setLocalColor(getColorInstance(color, awt.Color.ORANGE))

            color = config.getColor(c, "jyshell_ps1color")
            colorconfig.setPromptOneColor(getColorInstance(color, awt.Color.BLUE))

            color = config.getColor(c, "jyshell_ps2color")
            colorconfig.setPromptTwoColor(getColorInstance(color, awt.Color.GREEN))

            color = config.getColor(c, "jyshell_syntax")
            colorconfig.setSyntaxColor(getColorInstance(color, awt.Color.RED))

            color = config.getColor(c, "jyshell_output")
            colorconfig.setOutColor(getColorInstance(color, awt.Color.GRAY))

            color = config.getColor(c, "jyshell_error")
            colorconfig.setErrColor(getColorInstance(color, awt.Color.RED))

            family = config.get(c, "jyshell_text_font_family", "family")
            size = config.get(c, "jyshell_text_font_size", "size")
            weight = config.get(c, "jyshell_text_font_weight", "weight")
            slant = None
            font = config.getFontFromParams(
                c,
                "jyshell_text_font_family",
                "jyshell_text_font_size",
                None,
                "jyshell_text_font_weight",
            )

            use_bgimage = g.app.config.getBool(c, "jyshell_background_image")
            if use_bgimage:
                image_location = g.app.config.getString(c, "jyshell_image_location@as-filedialog")
                test_if_exists = java.io.File(image_location)
                if test_if_exists.exists():
                    ii = swing.ImageIcon(image_location)
                    alpha = g.app.config.getFloat(c, "jyshell_background_alpha")
                    js.setBackgroundImage(ii.getImage(), float(alpha))

            if font:
                js.setFont(font)

            js.setVisible(True)
            widget = js.getWidget()
            log = self.c.frame.log
            self.addMenuToJythonShell(js)
            log.addTab("JythonShell", widget)
            log.selectTab(widget)

        #@ addMenuToJythonShell
        def addMenuToJythonShell(self, js):
            c = self.c
            jd = js.getDelegate()
            jmenu = swing.JMenu("Leo")
            jd.addToMenu(jmenu)

            e = swing.JMenuItem("Execute Node As Script")
            e.actionPerformed = lambda event, jd=jd: self.fireNodeAsScript(event, jd)
            jmenu.add(e)

            p = swing.JMenuItem("Run Node in Pdb")
            p.actionPerformed = self.getRunNodeInPdb(c, jd)
            jmenu.add(p)

            captext = "Capture Shell Input In Node"
            totext = "Turn Off Shell Input Capture"
            sc = swing.JMenuItem(captext)
            import org.leo.JTextComponentOutputStream as jtcos

            class logcontrol:
                def __init__(self, menu):
                    self.menu = menu
                    self.loging = False
                    self.ostream = jtcos(c.frame.body.editor.editor)

                def __call__(self, event):
                    menu = self.menu
                    loging = self.loging
                    if not loging:
                        js.addLogger(self.ostream)
                        menu.setText(totext)
                        self.loging = True
                    else:
                        js.removeLogger(self.ostream)
                        menu.setText(captext)
                        self.loging = False

            sc.actionPerformed = logcontrol(sc)
            jmenu.add(sc)

            d = swing.JMenuItem("Detach Shell")

            class detacher(java.util.concurrent.Callable):
                def __init__(self, menu):
                    self.menu = menu
                    self.embeded = True
                    js.setCloser(self)

                def call(self):
                    if self.embeded:
                        log = c.frame.log
                        widget = js.getWidget()
                        log.removeTab(widget)
                    else:
                        widget = js.getWidget()
                        parent = widget.getTopLevelAncestor()
                        parent.dispose()

                def __call__(self, event):
                    d = self.menu
                    text = d.getText()
                    if text == "Detach Shell":
                        d.setText("Retach Shell")
                        jf = swing.JFrame("JythonShell")
                        widget = js.getWidget()
                        log = c.frame.log
                        log.removeTab(widget)
                        jf.add(widget)
                        jf.setSize(500, 500)
                        jf.visible = 1
                        self.embeded = False
                    else:
                        d.setText("Detach Shell")
                        widget = js.getWidget()
                        parent = widget.getTopLevelAncestor()
                        parent.dispose()
                        log = c.frame.log
                        log.addTab("JythonShell", widget)
                        log.selectTab(widget)
                        self.embeded = True

            d.actionPerformed = detacher(d)
            jmenu.add(d)

        #@ getInsertNodeIntoShell
        def getInsertNodeIntoShell(self, c, jd):
            jm = swing.JMenuItem("Write Node Into Shell as Reference")

            def writeNode(event):
                cp = c.currentPosition()
                at = c.atFileCommands
                c.fileCommands.assignFileIndices()
                at.write(cp.copy(), nosentinels=True, toString=True, scriptWrite=True)
                data = at.stringOutput

                jtf = self._GetReferenceName(jd, data)
                jtf.rmv_spot = jd.insertWidget(jtf)
                jtf.requestFocusInWindow()

            jm.actionPerformed = writeNode
            return jm

        #@ getInsertReferenceIntoLeo
        def getInsertReferenceIntoLeo(self, jd):
            jmi = swing.JMenuItem("Insert Reference As Node")

            def action(event):
                jtf = self._GetReferenceAsObject(jd, self.c)
                jtf.rmv_spot = jd.insertWidget(jtf)
                jtf.requestFocusInWindow()

            jmi.actionPerformed = action
            return jmi

        #@ getRunNodeInPdb
        def getRunNodeInPdb(self, c, jd):
            def runInPdb(event):
                cp = c.currentPosition()
                name = cp.h
                name = name.split()[0]
                at = c.atFileCommands
                c.fileCommands.assignFileIndices()
                at.write(cp.copy(), nosentinels=True, toString=True, scriptWrite=True)
                data = at.stringOutput

                f = java.io.File.createTempFile("leopdbrun", None)
                pw = java.io.PrintWriter(f)
                pw.println("import pdb")
                pw.println("pdb.set_trace()")
                for z in data.split("\n"):
                    pw.println(z)
                pw.close()
                f.deleteOnExit()
                l = java.util.Vector()
                l.add("execfile( '%s', globals(), locals())" % f.getAbsolutePath())
                jd.processAsScript(l)

            return runInPdb

        #@ fireNodeAsScript
        def fireNodeAsScript(self, event, jd):
            c = self.c
            cp = c.currentPosition()
            at = c.atFileCommands
            c.fileCommands.assignFileIndices()
            at.write(cp.copy(), nosentinels=True, toString=True, scriptWrite=True)
            data = at.stringOutput.split('\n')

            l = java.util.Vector()
            for z in data:
                l.add(java.lang.String(z))

            jd.processAsScript(l)

        #@ class _GetReferenceName
        class _GetReferenceName(swing.JTextField, aevent.KeyListener):
            def __init__(self, jd, data):
                swing.JTextField.__init__(self)
                self.jd = jd
                self.data = data
                border = self.getBorder()
                tborder = sborder.TitledBorder(border)
                tborder.setTitle("Choose Reference Name:")
                self.setBorder(tborder)
                self.addKeyListener(self)
                self.rmv_spot = None

            def keyPressed(self, event):
                kc = event.getKeyChar()
                if kc == '\n':
                    self.execute()
                elif java.lang.Character.isWhitespace(kc):
                    event.consume

            def execute(self):
                self.jd.setReference(self.getText(), self.data)
                if self.rmv_spot:
                    self.jd.remove(self.rmv_spot)
                self.jd.requestFocusInWindow()

            def keyTyped(self, event):
                kc = event.getKeyChar()
                if kc == '\n':
                    return
                elif java.lang.Character.isWhitespace(kc):
                    event.consume()

            def keyReleased(self, event):
                kc = event.getKeyChar()
                if kc == '\n':
                    return
                elif java.lang.Character.isWhitespace(kc):
                    event.consume()

        class _GetReferenceAsObject(_GetReferenceName):
            def __init__(self, jd, c):
                leoSwingMenu._GetReferenceName.__init__(self, jd, None)
                self.c = c
                border = self.getBorder()
                border.setTitle("Which Reference To Insert:")

            def execute(self):
                ref = self.jd.getReference(self.getText())
                if ref:
                    self.c.beginUpdate()
                    pos = self.c.currentPosition()
                    npos = pos.insertAfter()
                    npos.setHeadString("Reference: %s" % self.getText())
                    npos.setTnodeText(str(ref))
                    self.c.endUpdate()
                if self.rmv_spot:
                    self.jd.remove(self.rmv_spot)

        #@< addUserGuide
        def addUserGuide(self):
            help = self.getMenu('Help')
            c = self.c
            help.addSeparator()
            jmi = swing.JCheckBoxMenuItem("View User Guide")
            widgets = []

            def showUserGuide(event):
                if jmi.getState() and not widgets:
                    import leoSwingLeoTutorial

                    lswlt = leoSwingLeoTutorial.leoSwingLeoTutorial()
                    widget = lswlt.getWidget()
                    widgets.append(widget)
                    c.frame.body.addTab("User Guide", widget)
                elif jmi.getState() and widgets:
                    widget = widgets[0]
                    c.frame.body.addTab("User Guide", widget)
                else:
                    widget = widgets[0]
                    c.frame.body.removeTab(widget)

            jmi.actionPerformed = showUserGuide
            help.add(jmi)

        #@ createRecentFilesMenuItems (leoMenu)
        def createRecentFilesMenuItems(self):
            c = self.c
            frame = c.frame
            recentFilesMenu = self.getMenu("Recent Files...")

            # Delete all previous entries.
            if len(recentFilesMenu.getMenuComponents()) != 0:
                deferable = lambda: self.delete_range(recentFilesMenu, 0, len(c.recentFiles) + 2)
                if not swing.SwingUtilities.isEventDispatchThread():
                    dc = DefCallable(deferable)
                    ft = dc.wrappedAsFutureTask()
                    swing.SwingUtilities.invokeAndWait(ft)
                else:
                    deferable()
            # Create the first two entries.
            table = (("Clear Recent Files", None, c.clearRecentFiles), ("-", None, None))
            self.createMenuEntries(recentFilesMenu, table, init=True)

            # Create all the other entries.
            i = 3
            for name in c.recentFiles:

                def callback(event=None, c=c, name=name):  # 12/9/03
                    c.openRecentFile(name)

                label = "%d %s" % (i - 2, g.computeWindowTitle(name))
                self.add_command(recentFilesMenu, label=label, command=callback, underline=0)
                i += 1

        #@ oops
        def oops(self):
            print("leoMenu oops:", g.callerName(2), "should be overridden in subclass")

        #@ Must be overridden in menu subclasses
        #@> 9 Routines with Tk spellings
        def add_cascade(self, parent, label, menu, underline):
            menu.setText(label)

        def add_command(self, menu, **keys):
            if keys['label'] == "Open Python Window":
                keys['command'] = self.openJythonShell

            self.names_and_commands[keys['label']] = keys['command']

            action = self.MenuRunnable(keys['label'], keys['command'], self.c, self.executor)
            jmenu = swing.JMenuItem(action)
            if keys.has_key('accelerator') and keys['accelerator']:
                accel = keys['accelerator']
                acc_list = accel.split('+')
                changeTo = {
                    'Alt': 'alt',
                    'Shift': 'shift',  # translation table
                    'Ctrl': 'ctrl',
                    'UpArrow': 'UP',
                    'DnArrow': 'DOWN',
                    '-': 'MINUS',
                    '+': 'PLUS',
                    '=': 'EQUALS',
                    '[': 'typed [',
                    ']': 'typed ]',
                    '{': 'typed {',
                    '}': 'typed }',
                    'Esc': 'ESCAPE',
                    '.': 'typed .',
                    "`": "typed `",
                    "BkSp": "BACK_SPACE",
                }  # SEE java.awt.event.KeyEvent for further translations
                chg_list = []
                for z in acc_list:
                    if z in changeTo:
                        chg_list.append(changeTo[z])
                    else:
                        chg_list.append(z)
                accelerator = " ".join(chg_list)
                ks = swing.KeyStroke.getKeyStroke(accelerator)
                if ks:
                    self.keystrokes_and_actions[ks] = action
                    jmenu.setAccelerator(ks)
                else:
                    pass
            menu.add(jmenu)
            label = keys['label']
            return jmenu

        def add_separator(self, menu):
            menu.addSeparator()

        def bind(self, bind_shortcut, callback):
            # self.oops()
            pass

        def delete(self, menu, realItemName):
            self.oops()

        def delete_range(self, menu, n1, n2):
            items = menu.getMenuComponents()
            n3 = n1
            components = []
            while 1:
                if n3 == n2:
                    break
                item = menu.getMenuComponent(n3)
                components.append(item)
                n3 += 1

            for z in components:
                menu.remove(z)

        def destroy(self, menu):
            self.oops()

        def insert_cascade(self, parent, index, label, menu, underline):
            self.oops()

        def new_menu(self, parent, tearoff=0):
            jm = swing.JMenu("1")
            # jm = self.LeoMenu( "1" )
            parent.add(jm)
            # jm.setFont( self.font)
            return jm

        #@ 7 Routines with new spellings
        def createMenuBar(self, frame):
            top = frame.top
            self.defineMenuTables()
            topMenu = swing.JMenuBar()
            top.setJMenuBar(topMenu)
            topMenu.setFont(self.font)
            # Do gui-independent stuff.
            self.setMenu("top", topMenu)
            self.createMenusFromTables()
            self.createLeoSwingPrint()
            self.createPluginMenu()
            self.addUserGuide()

        def createOpenWithMenuFromTable(self, table):
            self.oops()

        def defineMenuCallback(self, command, name):
            return command

        def defineOpenWithMenuCallback(self, command):
            self.oops()

        def disableMenu(self, menu, name):
            for z in menu.getMenuComponents():
                if hasattr(z, "getText") and z.getText() == name:
                    z.setEnabled(False)

        def enableMenu(self, menu, name, val):
            for z in menu.getMenuComponents():
                if hasattr(z, "getText") and z.getText() == name:
                    z.setEnabled(bool(val))

        def setMenuLabel(self, menu, name, label, underline=-1, enabled=1):
            item = (menu, name, label, enabled)
            self.queue.offer(item)
            self.executor.submit(self.menu_changer)

        #@ class MenuRunnable
        class MenuRunnable(swing.AbstractAction, java.lang.Runnable):
            def __init__(self, name, command, c, executor):
                swing.AbstractAction.__init__(self, name)
                self.command = command
                self.c = c
                self.name = name
                self.executor = executor

            def run(self):
                self.c.doCommand(self.command, self.name)  # command()

            def actionPerformed(self, aE):
                # print self.command
                # if self.name == 'Save':
                self.executor.submit(self)

                # else:
                #    se

        #@ class MenuExecuteOnSelect
        class MenuExecuteOnSelect(sevent.MenuListener):
            def __init__(self, method):
                self.method = method

            def menuSelected(self, me):
                self.method()

            def menuCanceled(self, me):
                pass

            def menuDeselected(self, me):
                pass

        #@ class LeoMenu
        class LeoMenu(swing.JMenu):
            def __init__(self, *args):
                swing.JMenu.__init__(self, *args)

            def add(self, *items):
                if hasattr(items[0], "setFont"):
                    items[0].setFont(self.getFont())
                return self.super__add(*items)

        #@-others
    #@-others


#@<3 class leoSplash (java.lang.Runnable)
class leoSplash(java.lang.Runnable):
    #@+others
    #@> run (leoSplash)
    def run(self):
        g.trace(g.callers())

        self.splash = splash = swing.JWindow()
        splash.setAlwaysOnTop(1)
        cpane = splash.getContentPane()
        rp = splash.getRootPane()
        tb = swing.border.TitledBorder('Leo')
        tb.setTitleJustification(tb.CENTER)
        rp.setBorder(tb)
        splash.setBackground(awt.Color.ORANGE)
        dimension = awt.Dimension(400, 400)
        splash.setPreferredSize(dimension)
        splash.setSize(400, 400)

        sicon = g.os_path_join(g.app.loadDir, "..", "Icons", "Leosplash.GIF")
        ii = swing.ImageIcon(sicon)
        image = swing.JLabel(ii)
        image.setBackground(awt.Color.ORANGE)
        cpane.add(image)
        self.splashlabel = splashlabel = swing.JLabel("Leo is starting....")
        splashlabel.setBackground(awt.Color.ORANGE)
        splashlabel.setForeground(awt.Color.BLUE)
        cpane.add(splashlabel, awt.BorderLayout.SOUTH)
        w, h = self._calculateCenteredPosition(splash)
        splash.setLocation(w, h)
        splash.visible = True

    #@ utils
    def _calculateCenteredPosition(self, widget):
        size = widget.getPreferredSize()
        height = size.height / 2
        width = size.width / 2
        h, w = self._getScreenPositionForDialog()
        height = h - height
        width = w - width
        return width, height

    def _getScreenPositionForDialog(self):
        tk = awt.Toolkit.getDefaultToolkit()
        dim = tk.getScreenSize()
        h = dim.height / 2
        w = dim.width / 2
        return h, w

    def setText(self, text):
        self.splashlabel.setText(text)

    def hide(self):
        self.splash.visible = 0

    def toBack(self):
        if self.splash.visible:
            self.splash.toBack()

    def toFront(self):
        if self.splash.visible:
            self.splash.setAlwaysOnTop(1)
            self.splash.toFront()

    def isVisible(self):
        return self.splash.visible

    #@-others


#@< class leoSwingLog (REWRITE)
class leoSwingLog(leoFrame.leoLog):
    """A class that represents the log pane of a swing window."""

    #@+others
    #@> swingLog Birth
    #@> swingLog.__init__
    def __init__(self, frame, parentFrame):
        # g.trace("leoSwingLog")

        # Call the base class constructor and calls createControl.
        leoFrame.leoLog.__init__(self, frame, parentFrame)

        self.c = c = frame.c  # Also set in the base constructor, but we need it here.

        self.colorTags = []
        # The list of color names used as tags in present tab.
        # This gest switched by selectTab.

        self.wrap = g.choose(c.config.getBool('log_pane_wraps'), "word", "none")

        # New in 4.4a2: The log pane is a Pmw.Notebook...

        self.nb = None  # The Pmw.Notebook that holds all the tabs.
        self.colorTagsDict = {}  # Keys are page names.  Values are saved colorTags lists.
        self.menu = None  # A menu that pops up on right clicks in the hull or in tabs.

        self.logCtrl = self.createControl(parentFrame)
        self.setFontFromConfig()
        self.setColorFromConfig()

    #@ swingLog.createControl
    def createControl(self, parentFrame):
        return self

    #@ swingLog.finishCreate
    def finishCreate(self):
        # g.trace('swingLog')

        c = self.c
        log = self

        c.searchCommands.openFindTab(show=False)
        c.spellCommands.openSpellTab()
        log.selectTab('Log')

    #@ swingLog.createTextWidget
    def createTextWidget(self, parentFrame):
        self.logNumber += 1

        log = g.app.gui.plainTextWidget(
            parentFrame,
            name="log-%d" % self.logNumber,
            setgrid=0,
            wrap=self.wrap,
            bd=2,
            bg="white",
            relief="flat",
        )

        return log

    #@ swingLog.makeTabMenu
    def makeTabMenu(self, tabName=None):
        '''Create a tab popup menu.'''

    #@< Config & get/saveState
    #@> swingLog.configureBorder & configureFont
    def configureBorder(self, border):
        self.logCtrl.configure(bd=border)

    def configureFont(self, font):
        self.logCtrl.configure(font=font)

    #@ swingLog.getFontConfig
    def getFontConfig(self):
        font = self.logCtrl.cget("font")
        # g.trace(font)
        return font

    #@ swingLog.restoreAllState
    def restoreAllState(self, d):
        '''Restore the log from a dict created by saveAllState.'''

        logCtrl = self.logCtrl

        # Restore the text.
        text = d.get('text')
        logCtrl.insert('end', text)

        # Restore all colors.
        colors = d.get('colors')
        for color in colors.keys():
            if color not in self.colorTags:
                self.colorTags.append(color)
                logCtrl.tag_config(color, foreground=color)
            items = list(colors.get(color))
            while items:
                start, stop = items[0], items[1]
                items = items[2:]
                logCtrl.tag_add(color, start, stop)

    #@ swingLog.saveAllState
    def saveAllState(self):
        '''Return a dict containing all data needed to recreate the log in another widget.'''

        logCtrl = self.logCtrl
        colors = {}

        # Save the text
        text = logCtrl.getAllText()

        # Save color tags.
        tag_names = logCtrl.tag_names()
        for tag in tag_names:
            if tag in self.colorTags:
                colors[tag] = logCtrl.tag_ranges(tag)

        d = {'text': text, 'colors': colors}
        # g.trace('\n',g.dictToString(d))
        return d

    #@ swingLog.setColorFromConfig
    def setColorFromConfig(self):
        c = self.c

        bg = c.config.getColor("log_pane_background_color") or 'white'

        try:
            self.logCtrl.configure(bg=bg)
        except:
            g.es("exception setting log pane background color")
            g.es_exception()

    #@ swingLog.setFontFromConfig
    def SetWidgetFontFromConfig(self, logCtrl=None):
        c = self.c

        if not logCtrl:
            logCtrl = self.logCtrl

        font = c.config.getFontFromParams(
            "log_text_font_family",
            "log_text_font_size",
            "log_text_font_slant",
            "log_text_font_weight",
            c.config.defaultLogFontSize,
        )

        self.fontRef = font  # ESSENTIAL: retain a link to font.
        ### logCtrl.configure(font=font)

        # g.trace("LOG",logCtrl.cget("font"),font.cget("family"),font.cget("weight"))

        bg = c.config.getColor("log_text_background_color")
        if bg:
            try:
                logCtrl.configure(bg=bg)
            except:
                pass

        fg = c.config.getColor("log_text_foreground_color")
        if fg:
            try:
                logCtrl.configure(fg=fg)
            except:
                pass

    setFontFromConfig = SetWidgetFontFromConfig  # Renaming supresses a pychecker warning.

    #@< Focus & update (swingLog)
    #@> swingLog.onActivateLog
    def onActivateLog(self, event=None):
        try:
            self.c.setLog()
            self.frame.tree.OnDeactivate()
            self.c.logWantsFocus()
        except:
            g.es_event_exception("activate log")

    #@ swingLog.hasFocus
    def hasFocus(self):
        return self.c.get_focus() == self.logCtrl

    #@ forceLogUpdate
    def forceLogUpdate(self, s):
        if sys.platform == "darwin":  # Does not work on MacOS X.
            try:
                print(s)  # Don't add a newline.
            except UnicodeError:
                # g.app may not be inited during scripts!
                print(g.toEncodedString(s, 'utf-8'))
        else:
            self.logCtrl.update_idletasks()

    #@< put & putnl (swingLog)
    # with which tab is active.
    #
    # Also, selectTab switches the contents of colorTags, so that is not concern.
    # It may be that Pmw will allow us to dispense with the colorTags logic...
    #@> put
    # All output to the log stream eventually comes here.
    def put(self, s, color=None, tabName='Log'):
        c = self.c

        if g.app.quitting or not c or not c.exists:
            return

        if tabName:
            self.selectTab(tabName)

    #@ putnl
    def putnl(self, tabName='Log'):
        if g.app.quitting:
            return
        if tabName:
            self.selectTab(tabName)

    #@< Tab (TkLog)
    #@> clearTab
    def clearTab(self, tabName, wrap='none'):
        self.selectTab(tabName, wrap=wrap)
        w = self.logCtrl
        w and w.delete(0, 'end')

    #@ createTab
    def createTab(self, tabName, createText=True, wrap='none'):
        pass

    #@ cycleTabFocus
    def cycleTabFocus(self, event=None, stop_w=None):
        '''Cycle keyboard focus between the tabs in the log pane.'''

        c = self.c
        d = self.frameDict  # Keys are page names. Values are Tk.Frames.
        w = d.get(self.tabName)
        # g.trace(self.tabName,w)
        values = d.values()
        if self.numberOfVisibleTabs() > 1:
            i = i2 = values.index(w) + 1
            if i == len(values):
                i = 0
            tabName = d.keys()[i]
            self.selectTab(tabName)
            return

    #@ deleteTab
    def deleteTab(self, tabName, force=False):
        if tabName == 'Log':
            pass

        elif tabName in ('Find', 'Spell') and not force:
            self.selectTab('Log')

        self.c.invalidateFocus()
        self.c.bodyWantsFocus()

    #@ hideTab
    def hideTab(self, tabName):
        # __pychecker__ = '--no-argsused' # tabName

        self.selectTab('Log')

    #@ getSelectedTab
    def getSelectedTab(self):
        return self.tabName

    #@ lower/raiseTab
    def lowerTab(self, tabName):
        self.c.invalidateFocus()
        self.c.bodyWantsFocus()

    def raiseTab(self, tabName):
        self.c.invalidateFocus()
        self.c.bodyWantsFocus()

    #@ numberOfVisibleTabs
    def numberOfVisibleTabs(self):
        return len([val for val in self.frameDict.values() if val != None])

    #@ renameTab
    def renameTab(self, oldName, newName):
        pass

    #@ selectTab
    def selectTab(self, tabName, createText=True, wrap='none'):
        '''Create the tab if necessary and make it active.'''

    #@ setTabBindings
    def setTabBindings(self, tabName):
        '''Set tab bindings'''

    #@ Tab menu callbacks & helpers
    #@> onRightClick & onClick
    def onRightClick(self, event, menu):
        c = self.c
        menu.post(event.x_root, event.y_root)

    def onClick(self, event, tabName):
        self.selectTab(tabName)

    #@ newTabFromMenu
    def newTabFromMenu(self, tabName='Log'):
        self.selectTab(tabName)

        # This is called by getTabName.
        def selectTabCallback(newName):
            return self.selectTab(newName)

        self.getTabName(selectTabCallback)

    #@ renameTabFromMenu
    def renameTabFromMenu(self, tabName):
        if tabName in ('Log', 'Completions'):
            g.es('can not rename %s tab' % (tabName), color='blue')
        else:

            def renameTabCallback(newName):
                return self.renameTab(tabName, newName)

            self.getTabName(renameTabCallback)

    #@ getTabName
    def getTabName(self, exitCallback):
        canvas = self.nb.component('hull')

        # Overlay what is there!
        c = self.c
        f = Tk.Frame(canvas)
        f.pack(side='top', fill='both', expand=1)

        row1 = Tk.Frame(f)
        row1.pack(side='top', expand=0, fill='x', pady=10)
        row2 = Tk.Frame(f)
        row2.pack(side='top', expand=0, fill='x')

        Tk.Label(row1, text='Tab name').pack(side='left')

        e = Tk.Entry(row1, background='white')
        e.pack(side='left')

        def getNameCallback(event=None):
            s = e.get().strip()
            f.pack_forget()
            if s:
                exitCallback(s)

        def closeTabNameCallback(event=None):
            f.pack_forget()

        b = Tk.Button(row2, text='Ok', width=6, command=getNameCallback)
        b.pack(side='left', padx=10)

        b = Tk.Button(row2, text='Cancel', width=6, command=closeTabNameCallback)
        b.pack(side='left')

        g.app.gui.set_focus(c, e)
        e.bind('<Return>', getNameCallback)

    #@<2 swingLog color tab stuff
    def createColorPicker(self, tabName):
        log = self

        #@+<< define colors >>
        #@> << define colors >>
        colors = (
            "gray60",
            "gray70",
            "gray80",
            "gray85",
            "gray90",
            "gray95",
            "snow1",
            "snow2",
            "snow3",
            "snow4",
            "seashell1",
            "seashell2",
            "seashell3",
            "seashell4",
            "AntiqueWhite1",
            "AntiqueWhite2",
            "AntiqueWhite3",
            "AntiqueWhite4",
            "bisque1",
            "bisque2",
            "bisque3",
            "bisque4",
            "PeachPuff1",
            "PeachPuff2",
            "PeachPuff3",
            "PeachPuff4",
            "NavajoWhite1",
            "NavajoWhite2",
            "NavajoWhite3",
            "NavajoWhite4",
            "LemonChiffon1",
            "LemonChiffon2",
            "LemonChiffon3",
            "LemonChiffon4",
            "cornsilk1",
            "cornsilk2",
            "cornsilk3",
            "cornsilk4",
            "ivory1",
            "ivory2",
            "ivory3",
            "ivory4",
            "honeydew1",
            "honeydew2",
            "honeydew3",
            "honeydew4",
            "LavenderBlush1",
            "LavenderBlush2",
            "LavenderBlush3",
            "LavenderBlush4",
            "MistyRose1",
            "MistyRose2",
            "MistyRose3",
            "MistyRose4",
            "azure1",
            "azure2",
            "azure3",
            "azure4",
            "SlateBlue1",
            "SlateBlue2",
            "SlateBlue3",
            "SlateBlue4",
            "RoyalBlue1",
            "RoyalBlue2",
            "RoyalBlue3",
            "RoyalBlue4",
            "blue1",
            "blue2",
            "blue3",
            "blue4",
            "DodgerBlue1",
            "DodgerBlue2",
            "DodgerBlue3",
            "DodgerBlue4",
            "SteelBlue1",
            "SteelBlue2",
            "SteelBlue3",
            "SteelBlue4",
            "DeepSkyBlue1",
            "DeepSkyBlue2",
            "DeepSkyBlue3",
            "DeepSkyBlue4",
            "SkyBlue1",
            "SkyBlue2",
            "SkyBlue3",
            "SkyBlue4",
            "LightSkyBlue1",
            "LightSkyBlue2",
            "LightSkyBlue3",
            "LightSkyBlue4",
            "SlateGray1",
            "SlateGray2",
            "SlateGray3",
            "SlateGray4",
            "LightSteelBlue1",
            "LightSteelBlue2",
            "LightSteelBlue3",
            "LightSteelBlue4",
            "LightBlue1",
            "LightBlue2",
            "LightBlue3",
            "LightBlue4",
            "LightCyan1",
            "LightCyan2",
            "LightCyan3",
            "LightCyan4",
            "PaleTurquoise1",
            "PaleTurquoise2",
            "PaleTurquoise3",
            "PaleTurquoise4",
            "CadetBlue1",
            "CadetBlue2",
            "CadetBlue3",
            "CadetBlue4",
            "turquoise1",
            "turquoise2",
            "turquoise3",
            "turquoise4",
            "cyan1",
            "cyan2",
            "cyan3",
            "cyan4",
            "DarkSlateGray1",
            "DarkSlateGray2",
            "DarkSlateGray3",
            "DarkSlateGray4",
            "aquamarine1",
            "aquamarine2",
            "aquamarine3",
            "aquamarine4",
            "DarkSeaGreen1",
            "DarkSeaGreen2",
            "DarkSeaGreen3",
            "DarkSeaGreen4",
            "SeaGreen1",
            "SeaGreen2",
            "SeaGreen3",
            "SeaGreen4",
            "PaleGreen1",
            "PaleGreen2",
            "PaleGreen3",
            "PaleGreen4",
            "SpringGreen1",
            "SpringGreen2",
            "SpringGreen3",
            "SpringGreen4",
            "green1",
            "green2",
            "green3",
            "green4",
            "chartreuse1",
            "chartreuse2",
            "chartreuse3",
            "chartreuse4",
            "OliveDrab1",
            "OliveDrab2",
            "OliveDrab3",
            "OliveDrab4",
            "DarkOliveGreen1",
            "DarkOliveGreen2",
            "DarkOliveGreen3",
            "DarkOliveGreen4",
            "khaki1",
            "khaki2",
            "khaki3",
            "khaki4",
            "LightGoldenrod1",
            "LightGoldenrod2",
            "LightGoldenrod3",
            "LightGoldenrod4",
            "LightYellow1",
            "LightYellow2",
            "LightYellow3",
            "LightYellow4",
            "yellow1",
            "yellow2",
            "yellow3",
            "yellow4",
            "gold1",
            "gold2",
            "gold3",
            "gold4",
            "goldenrod1",
            "goldenrod2",
            "goldenrod3",
            "goldenrod4",
            "DarkGoldenrod1",
            "DarkGoldenrod2",
            "DarkGoldenrod3",
            "DarkGoldenrod4",
            "RosyBrown1",
            "RosyBrown2",
            "RosyBrown3",
            "RosyBrown4",
            "IndianRed1",
            "IndianRed2",
            "IndianRed3",
            "IndianRed4",
            "sienna1",
            "sienna2",
            "sienna3",
            "sienna4",
            "burlywood1",
            "burlywood2",
            "burlywood3",
            "burlywood4",
            "wheat1",
            "wheat2",
            "wheat3",
            "wheat4",
            "tan1",
            "tan2",
            "tan3",
            "tan4",
            "chocolate1",
            "chocolate2",
            "chocolate3",
            "chocolate4",
            "firebrick1",
            "firebrick2",
            "firebrick3",
            "firebrick4",
            "brown1",
            "brown2",
            "brown3",
            "brown4",
            "salmon1",
            "salmon2",
            "salmon3",
            "salmon4",
            "LightSalmon1",
            "LightSalmon2",
            "LightSalmon3",
            "LightSalmon4",
            "orange1",
            "orange2",
            "orange3",
            "orange4",
            "DarkOrange1",
            "DarkOrange2",
            "DarkOrange3",
            "DarkOrange4",
            "coral1",
            "coral2",
            "coral3",
            "coral4",
            "tomato1",
            "tomato2",
            "tomato3",
            "tomato4",
            "OrangeRed1",
            "OrangeRed2",
            "OrangeRed3",
            "OrangeRed4",
            "red1",
            "red2",
            "red3",
            "red4",
            "DeepPink1",
            "DeepPink2",
            "DeepPink3",
            "DeepPink4",
            "HotPink1",
            "HotPink2",
            "HotPink3",
            "HotPink4",
            "pink1",
            "pink2",
            "pink3",
            "pink4",
            "LightPink1",
            "LightPink2",
            "LightPink3",
            "LightPink4",
            "PaleVioletRed1",
            "PaleVioletRed2",
            "PaleVioletRed3",
            "PaleVioletRed4",
            "maroon1",
            "maroon2",
            "maroon3",
            "maroon4",
            "VioletRed1",
            "VioletRed2",
            "VioletRed3",
            "VioletRed4",
            "magenta1",
            "magenta2",
            "magenta3",
            "magenta4",
            "orchid1",
            "orchid2",
            "orchid3",
            "orchid4",
            "plum1",
            "plum2",
            "plum3",
            "plum4",
            "MediumOrchid1",
            "MediumOrchid2",
            "MediumOrchid3",
            "MediumOrchid4",
            "DarkOrchid1",
            "DarkOrchid2",
            "DarkOrchid3",
            "DarkOrchid4",
            "purple1",
            "purple2",
            "purple3",
            "purple4",
            "MediumPurple1",
            "MediumPurple2",
            "MediumPurple3",
            "MediumPurple4",
            "thistle1",
            "thistle2",
            "thistle3",
            "thistle4",
        )
        #@-<< define colors >>

        parent = log.frameDict.get(tabName)
        w = log.textDict.get(tabName)
        w.pack_forget()

        colors = list(colors)
        bg = parent.cget('background')

        outer = Tk.Frame(parent, background=bg)
        outer.pack(side='top', fill='both', expand=1, pady=10)

        f = Tk.Frame(outer)
        f.pack(side='top', expand=0, fill='x')
        f1 = Tk.Frame(f)
        f1.pack(side='top', expand=0, fill='x')
        f2 = Tk.Frame(f)
        f2.pack(side='top', expand=1, fill='x')
        f3 = Tk.Frame(f)
        f3.pack(side='top', expand=1, fill='x')

        label = g.app.gui.plainTextWidget(f1, height=1, width=20)
        label.insert('1.0', 'Color name or value...')
        label.pack(side='left', pady=6)

        #@+<< create optionMenu and callback >>
        #@ << create optionMenu and callback >>
        colorBox = Pmw.ComboBox(f2, scrolledlist_items=colors)
        colorBox.pack(side='left', pady=4)

        def colorCallback(newName):
            label.delete('1.0', 'end')
            label.insert('1.0', newName)
            try:
                for theFrame in (parent, outer, f, f1, f2, f3):
                    theFrame.configure(background=newName)
            except:
                pass  # Ignore invalid names.

        colorBox.configure(selectioncommand=colorCallback)

        #@-<< create optionMenu and callback >>
        #@+<< create picker button and callback >>
        #@ << create picker button and callback >>
        def pickerCallback():
            rgb, val = swingColorChooser.askcolor(parent=parent, initialcolor=f.cget('background'))
            if rgb or val:
                # label.configure(text=val)
                label.delete('1.0', 'end')
                label.insert('1.0', val)
                for theFrame in (parent, outer, f, f1, f2, f3):
                    theFrame.configure(background=val)

        b = Tk.Button(f3, text="Color Picker...", command=pickerCallback, background=bg)
        b.pack(side='left', pady=4)
        #@-<< create picker button and callback >>

    #@< swingLog font tab stuff
    #@> createFontPicker
    def createFontPicker(self, tabName):
        log = self
        parent = log.frameDict.get(tabName)
        w = log.textDict.get(tabName)
        w.pack_forget()

        bg = parent.cget('background')
        font = self.getFont()
        #@+<< create the frames >>
        #@> << create the frames >>
        f = Tk.Frame(parent, background=bg)
        f.pack(side='top', expand=0, fill='both')
        f1 = Tk.Frame(f, background=bg)
        f1.pack(side='top', expand=1, fill='x')
        f2 = Tk.Frame(f, background=bg)
        f2.pack(side='top', expand=1, fill='x')
        f3 = Tk.Frame(f, background=bg)
        f3.pack(side='top', expand=1, fill='x')
        f4 = Tk.Frame(f, background=bg)
        f4.pack(side='top', expand=1, fill='x')
        #@-<< create the frames >>
        #@+<< create the family combo box >>
        #@ << create the family combo box >>
        names = swingFont.families()
        names = list(names)
        names.sort()
        names.insert(0, '<None>')

        self.familyBox = familyBox = Pmw.ComboBox(
            f1,
            labelpos="we",
            label_text='Family:',
            label_width=10,
            label_background=bg,
            arrowbutton_background=bg,
            scrolledlist_items=names,
        )

        familyBox.selectitem(0)
        familyBox.pack(side="left", padx=2, pady=2)
        #@-<< create the family combo box >>
        #@+<< create the size entry >>
        #@ << create the size entry >>
        Tk.Label(f2, text="Size:", width=10, background=bg).pack(side="left")

        sizeEntry = Tk.Entry(f2, width=4)
        sizeEntry.insert(0, '12')
        sizeEntry.pack(side="left", padx=2, pady=2)
        #@-<< create the size entry >>
        #@+<< create the weight combo box >>
        #@ << create the weight combo box >>
        weightBox = Pmw.ComboBox(
            f3,
            labelpos="we",
            label_text="Weight:",
            label_width=10,
            label_background=bg,
            arrowbutton_background=bg,
            scrolledlist_items=['normal', 'bold'],
        )

        weightBox.selectitem(0)
        weightBox.pack(side="left", padx=2, pady=2)
        #@-<< create the weight combo box >>
        #@+<< create the slant combo box >>
        #@-<< create the slant combo box >>
        #@+<< create the sample text widget >>
        #@ << create the sample text widget >>
        self.sampleWidget = sample = g.app.gui.plainTextWidget(f, height=20, width=80, font=font)
        sample.pack(side='left')

        s = 'The quick brown fox\njumped over the lazy dog.\n0123456789'
        sample.insert(0, s)

        #@-<< create the sample text widget >>
        #@+<< create and bind the callbacks >>
        #@ << create and bind the callbacks >>
        def fontCallback(event=None):
            self.setFont(familyBox, sizeEntry, slantBox, weightBox, sample)

        for w in (familyBox, slantBox, weightBox):
            w.configure(selectioncommand=fontCallback)

        sizeEntry.bind('<Return>', fontCallback)
        #@-<< create and bind the callbacks >>
        self.createBindings()

    #@< createBindings (fontPicker)
    def createBindings(self):
        pass

    #@ getFont
    def getFont(self, family=None, size=12, slant='roman', weight='normal'):
        try:
            return swingFont.Font(family=family, size=size, slant=slant, weight=weight)
        except Exception:
            g.es("exception setting font")
            g.es("family,size,slant,weight:", family, size, slant, weight)
            # g.es_exception() # This just confuses people.
            return g.app.config.defaultFont

    #@ setFont
    def setFont(self, familyBox, sizeEntry, slantBox, weightBox, label):
        d = {}
        for box, key in (
            (familyBox, 'family'),
            (None, 'size'),
            (slantBox, 'slant'),
            (weightBox, 'weight'),
        ):
            if box:
                val = box.get()
            else:
                val = sizeEntry.get().strip() or ''
                try:
                    int(val)
                except ValueError:
                    val = None
            if val and val.lower() not in (
                'none',
                '<none>',
            ):
                d[key] = val

        family = d.get('family', None)
        size = d.get('size', 12)
        weight = d.get('weight', 'normal')
        slant = d.get('slant', 'roman')
        font = self.getFont(family, size, slant, weight)
        label.configure(font=font)

    #@ hideFontTab
    def hideFontTab(self, event=None):
        c = self.c
        c.frame.log.selectTab('Log')
        c.bodyWantsFocus()

    #@-others


#@<2 class leoSwingTreeTab (REWRITE)
class leoSwingTreeTab(leoFrame.leoTreeTab):
    '''A class representing a tabbed outline pane drawn with swing.'''

    #@+others
    #@>  Birth & death
    #@>  ctor (leoTreeTab)
    def __init__(self, c, parentFrame, chapterController):
        leoFrame.leoTreeTab.__init__(self, c, chapterController, parentFrame)
        # Init the base class.  Sets self.c, self.cc and self.parentFrame.

        self.tabNames = []  # The list of tab names.  Changes when tabs are renamed.

        self.createControl()

    #@ tt.createControl
    def createControl(self):
        tt = self
        c = tt.c

        # Create the main container.
        tt.frame = Tk.Frame(c.frame.iconFrame)
        tt.frame.pack(side="left")

        # Create the chapter menu.
        self.chapterVar = var = Tk.StringVar()
        var.set('main')

        tt.chapterMenu = menu = Pmw.OptionMenu(
            tt.frame,
            labelpos='w',
            label_text='chapter',
            menubutton_textvariable=var,
            items=[],
            command=tt.selectTab,
        )
        menu.pack(side='left', padx=5)

    #@< Tabs...
    #@> tt.createTab
    def createTab(self, tabName, select=True):
        tt = self

        if tabName not in tt.tabNames:
            tt.tabNames.append(tabName)
            tt.setNames()

    #@ tt.destroyTab
    def destroyTab(self, tabName):
        tt = self

        if tabName in tt.tabNames:
            tt.tabNames.remove(tabName)
            tt.setNames()

    #@ tt.selectTab
    def selectTab(self, tabName):
        tt = self

        if tabName not in self.tabNames:
            tt.createTab(tabName)

        tt.cc.selectChapterByName(tabName)

    #@ tt.setTabLabel
    def setTabLabel(self, tabName):
        tt = self
        tt.chapterVar.set(tabName)

    #@ tt.setNames
    def setNames(self):
        '''Recreate the list of items.'''

        tt = self
        names = tt.tabNames[:]
        if 'main' in names:
            names.remove('main')
        names.sort()
        names.insert(0, 'main')
        tt.chapterMenu.setitems(names)

    #@-others


#@<2 class leoSwingTextWidget (revise)
class leoSwingTextWidget:  ### (leoFrame.baseTextWidget):
    '''A class to wrap the Tk.Text widget.
    Translates Python (integer) indices to and from Tk (string) indices.

    This class inherits almost all swingText methods: you call use them as usual.'''

    # The signatures of tag_add and insert are different from the Tk.Text signatures.
    # __pychecker__ = '--no-override' # suppress warning about changed signature.

    def __repr__(self):
        name = hasattr(self, '_name') and self._name or '<no name>'
        return 'swingTextWidget id: %s name: %s' % (id(self), name)

    #@+others
    #@> swingTextWidget.__init__
    def __init__(self, parentFrame, *args, **keys):
        # Create the actual gui widget.

        # To do: probably need to subclass JTextField so we can inject ivars.

        self.widget = w = swing.JTextField()  ###preferredSize=(200,20))
        parentFrame.contentPane.add(w)

        # Probably should be somewhere else.
        parentFrame.pack()
        parentFrame.show()

    #@ bindings (not used)
    # Specify the names of widget-specific methods.
    # These particular names are the names of wx.TextCtrl methods.

    # def _appendText(self,s):            return self.widget.insert(s)
    # def _get(self,i,j):                 return self.widget.get(i,j)
    # def _getAllText(self):              return self.widget.get('1.0','end')
    # def _getFocus(self):                return self.widget.focus_get()
    # def _getInsertPoint(self):          return self.widget.index('insert')
    # def _getLastPosition(self):         return self.widget.index('end')
    # def _getSelectedText(self):         return self.widget.get('sel.start','sel.end')
    # def _getSelectionRange(self):       return self.widget.index('sel.start'),self.widget.index('sel.end')
    # def _hitTest(self,pos):             pass ###
    # def _insertText(self,i,s):          return self.widget.insert(i,s)
    # def _scrollLines(self,n):           pass ###
    # def _see(self,i):                   return self.widget.see(i)
    # def _setAllText(self,s):            self.widget.delete('1.0','end') ; self.widget.insert('1.0',s)
    # def _setBackgroundColor(self,color): return self.widget.configure(background=color)
    # def _setFocus(self):                return self.widget.focus_set()
    # def _setInsertPoint(self,i):        return self.widget.mark_set('insert',i)
    # # def _setSelectionRange(self,i,j):   return self.widget.SetSelection(i,j)
    #@ Index conversion (swingTextWidget)
    #@> w.toGuiIndex
    def toGuiIndex(self, i, s=None):
        '''Convert a Python index to a Tk index as needed.'''
        w = self
        if i is None:
            g.trace('can not happen: i is None', g.callers())
            return '1.0'
        elif type(i) == type(99):
            # The 's' arg supports the threaded colorizer.
            if s is None:
                # This *must* be 'end-1c', even if other code must change.
                s = ''  ### s = Tk.Text.get(w,'1.0','end-1c')
            row, col = g.convertPythonIndexToRowCol(s, i)
            i = '%s.%s' % (row + 1, col)
            # g.trace(len(s),i,repr(s))
        else:
            try:
                i = 0  ### i = Tk.Text.index(w,i)
            except Exception:
                # g.es_exception()
                g.trace('Tk.Text.index failed:', repr(i), g.callers())
                i = '1.0'
        return i

    #@ w.toPythonIndex
    def toPythonIndex(self, i):
        '''Convert a Tk index to a Python index as needed.'''
        w = self
        if i is None:
            g.trace('can not happen: i is None')
            return 0
        elif type(i) in (type('a')):
            s = ''  ### s = Tk.Text.get(w,'1.0','end') # end-1c does not work.
            i = '1.0'  ### i = Tk.Text.index(w,i) # Convert to row/column form.
            row, col = i.split('.')
            row, col = int(row), int(col)
            row -= 1
            i = g.convertRowColToPythonIndex(s, row, col)
            # g.es_print(i)
        return i

    #@ w.rowColToGuiIndex
    # This method is called only from the colorizer.
    # It provides a huge speedup over naive code.

    def rowColToGuiIndex(self, s, row, col):
        return '%s.%s' % (row + 1, col)

    #@< getName (Tk.Text)
    def getName(self):
        w = self
        return hasattr(w, '_name') and w._name or repr(w)

    #@ _setSelectionRange
    if 0:

        def _setSelectionRange(self, i, j, insert=None):
            w = self.widget

            i, j = w.toGuiIndex(i), w.toGuiIndex(j)

            # g.trace('i,j,insert',repr(i),repr(j),repr(insert),g.callers())

            # g.trace('i,j,insert',i,j,repr(insert))
            if w.compare(w, i, ">", j):
                i, j = j, i
            w.tag_remove(w, "sel", "1.0", i)
            w.tag_add(w, "sel", i, j)
            w.tag_remove(w, "sel", j, "end")

            if insert is not None:
                w.setInsertPoint(insert)

    #@ Wrapper methods (swingTextWidget)
    #@> after_idle (new)
    def after_idle(self, *args, **keys):
        pass

    #@ bind (new)
    def bind(self, *args, **keys):
        pass

    #@ delete
    def delete(self, i, j=None):
        w = self
        i = w.toGuiIndex(i)

        if j is None:
            pass  ### Tk.Text.delete(w,i)
        else:
            j = w.toGuiIndex(j)
            pass  ### Tk.Text.delete(w,i,j)

    #@ flashCharacter
    def flashCharacter(self, i, bg='white', fg='red', flashes=3, delay=75):  # swingTextWidget.
        pass

    #@ get
    def get(self, i, j=None):
        w = self
        i = w.toGuiIndex(i)

        if j is None:
            return ''  ### return Tk.Text.get(w,i)
        else:
            j = w.toGuiIndex(j)
            return  ### return Tk.Text.get(w,i,j)

    #@ getAllText
    def getAllText(self):  # swingTextWidget.
        """Return all the text of Tk.Text widget w converted to unicode."""

        w = self
        s = ''

        if s is None:
            return g.u('')
        else:
            return g.toUnicode(s)

    #@ getInsertPoint
    def getInsertPoint(self):  # swingTextWidget.
        w = self
        i = 0  ### i = Tk.Text.index(w,'insert')
        i = w.toPythonIndex(i)
        return i

    #@ getSelectedText
    def getSelectedText(self):  # swingTextWidget.
        w = self
        i, j = w.getSelectionRange()
        if i != j:
            i, j = w.toGuiIndex(i), w.toGuiIndex(j)
            s = ''  ### s = Tk.Text.get(w,i,j)
            return g.toUnicode(s)
        else:
            return g.u('')

    #@ getSelectionRange
    def getSelectionRange(self, sort=True):  # swingTextWidget.
        """Return a tuple representing the selected range.

        Return a tuple giving the insertion point if no range of text is selected."""

        w = self
        sel = 0, 0  ### sel = Tk.Text.tag_ranges(w,"sel")
        if len(sel) == 2:
            i, j = sel
        else:
            i = j = 0  ### i = j = Tk.Text.index(w,"insert")

        i, j = w.toPythonIndex(i), w.toPythonIndex(j)
        if sort and i > j:
            i, j = j, i
        return i, j

    #@ getYScrollPosition
    def getYScrollPosition(self):
        w = self
        return 0  ### return w.yview()

    #@ getWidth
    def getWidth(self):
        '''Return the width of the widget.
        This is only called for headline widgets,
        and gui's may choose not to do anything here.'''

        w = self
        return 0  ### return w.cget('width')

    #@ hasSelection
    def hasSelection(self):
        w = self
        i, j = w.getSelectionRange()
        return i != j

    #@ insert
    # The signature is more restrictive than the Tk.Text.insert method.

    def insert(self, i, s):
        w = self
        i = w.toGuiIndex(i)
        ### Tk.Text.insert(w,i,s)

    #@ indexIsVisible (swing)
    def indexIsVisible(self, i):
        w = self

        return True  ### return w.dlineinfo(i)

    #@ replace
    def replace(self, i, j, s):  # swingTextWidget
        w = self
        i, j = w.toGuiIndex(i), w.toGuiIndex(j)

    #@ see
    def see(self, i):  # swingTextWidget.
        w = self
        i = w.toGuiIndex(i)
        ### Tk.Text.see(w,i)

    #@ seeInsertPoint
    def seeInsertPoint(self):  # swingTextWidget.
        w = self
        ### Tk.Text.see(w,'insert')

    #@ selectAllText
    def selectAllText(self, insert=None):  # swingTextWidget
        '''Select all text of the widget, *not* including the extra newline.'''

        w = self
        s = w.getAllText()
        if insert is None:
            insert = len(s)
        w.setSelectionRange(0, len(s), insert=insert)

    #@ setAllText
    def setAllText(self, s):  # swingTextWidget
        pass

    #@ setBackgroundColor
    def setBackgroundColor(self, color):
        w = self
        w.configure(background=color)

    #@ setInsertPoint
    def setInsertPoint(self, i):  # swingTextWidget.
        w = self
        i = w.toGuiIndex(i)

    #@ setSelectionRange
    def setSelectionRange(self, i, j, insert=None):  # swingTextWidget
        pass

    #@ setYScrollPosition
    def setYScrollPosition(self, i):
        w = self
        w.yview('moveto', i)

    #@ setWidth
    def setWidth(self, width):
        '''Set the width of the widget.
        This is only called for headline widgets,
        and gui's may choose not to do anything here.'''

        w = self
        w.configure(width=width)

    #@ tag_add
    def tag_add(self, tagName, i, j=None, *args):
        pass

    #@ tag_configure (NEW)
    def tag_configure(self, *args, **keys):
        pass

    tag_config = tag_configure

    #@ tag_ranges
    def tag_ranges(self, tagName):
        w = self
        aList = []  ### aList = Tk.Text.tag_ranges(w,tagName)
        aList = [w.toPythonIndex(z) for z in aList]
        return tuple(aList)

    #@ tag_remove
    def tag_remove(self, tagName, i, j=None, *args):
        w = self
        i = w.toGuiIndex(i)

        if j is None:
            pass  ### Tk.Text.tag_remove(w,tagName,i,*args)
        else:
            j = w.toGuiIndex(j)
            ### Tk.Text.tag_remove(w,tagName,i,j,*args)

    #@ w.deleteTextSelection
    def deleteTextSelection(self):  # swingTextWidget
        pass

    #@ xyToGui/PythonIndex
    def xyToGuiIndex(self, x, y):  # swingTextWidget
        w = self
        return 0  ### return Tk.Text.index(w,"@%d,%d" % (x,y))

    def xyToPythonIndex(self, x, y):  # swingTextWidget
        w = self
        i = 0  ### i = Tk.Text.index(w,"@%d,%d" % (x,y))
        i = w.toPythonIndex(i)
        return i

    #@-others


#@<2 class leoSwingTree (REWRITE)
class leoSwingTree(leoFrame.leoTree):
    callbacksInjected = False

    """Leo swing tree class."""

    #@+others
    #@>   Notes
    #@@killcolor
    #@> Changes made since first update
    #
    # - disabled drawing of user icons. They weren't being hidden, which messed upscrolling.
    # - Expanded clickBox so all clicks fall inside it.
    # - Added binding for plugBox so it doesn't interfere with the clickBox.  Another weirdness.
    # - Re-enabled code in drawText that sets the headline state.
    # - eventToPosition now returns p.copy, which means that nobody can change the list.
    # - Likewise, clear self.iconIds so old icon id's don't confuse findVnodeWithIconId.
    # - All drawing methods must do p = p.copy() at the beginning if they make any changes to p.
    #     - This ensures neither they nor their allies can change the caller's position.
    #     - In fact, though, only drawTree changes position.  It makes a copy before calling drawNode.
    #     *** Therefore, all positions in the drawing code are immutable!
    #
    # - Fixed the race conditions that caused drawing sometimes to fail. The essential
    #   idea is that we must not call w.config if we are about to do a redraw. For
    #   full details, see the Notes node in the Race Conditions section.
    #@ Changes made since second update
    #
    # - Removed duplicate code in tree.select.
    #   The following code was being called twice (!!):
    #     self.endEditLabel()
    #     self.setUnselectedLabelState(old_p)
    #
    # - Add p.copy() instead of p when inserting nodes into data structures in select.
    #
    # - Fixed a _major_ bug in Leo's core. c.setCurrentPosition must COPY the position
    #   given to it! It's _not_ enough to return a copy of position: it may already
    #   have changed!!
    #
    # - Fixed a another (lesser??) bug in Leo's core. handleUserClick should also make
    #   a copy.
    #
    # - Fixed bug in mod_scripting.py.  The callback was failing if the script was empty.
    #
    # - Put in the self.recycle ivar AND THE CODE STILL FAILS. It seems to me that
    #   this shows there is a bug in my code somewhere, but where??
    #@ Most recent changes
    #
    # - Added generation count.
    #     - Incremented on each redraw.
    #     - Potentially a barrior to race conditions,
    #       but it never seemed to do anything.
    #     - This code is a candidate for elimination.
    #
    # - Used vnodes rather than positions in several places.
    #     - I actually don't think this was involved in the real problem,
    #       and it doesn't hurt.
    #
    # - Added much better traces: the beginning of the end for the bugs :-)
    #     - Added self.verbose option.
    #     - Added align keyword option to g.trace.
    #     - Separate each set of traces by a blank line.
    #         - This makes clear the grouping of id's.
    #
    # - Defensive code: Disable dragging at start of redraw code.
    #     - This protects against race conditions.
    #
    # - Fixed blunder 1: Fixed a number of bugs in the dragging code.
    #     - I had never looked at this code!
    #     - Eliminating false drags greatly simplifies matters.
    #
    # - Fixed blunder 2: Added the following to eventToPosition:
    #         x = canvas.canvasx(x)
    #         y = canvas.canvasy(y)
    #     - Apparently this was the cause of false associations between icons and id's.
    #     - It's amazing that the code didn't fail earlier without these!
    #
    # - Converted all module-level constants to ivars.
    #
    # - Lines no longer interfere with eventToPosition.
    #     - The problem was that find_nearest or find_overlapping don't depend on stacking order!
    #     - Added p param to horizontal lines, but not vertical lines.
    #     - EventToPosition adds 1 to the x coordinate of vertical lines, then recomputes the id.
    #
    # - Compute indentation only in forceDrawNode.  Removed child_indent constant.
    #
    # - Simplified drawTree to use indentation returned from forceDrawNode.
    #
    # - setHeadlineText now ensures that state is "normal" before attempting to set the text.
    #     - This is the robust way.
    #
    # 7/31/04: newText must call setHeadlineText for all nodes allocated, even if p matches.
    #@<  Birth... (swingTree)
    #@> __init__ (swingTree)
    def __init__(self, c, frame, canvas):
        # Init the base class.
        leoFrame.leoTree.__init__(self, frame)

        # Configuration and debugging settings.
        # These must be defined here to eliminate memory leaks.
        self.allow_clone_drags = c.config.getBool('allow_clone_drags')
        self.center_selected_tree_node = c.config.getBool('center_selected_tree_node')
        self.enable_drag_messages = c.config.getBool("enable_drag_messages")
        self.expanded_click_area = c.config.getBool('expanded_click_area')
        self.gc_before_redraw = c.config.getBool('gc_before_redraw')

        self.headline_text_editing_foreground_color = c.config.getColor(
            'headline_text_editing_foreground_color'
        )
        self.headline_text_editing_background_color = c.config.getColor(
            'headline_text_editing_background_color'
        )
        self.headline_text_editing_selection_foreground_color = c.config.getColor(
            'headline_text_editing_selection_foreground_color'
        )
        self.headline_text_editing_selection_background_color = c.config.getColor(
            'headline_text_editing_selection_background_color'
        )
        self.headline_text_selected_foreground_color = c.config.getColor(
            "headline_text_selected_foreground_color"
        )
        self.headline_text_selected_background_color = c.config.getColor(
            "headline_text_selected_background_color"
        )
        self.headline_text_editing_selection_foreground_color = c.config.getColor(
            "headline_text_editing_selection_foreground_color"
        )
        self.headline_text_editing_selection_background_color = c.config.getColor(
            "headline_text_editing_selection_background_color"
        )
        self.headline_text_unselected_foreground_color = c.config.getColor(
            'headline_text_unselected_foreground_color'
        )
        self.headline_text_unselected_background_color = c.config.getColor(
            'headline_text_unselected_background_color'
        )

        self.idle_redraw = c.config.getBool('idle_redraw')
        self.initialClickExpandsOrContractsNode = c.config.getBool(
            'initialClickExpandsOrContractsNode'
        )
        self.look_for_control_drag_on_mouse_down = c.config.getBool(
            'look_for_control_drag_on_mouse_down'
        )
        self.select_all_text_when_editing_headlines = c.config.getBool(
            'select_all_text_when_editing_headlines'
        )

        self.stayInTree = c.config.getBool('stayInTreeAfterSelect')
        self.trace = c.config.getBool('trace_tree')
        self.trace_alloc = c.config.getBool('trace_tree_alloc')
        self.trace_chapters = c.config.getBool('trace_chapters')
        self.trace_edit = c.config.getBool('trace_tree_edit')
        self.trace_gc = c.config.getBool('trace_tree_gc')
        self.trace_redraw = c.config.getBool('trace_tree_redraw')
        self.trace_select = c.config.getBool('trace_select')
        self.trace_stats = c.config.getBool('show_tree_stats')
        self.use_chapters = False and c.config.getBool('use_chapters')  ###

        # Objects associated with this tree.
        self.canvas = canvas

        #@+<< define drawing constants >>
        #@> << define drawing constants >>
        self.box_padding = 5  # extra padding between box and icon
        self.box_width = 9 + self.box_padding
        self.icon_width = 20
        self.text_indent = 4  # extra padding between icon and tex

        self.hline_y = 7  # Vertical offset of horizontal line
        self.root_left = 7 + self.box_width
        self.root_top = 2

        self.default_line_height = 17 + 2  # default if can't set line_height from font.
        self.line_height = self.default_line_height
        #@-<< define drawing constants >>
        #@+<< old ivars >>
        #@ << old ivars >>
        # Miscellaneous info.
        self.iconimages = {}  # Image cache set by getIconImage().
        self.active = False  # True if present headline is active
        self._editPosition = None  # Returned by leoTree.editPosition()
        self.lineyoffset = 0  # y offset for this headline.
        self.lastClickFrameId = None  # id of last entered clickBox.
        self.lastColoredText = None  # last colored text widget.

        # Set self.font and self.fontName.
        self.setFontFromConfig()

        # Drag and drop
        self.drag_p = None
        self.controlDrag = False  # True: control was down when drag started.

        # Keep track of popup menu so we can handle behavior better on Linux Context menu
        self.popupMenu = None

        # Incremental redraws:
        self.allocateOnlyVisibleNodes = False  # True: enable incremental redraws.
        self.prevMoveToFrac = 0.0
        self.visibleArea = None
        self.expandedVisibleArea = None
        #@-<< old ivars >>
        #@+<< inject callbacks into the position class >>
        #@ << inject callbacks into the position class >>
        # The new code injects 3 callbacks for the colorizer.

        if not leoSwingTree.callbacksInjected:  # Class var.
            leoSwingTree.callbacksInjected = True
            self.injectCallbacks()
        #@-<< inject callbacks into the position class >>

        self.dragging = False
        self.generation = 0
        self.prevPositions = 0
        self.redrawing = False  # Used only to disable traces.
        self.redrawCount = 0  # Count for debugging.
        self.revertHeadline = None  # Previous headline text for abortEditLabel.

        # New in 4.4: We should stay in the tree to use per-pane bindings.
        self.textBindings = []  # Set in setBindings.
        self.textNumber = 0  # To make names unique.
        self.updateCount = 0  # Drawing is enabled only if self.updateCount <= 0
        self.verbose = True

        self.setEditPosition(None)  # Set positions returned by leoTree.editPosition()

        # Keys are id's, values are positions...
        self.ids = {}
        self.iconIds = {}

        # Lists of visible (in-use) widgets...
        self.visibleBoxes = []
        self.visibleClickBoxes = []
        self.visibleIcons = []
        self.visibleLines = []
        self.visibleText = {}
        # Pre 4.4b2: Keys are vnodes, values are Tk.Text widgets.
        #     4.4b2: Keys are p.key(), values are Tk.Text widgets.
        self.visibleUserIcons = []

        # Lists of free, hidden widgets...
        self.freeBoxes = []
        self.freeClickBoxes = []
        self.freeIcons = []
        self.freeLines = []
        self.freeText = []  # New in 4.4b2: a list of free Tk.Text widgets

        self.freeUserIcons = []

    #@< swingTtree.setBindings
    def setBindings(
        self,
    ):
        '''Create master bindings for all headlines.'''

        tree = self
        k = self.c.k
        canvas = self.canvas

        if 0:
            # g.trace('self',self,'canvas',canvas)

            #@+<< make bindings for a common binding widget >>
            #@> << make bindings for a common binding widget >>
            self.bindingWidget = w = g.app.gui.plainTextWidget(self.canvas, name='bindingWidget')
            #@-<< make bindings for a common binding widget >>

            tree.setCanvasBindings(canvas)

            k.completeAllBindingsForWidget(canvas)

            k.completeAllBindingsForWidget(self.bindingWidget)

    #@< swingTree.setCanvasBindings
    def setCanvasBindings(self, canvas):
        pass

    #@< Allocation...
    #@> newBox
    def newBox(self, p, x, y, image):
        canvas = self.canvas
        tag = "plusBox"

        if self.freeBoxes:
            theId = self.freeBoxes.pop(0)
            canvas.coords(theId, x, y)
            canvas.itemconfigure(theId, image=image)
        else:
            theId = canvas.create_image(x, y, image=image, tag=tag)
            if self.trace_alloc:
                g.trace("%3d %s" % (theId, p and p.h), align=-20)

        if theId not in self.visibleBoxes:
            self.visibleBoxes.append(theId)

        if p:
            self.ids[theId] = p

        return theId

    #@ newClickBox
    def newClickBox(self, p, x1, y1, x2, y2):
        canvas = self.canvas
        defaultColor = ""
        tag = g.choose(p.hasChildren(), 'clickBox', 'selectBox')

        if self.freeClickBoxes:
            theId = self.freeClickBoxes.pop(0)
            canvas.coords(theId, x1, y1, x2, y2)
            canvas.itemconfig(theId, tag=tag)
        else:
            theId = self.canvas.create_rectangle(x1, y1, x2, y2, tag=tag)
            canvas.itemconfig(theId, fill=defaultColor, outline=defaultColor)
            if self.trace_alloc:
                g.trace("%3d %s" % (theId, p and p.h), align=-20)

        if theId not in self.visibleClickBoxes:
            self.visibleClickBoxes.append(theId)
        if p:
            self.ids[theId] = p

        return theId

    #@ newIcon
    def newIcon(self, p, x, y, image):
        canvas = self.canvas
        tag = "iconBox"

        if self.freeIcons:
            theId = self.freeIcons.pop(0)
            canvas.itemconfigure(theId, image=image)
            canvas.coords(theId, x, y)
        else:
            theId = canvas.create_image(x, y, image=image, anchor="nw", tag=tag)
            if self.trace_alloc:
                g.trace("%3d %s" % (theId, p and p.h), align=-20)

        if theId not in self.visibleIcons:
            self.visibleIcons.append(theId)

        if p:
            data = p, self.generation
            self.iconIds[theId] = data  # Remember which vnode belongs to the icon.
            self.ids[theId] = p

        return theId

    #@ newLine
    def newLine(self, p, x1, y1, x2, y2):
        canvas = self.canvas

        if self.freeLines:
            theId = self.freeLines.pop(0)
            canvas.coords(theId, x1, y1, x2, y2)
        else:
            theId = canvas.create_line(
                x1, y1, x2, y2, tag="lines", fill="gray50"
            )  # stipple="gray25")
            if self.trace_alloc:
                g.trace("%3d %s" % (theId, p and p.h), align=-20)

        if p:
            self.ids[theId] = p

        if theId not in self.visibleLines:
            self.visibleLines.append(theId)

        return theId

    #@ newText (swingTree) and helper
    def newText(self, p, x, y):
        canvas = self.canvas
        tag = "textBox"
        c = self.c
        k = c.k
        if self.freeText:
            w, theId = self.freeText.pop()
            canvas.coords(theId, x, y)  # Make the window visible again.
        # theId is the id of the *window* not the text.
        else:
            # Tags are not valid in Tk.Text widgets.
            self.textNumber += 1
            w = g.app.gui.plainTextWidget(
                canvas,
                name='head-%d' % self.textNumber,
                state="normal",
                font=self.font,
                bd=0,
                relief="flat",
                height=1,
            )
            ### w.bindtags(self.textBindings) # Set the bindings for this widget.

            if 0:  # Crashes on XP.
                #@+<< patch by Maciej Kalisiak to handle scroll-wheel events >>
                #@-<< patch by Maciej Kalisiak to handle scroll-wheel events >>

            theId = canvas.create_window(x, y, anchor="nw", window=w, tag=tag)
            w.leo_window_id = theId  # Never changes.

            if self.trace_alloc:
                g.trace('%3d %6s' % (theId, id(w)), align=-20)

        # Common configuration.
        if 0:  # Doesn't seem to work.
            balloon = Pmw.Balloon(canvas, initwait=700)
            balloon.tagbind(canvas, theId, balloonHelp='Headline')

        if p:
            self.ids[theId] = p  # Add the id of the *window*
            self.setHeadlineText(theId, w, p.h)
            w.configure(width=self.headWidth(p=p))
            w.leo_position = p  # This p never changes.
            # *Required*: onHeadlineClick uses w.leo_position to get p.

            # Keys are p.key().  Entries are (w,theId)
            self.visibleText[p.key()] = w, theId
        else:
            g.trace('**** can not happen.  No p')

        return w

    #@ recycleWidgets
    def recycleWidgets(self):
        canvas = self.canvas

        for theId in self.visibleBoxes:
            if theId not in self.freeBoxes:
                self.freeBoxes.append(theId)
            canvas.coords(theId, -100, -100)
        self.visibleBoxes = []

        for theId in self.visibleClickBoxes:
            if theId not in self.freeClickBoxes:
                self.freeClickBoxes.append(theId)
            canvas.coords(theId, -100, -100, -100, -100)
        self.visibleClickBoxes = []

        for theId in self.visibleIcons:
            if theId not in self.freeIcons:
                self.freeIcons.append(theId)
            canvas.coords(theId, -100, -100)
        self.visibleIcons = []

        for theId in self.visibleLines:
            if theId not in self.freeLines:
                self.freeLines.append(theId)
            canvas.coords(theId, -100, -100, -100, -100)
        self.visibleLines = []

        aList = self.visibleText.values()
        for data in aList:
            w, theId = data
            # assert theId == w.leo_window_id
            canvas.coords(theId, -100, -100)
            w.leo_position = None  # Allow the position to be freed.
            if data not in self.freeText:
                self.freeText.append(data)
        self.visibleText = {}

        for theId in self.visibleUserIcons:
            # The present code does not recycle user Icons.
            self.canvas.delete(theId)
        self.visibleUserIcons = []

    #@ destroyWidgets
    def destroyWidgets(self):
        self.ids = {}

        self.visibleBoxes = []
        self.visibleClickBoxes = []
        self.visibleIcons = []
        self.visibleLines = []
        self.visibleUserIcons = []

        self.visibleText = {}

        self.freeText = []
        self.freeBoxes = []
        self.freeClickBoxes = []
        self.freeIcons = []
        self.freeLines = []

        self.canvas.delete("all")

    #@ showStats
    def showStats(self):
        z = []
        for kind, a, b in (
            ('boxes', self.visibleBoxes, self.freeBoxes),
            ('clickBoxes', self.visibleClickBoxes, self.freeClickBoxes),
            ('icons', self.visibleIcons, self.freeIcons),
            ('lines', self.visibleLines, self.freeLines),
            ('tesxt', self.visibleText.values(), self.freeText),
        ):
            z.append('%10s used: %4d free: %4d' % (kind, len(a), len(b)))

        g.es_print('\n' + '\n'.join(z))

    #@< Config & Measuring...
    #@> tree.getFont,setFont,setFontFromConfig
    def getFont(self):
        return self.font

    def setFont(self, font=None, fontName=None):
        # ESSENTIAL: retain a link to font.
        if fontName:
            self.fontName = fontName
            self.font = swingFont.Font(font=fontName)
        else:
            self.fontName = None
            self.font = font

        self.setLineHeight(self.font)

    # Called by ctor and when config params are reloaded.
    def setFontFromConfig(self):
        c = self.c
        # g.trace()
        font = c.config.getFontFromParams(
            "headline_text_font_family",
            "headline_text_font_size",
            "headline_text_font_slant",
            "headline_text_font_weight",
            c.config.defaultTreeFontSize,
        )

        self.setFont(font)

    #@ headWidth & widthInPixels
    def headWidth(self, p=None, s=''):
        """Returns the proper width of the entry widget for the headline."""

        if p:
            s = p.h

        return self.font.measure(s) / self.font.measure('0') + 1

    def widthInPixels(self, s):
        s = g.toEncodedString(s)

        return self.font.measure(s)

    #@ setLineHeight
    def setLineHeight(self, font):
        pass

    #@< Debugging...
    #@> textAddr
    def textAddr(self, w):
        """Return the address part of repr(Tk.Text)."""

        return repr(w)[-9:-1].lower()

    #@ traceIds (Not used)
    # Verbose tracing is much more useful than this because we can see the recent past.

    def traceIds(self, full=False):
        tree = self

        for theDict, tag, flag in ((tree.ids, "ids", True), (tree.iconIds, "icon ids", False)):
            print('=' * 60)
            print("\n%s..." % tag)
            keys = theDict.keys()
            keys.sort()
            for key in keys:
                p = tree.ids.get(key)
                if p is None:  # For lines.
                    print("%3d None" % key)
                else:
                    print("%3d" % key, p.h)
            if flag and full:
                print('-' * 40)
                values = theDict.values()
                values.sort()
                seenValues = []
                for value in values:
                    if value not in seenValues:
                        seenValues.append(value)
                        for item in theDict.items():
                            key, val = item
                            if val and val == value:
                                print("%3d" % key, val.h)

    #@< Drawing... (swingTree)
    #@> tree.begin/endUpdate
    def beginUpdate(self):
        self.updateCount += 1
        # g.trace('tree',id(self),self.updateCount,g.callers())

    def endUpdate(self, flag, scroll=False):
        self.updateCount -= 1
        # g.trace(self.updateCount,'scroll',scroll,g.callers())

        if self.updateCount <= 0:
            if flag:
                self.redraw_now(scroll=scroll)
            if self.updateCount < 0:
                g.trace("Can't happen: negative updateCount", g.callers())

    #@ tree.redraw_now & helper
    # New in 4.4b2: suppress scrolling by default.

    def redraw_now(self, scroll=False):
        '''Redraw immediately: used by Find so a redraw doesn't mess up selections in headlines.'''

        if g.app.quitting or self.drag_p or self.frame not in g.app.windowList:
            return

        c = self.c

        # g.trace(g.callers())

        if not g.app.unitTesting:
            if self.gc_before_redraw:
                g.collectGarbage()
            if g.app.trace_gc_verbose:
                if (self.redrawCount % 5) == 0:
                    g.printGcSummary()
            if self.trace_redraw or self.trace_alloc:
                # g.trace(self.redrawCount,g.callers())
                # g.trace(c.rootPosition().h,'canvas:',id(self.canvas),g.callers())
                if self.trace_stats:
                    g.print_stats()
                    g.clear_stats()

        # New in 4.4b2: Call endEditLabel, but suppress the redraw.
        self.beginUpdate()
        try:
            self.endEditLabel()
        finally:
            self.endUpdate(False)

        # Do the actual redraw.
        c.expandAllAncestors(c.currentPosition())
        if self.idle_redraw:

            def idleRedrawCallback(event=None, self=self, scroll=scroll):
                self.redrawHelper(scroll=scroll)

            ### self.canvas.after_idle(idleRedrawCallback)
        else:
            self.redrawHelper(scroll=scroll)
        if g.app.unitTesting:
            self.canvas.update_idletasks()  # Important for unit tests.
        c.masterFocusHandler()

    redraw = redraw_now  # Compatibility

    #@> redrawHelper
    def redrawHelper(self, scroll=True):
        c = self.c
        g.doHook("after-redraw-outline", c=c)

    #@< idle_second_redraw
    def idle_second_redraw(self):
        c = self.c

        # Erase and redraw the entire tree the SECOND time.
        # This ensures that all visible nodes are allocated.
        c.setTopVnode(None)
        args = self.canvas.yview()
        self.setVisibleArea(args)

        if 0:
            self.deleteBindings()
            self.canvas.delete("all")

        self.drawTopTree()

        if self.trace:
            g.trace(self.redrawCount)

    #@ drawX...
    #@> drawBox
    def drawBox(self, p, x, y):
        tree = self
        c = self.c
        y += 7  # draw the box at x, y+7

        theId = g.doHook("draw-outline-box", tree=tree, c=c, p=p, v=p, x=x, y=y)

        if theId is None:
            # if self.trace_gc: g.printNewObjects(tag='box 1')
            iconname = g.choose(p.isExpanded(), "minusnode.gif", "plusnode.gif")
            image = self.getIconImage(iconname)
            theId = self.newBox(p, x, y + self.lineyoffset, image)
            # if self.trace_gc: g.printNewObjects(tag='box 2')
            return theId
        else:
            return theId

    #@ drawClickBox
    def drawClickBox(self, p, y):
        h = self.line_height

        # Define a slighly larger rect to catch clicks.
        if self.expanded_click_area:
            self.newClickBox(p, 0, y, 1000, y + h - 2)

    #@ drawIcon
    def drawIcon(self, p, x=None, y=None):
        """Draws icon for position p at x,y, or at p.v.iconx,p.v.icony if x,y = None,None"""

        # if self.trace_gc: g.printNewObjects(tag='icon 1')

        c = self.c
        v = p.v
        #@+<< compute x,y and iconVal >>
        #@> << compute x,y and iconVal >>
        if x is None and y is None:
            try:
                x, y = v.iconx, v.icony
            except:
                # Inject the ivars.
                x, y = v.iconx, v.icony = 0, 0
        else:
            # Inject the ivars.
            v.iconx, v.icony = x, y

        y += 2  # draw icon at y + 2

        # Always recompute v.iconVal.
        # This is an important drawing optimization.
        val = v.computeIcon()
        assert 0 <= val <= 15
        # g.trace(v,val)
        #@-<< compute x,y and iconVal >>
        v.iconVal = val

        if not g.doHook("draw-outline-icon", tree=self, c=c, p=p, v=p, x=x, y=y):
            # Get the image.
            imagename = "box%02d.GIF" % val
            image = self.getIconImage(imagename)
            self.newIcon(p, x, y + self.lineyoffset, image)

        return 0, self.icon_width  # dummy icon height,width

    #@< drawLine
    def drawLine(self, p, x1, y1, x2, y2):
        theId = self.newLine(p, x1, y1, x2, y2)

        return theId

    #@ drawNode & force_draw_node (good trace)
    def drawNode(self, p, x, y):
        c = self.c

        # g.trace(x,y,p,id(self.canvas))

        data = g.doHook("draw-outline-node", tree=self, c=c, p=p, v=p, x=x, y=y)
        if data is not None:
            return data

        if 1:
            self.lineyoffset = 0
        else:
            if hasattr(p.v.t, "unknownAttributes"):
                self.lineyoffset = p.v.t.unknownAttributes.get("lineYOffset", 0)
            else:
                self.lineyoffset = 0

        # Draw the horizontal line.
        self.drawLine(p, x, y + 7 + self.lineyoffset, x + self.box_width, y + 7 + self.lineyoffset)

        if self.inVisibleArea(y):
            return self.force_draw_node(p, x, y)
        else:
            return self.line_height, 0

    #@> force_draw_node
    def force_draw_node(self, p, x, y):
        h = 0  # The total height of the line.
        indent = 0  # The amount to indent this line.

        h2, w2 = self.drawUserIcons(p, "beforeBox", x, y)
        h = max(h, h2)
        x += w2
        indent += w2

        if p.hasChildren():
            self.drawBox(p, x, y)

        indent += self.box_width
        x += self.box_width  # even if box isn't drawn.

        h2, w2 = self.drawUserIcons(p, "beforeIcon", x, y)
        h = max(h, h2)
        x += w2
        indent += w2

        h2, w2 = self.drawIcon(p, x, y)
        h = max(h, h2)
        x += w2
        indent += w2 / 2

        # Nothing after here affects indentation.
        h2, w2 = self.drawUserIcons(p, "beforeHeadline", x, y)
        h = max(h, h2)
        x += w2

        h2 = self.drawText(p, x, y)
        h = max(h, h2)
        x += self.widthInPixels(p.h)

        h2, w2 = self.drawUserIcons(p, "afterHeadline", x, y)
        h = max(h, h2)

        self.drawClickBox(p, y)

        return h, indent

    #@< drawText
    def drawText(self, p, x, y):
        """draw text for position p at nominal coordinates x,y."""

        assert p

        c = self.c
        x += self.text_indent

        data = g.doHook("draw-outline-text-box", tree=self, c=c, p=p, v=p, x=x, y=y)
        if data is not None:
            return data

        self.newText(p, x, y + self.lineyoffset)

        self.configureTextState(p)

        return self.line_height

    #@ drawUserIcons
    def drawUserIcons(self, p, where, x, y):
        """Draw any icons specified by p.v.t.unknownAttributes["icons"]."""

        h, w = 0, 0
        t = p.v.t

        if not hasattr(t, "unknownAttributes"):
            return h, w

        iconsList = t.unknownAttributes.get("icons")
        if not iconsList:
            return h, w

        try:
            for theDict in iconsList:
                h2, w2 = self.drawUserIcon(p, where, x, y, w, theDict)
                h = max(h, h2)
                w += w2
        except:
            g.es_exception()

        # g.trace(where,h,w)

        return h, w

    #@ drawUserIcon
    def drawUserIcon(self, p, where, x, y, w2, theDict):
        h, w = 0, 0

        if where != theDict.get("where", "beforeHeadline"):
            return h, w

        # if self.trace_gc: g.printNewObjects(tag='userIcon 1')

        # g.trace(where,x,y,theDict)

        #@+<< set offsets and pads >>
        #@> << set offsets and pads >>
        xoffset = theDict.get("xoffset")
        try:
            xoffset = int(xoffset)
        except:
            xoffset = 0

        yoffset = theDict.get("yoffset")
        try:
            yoffset = int(yoffset)
        except:
            yoffset = 0

        xpad = theDict.get("xpad")
        try:
            xpad = int(xpad)
        except:
            xpad = 0

        ypad = theDict.get("ypad")
        try:
            ypad = int(ypad)
        except:
            ypad = 0
        #@-<< set offsets and pads >>
        theType = theDict.get("type")
        if theType == "icon":
            if 0:  # not ready yet.
                s = theDict.get("icon")
                #@+<< draw the icon in string s >>
                #@ << draw the icon in string s >>
                pass
                #@-<< draw the icon in string s >>
        elif theType == "file":
            theFile = theDict.get("file")
            #@+<< draw the icon at file >>
            #@ << draw the icon at file >>
            try:
                image = self.iconimages[theFile]
                # Get the image from the cache if possible.
            except KeyError:
                try:
                    fullname = g.os_path_join(g.app.loadDir, "..", "Icons", theFile)
                    fullname = g.os_path_normpath(fullname)
                    image = Tk.PhotoImage(master=self.canvas, file=fullname)
                    self.iconimages[fullname] = image
                except:
                    # g.es("Exception loading: " + fullname)
                    # g.es_exception()
                    image = None

            if image:
                theId = self.canvas.create_image(
                    x + xoffset + w2, y + yoffset, anchor="nw", image=image, tag="userIcon"
                )
                self.ids[theId] = p
                # assert(theId not in self.visibleIcons)
                self.visibleUserIcons.append(theId)

                h = image.height() + yoffset + ypad
                w = image.width() + xoffset + xpad
            #@-<< draw the icon at file >>
        elif theType == "url":
            ## url = theDict.get("url")
            #@+<< draw the icon at url >>
            #@ << draw the icon at url >>
            pass
            #@-<< draw the icon at url >>

        # Allow user to specify height, width explicitly.
        h = theDict.get("height", h)
        w = theDict.get("width", w)

        # if self.trace_gc: g.printNewObjects(tag='userIcon 2')

        return h, w

    #@< drawTopTree
    def drawTopTree(self):
        """Draws the top-level tree, taking into account the hoist state."""

        c = self.c
        canvas = self.canvas
        trace = False or self.trace or self.trace_redraw

        self.redrawing = True

        # Recycle all widgets and clear all widget lists.
        self.recycleWidgets()
        # Clear all ids so invisible id's don't confuse eventToPosition & findPositionWithIconId
        self.ids = {}
        self.iconIds = {}
        self.generation += 1
        self.redrawCount += 1
        self.drag_p = None  # Disable drags across redraws.
        self.dragging = False
        if trace:
            g.trace(
                'redrawCount', self.redrawCount, g.callers()
            )  # 'len(c.hoistStack)',len(c.hoistStack))
            if 0:
                delta = g.app.positions - self.prevPositions
                g.trace(
                    "**** gen: %-3d positions: %5d +%4d"
                    % (self.generation, g.app.positions, delta),
                    g.callers(),
                )

        self.prevPositions = g.app.positions
        if self.trace_gc:
            g.printNewObjects(tag='top 1')

        hoistFlag = c.hoistStack
        if c.hoistStack:
            bunch = c.hoistStack[-1]
            p = bunch.p
            h = p.h
            if len(c.hoistStack) == 1 and h.startswith('@chapter') and p.hasChildren():
                p = p.firstChild()
                hoistFlag = False
        else:
            p = c.rootPosition()

        self.drawTree(p, self.root_left, self.root_top, 0, 0, hoistFlag=hoistFlag)

        if self.trace_gc:
            g.printNewObjects(tag='top 2')
        if self.trace_stats:
            self.showStats()

        canvas.lower("lines")  # Lowest.
        canvas.lift("textBox")  # Not the Tk.Text widget: it should be low.
        canvas.lift("userIcon")
        canvas.lift("plusBox")
        canvas.lift("clickBox")
        canvas.lift("clickExpandBox")
        canvas.lift("iconBox")  # Higest.

        self.redrawing = False

    #@ drawTree
    def drawTree(self, p, x, y, h, level, hoistFlag=False):
        tree = self
        c = self.c
        yfirst = ylast = y
        h1 = None
        data = g.doHook(
            "draw-sub-outline",
            tree=tree,
            c=c,
            p=p,
            v=p,
            x=x,
            y=y,
            h=h,
            level=level,
            hoistFlag=hoistFlag,
        )
        if data is not None:
            return data

        while p:  # Do not use iterator.
            # This is the ONLY copy of p that needs to be made;
            # no other drawing routine calls any p.moveTo method.
            const_p = p.copy()
            h, indent = self.drawNode(const_p, x, y)
            if h1 is None:
                h1 = h  # Set h1 *after* calling drawNode.
            y += h
            ylast = y
            if p.isExpanded() and p.hasFirstChild():
                # Must make an additional copy here by calling firstChild.
                y = self.drawTree(p.firstChild(), x + indent, y, h, level + 1)
            if hoistFlag:
                break
            else:
                p = p.next()
        # Draw the vertical line.
        if h1 is None:
            h1 = h
        y2 = g.choose(level == 0, yfirst + (h1 - 1) / 2, yfirst - h1 / 2 - 1)
        self.drawLine(None, x, y2, x, ylast + self.hline_y - h)
        return y

    #@< Helpers...
    #@> getIconImage
    def getIconImage(self, name):
        # Return the image from the cache if possible.
        if self.iconimages.has_key(name):
            return self.iconimages[name]

        # g.trace(name)

        try:
            fullname = g.os_path_join(g.app.loadDir, "..", "Icons", name)
            fullname = g.os_path_normpath(fullname)
            image = Tk.PhotoImage(master=self.canvas, file=fullname)
            self.iconimages[name] = image
            return image
        except:
            g.es("Exception loading: " + fullname)
            g.es_exception()
            return None

    #@ inVisibleArea & inExpandedVisibleArea
    def inVisibleArea(self, y1):
        if self.allocateOnlyVisibleNodes:
            if self.visibleArea:
                vis1, vis2 = self.visibleArea
                y2 = y1 + self.line_height
                return y2 >= vis1 and y1 <= vis2
            else:
                return False
        else:
            return True  # This forces all nodes to be allocated on all redraws.

    def inExpandedVisibleArea(self, y1):
        if self.expandedVisibleArea:
            vis1, vis2 = self.expandedVisibleArea
            y2 = y1 + self.line_height
            return y2 >= vis1 and y1 <= vis2
        else:
            return False

    #@ numberOfVisibleNodes
    def numberOfVisibleNodes(self):
        c = self.c

        n = 0
        p = self.c.rootPosition()
        while p:
            n += 1
            p.moveToVisNext(c)
        return n

    #@ scrollTo (swingTree)
    def scrollTo(self, p=None):
        """Scrolls the canvas so that p is in view."""

        # __pychecker__ = '--no-argsused' # event not used.
        # __pychecker__ = '--no-intdivide' # suppress warning about integer division.

        c = self.c
        frame = c.frame
        trace = True
        if not p or not c.positionExists(p):
            p = c.currentPosition()
        if not p or not c.positionExists(p):
            if trace:
                g.trace('current p does not exist', p)
            p = c.rootPosition()
        if not p or not c.positionExists(p):
            if trace:
                g.trace('no root position')
            return
        try:
            h1 = self.yoffset(p)
            if self.center_selected_tree_node:  # New in Leo 4.4.3.
                #@+<< compute frac0 >>
                #@> << compute frac0 >>
                # frac0 attempt to put the
                scrollRegion = self.canvas.cget('scrollregion')
                geom = self.canvas.winfo_geometry()

                if scrollRegion and geom:
                    scrollRegion = scrollRegion.split(' ')
                    # g.trace('scrollRegion',repr(scrollRegion))
                    htot = int(scrollRegion[3])
                    wh, junk, junk = geom.split('+')
                    junk, h = wh.split('x')
                    if h:
                        wtot = int(h)
                    else:
                        wtot = 500
                    # g.trace('geom',geom,'wtot',wtot)
                    if htot > 0.1:
                        frac0 = float(h1 - wtot / 2) / float(htot)
                        frac0 = max(min(frac0, 1.0), 0.0)
                    else:
                        frac0 = 0.0
                else:
                    frac0 = 0.0
                    htot = wtot = 0
                #@-<< compute frac0 >>
                delta = abs(self.prevMoveToFrac - frac0)
                # g.trace(delta)
                if delta > 0.0:
                    self.prevMoveToFrac = frac0
                    self.canvas.yview("moveto", frac0)
                    if trace:
                        g.trace("frac0 %1.2f %3d %3d %3d" % (frac0, h1, htot, wtot))
            else:
                last = c.lastVisible()
                nextToLast = last.visBack(c)
                h2 = self.yoffset(last)
                #@+<< compute approximate line height >>
                #@ << compute approximate line height >>
                if nextToLast:  # 2/2/03: compute approximate line height.
                    lineHeight = h2 - self.yoffset(nextToLast)
                else:
                    lineHeight = 20  # A reasonable default.
                #@-<< compute approximate line height >>
                #@+<< Compute the fractions to scroll down/up >>
                #@ << Compute the fractions to scroll down/up >>
                data = frame.canvas.leo_treeBar.get()  # Get the previous values of the scrollbar.
                try:
                    lo, hi = data
                except:
                    lo, hi = 0.0, 1.0

                # h1 and h2 are the y offsets of the present and last nodes.
                if h2 > 0.1:
                    frac = float(h1) / float(h2)  # For scrolling down.
                    frac2 = float(h1 + lineHeight / 2) / float(h2)  # For scrolling up.
                    frac2 = frac2 - (hi - lo)
                else:
                    frac = frac2 = 0.0  # probably any value would work here.

                frac = max(min(frac, 1.0), 0.0)
                frac2 = max(min(frac2, 1.0), 0.0)
                #@-<< Compute the fractions to scroll down/up >>
                if frac <= lo:  # frac is for scrolling down.
                    if self.prevMoveToFrac != frac:
                        self.prevMoveToFrac = frac
                        self.canvas.yview("moveto", frac)
                        if trace:
                            g.trace("frac  %1.2f %3d %3d %1.2f %1.2f" % (frac, h1, h2, lo, hi))
                elif frac2 + (hi - lo) >= hi:  # frac2 is for scrolling up.
                    if self.prevMoveToFrac != frac2:
                        self.prevMoveToFrac = frac2
                        self.canvas.yview("moveto", frac2)
                        if trace:
                            g.trace("frac2 1.2f %3d %3d %1.2f %1.2f" % (frac2, h1, h2, lo, hi))

            if self.allocateOnlyVisibleNodes:
                pass  ### self.canvas.after_idle(self.idle_second_redraw)

            c.setTopVnode(p)  # 1/30/04: remember a pseudo "top" node.

        except:
            g.es_exception()

    idle_scrollTo = scrollTo  # For compatibility.
    #@< yoffset (swingTree)
    # For the same reason we can't rely on any TK canvas methods here.
    #@@c

    def yoffset(self, p1):
        # if not p1.isVisible(): print "yoffset not visible:",p1
        if not p1:
            return 0
        if c.hoistStack:
            bunch = c.hoistStack[-1]
            root = bunch.p.copy()
        else:
            root = self.c.rootPosition()
        if root:
            h, flag = self.yoffsetTree(root, p1)
            # flag can be False during initialization.
            # if not flag: print "yoffset fails:",h,v1
            return h
        else:
            return 0

    def yoffsetTree(self, p, p1):
        h = 0
        trace = False
        if not self.c.positionExists(p):
            if trace:
                g.trace('does not exist', p.h)
            return h, False  # An extra precaution.
        p = p.copy()
        for p2 in p.self_and_siblings():
            print("yoffsetTree:", p2)
            if p2 == p1:
                if trace:
                    g.trace(p.h, p1.h, h)
                return h, True
            h += self.line_height
            if p2.isExpanded() and p2.hasChildren():
                child = p2.firstChild()
                h2, flag = self.yoffsetTree(child, p1)
                h += h2
                if flag:
                    if trace:
                        g.trace(p.h, p1.h, h)
                    return h, True

        if trace:
            g.trace('not found', p.h, p1.h)
        return h, False

    #@<2 Event handlers (swingTree)
    #@> Helpers
    #@> checkWidgetList
    def checkWidgetList(self, tag):
        return True  # This will fail when the headline actually changes!

        for w in self.visibleText:
            p = w.leo_position
            if p:
                s = w.getAllText().strip()
                h = p.h.strip()

                if h != s:
                    self.dumpWidgetList(tag)
                    return False
            else:
                self.dumpWidgetList(tag)
                return False

        return True

    #@ dumpWidgetList
    def dumpWidgetList(self, tag):
        print("checkWidgetList: %s" % tag)

        for w in self.visibleText:
            p = w.leo_position
            if p:
                s = w.getAllText().strip()
                h = p.h.strip()

                addr = self.textAddr(w)
                print("p:", addr, h)
                if h != s:
                    print("w:", '*' * len(addr), s)
            else:
                print("w.leo_position == None", w)

    #@ tree.edit_widget
    def edit_widget(self, p):
        """Returns the Tk.Edit widget for position p."""

        return self.findEditWidget(p)

    #@ eventToPosition
    def eventToPosition(self, event):
        canvas = self.canvas
        x, y = event.x, event.y
        x = canvas.canvasx(x)
        y = canvas.canvasy(y)
        if self.trace:
            g.trace(x, y)
        item = canvas.find_overlapping(x, y, x, y)
        if not item:
            return None

        # Item may be a tuple, possibly empty.
        try:
            theId = item[0]
        except:
            theId = item
        if not theId:
            return None

        p = self.ids.get(theId)

        # A kludge: p will be None for vertical lines.
        if not p:
            item = canvas.find_overlapping(x + 1, y, x + 1, y)
            try:
                theId = item[0]
            except:
                theId = item
            if not theId:
                g.es_print('oops: eventToPosition failed')
                return None
            p = self.ids.get(theId)
            # g.trace("was vertical line",p)

        if self.trace and self.verbose:
            if p:
                w = self.findEditWidget(p)
                g.trace("%3d %3d %3d %d" % (theId, x, y, id(w)), p.h)
            else:
                g.trace("%3d %3d %3d" % (theId, x, y), None)

        # defensive programming: this copy is not needed.
        if p:
            return p.copy()  # Make _sure_ nobody changes this table!
        else:
            return None

    #@ findEditWidget
    def findEditWidget(self, p):
        """Return the Tk.Text item corresponding to p."""

        c = self.c

        if p and c:
            aTuple = self.visibleText.get(p.key())
            if aTuple:
                w, theId = aTuple
                # g.trace('%4d' % (theId),self.textAddr(w),p.h)
                return w
            else:
                # g.trace('oops: not found',p)
                return None

        # g.trace(not found',p.h)
        return None

    #@ findVnodeWithIconId
    def findPositionWithIconId(self, theId):
        # Due to an old bug, theId may be a tuple.
        try:
            data = self.iconIds.get(theId[0])
        except:
            data = self.iconIds.get(theId)

        if data:
            p, generation = data
            if generation == self.generation:
                if self.trace and self.verbose:
                    g.trace(theId, p.h)
                return p
            else:
                if self.trace and self.verbose:
                    g.trace("*** wrong generation: %d ***" % theId)
                return None
        else:
            if self.trace and self.verbose:
                g.trace(theId, None)
            return None

    #@< Click Box...
    #@> onClickBoxClick
    def onClickBoxClick(self, event, p=None):
        c = self.c
        p1 = c.currentPosition()

        if not p:
            p = self.eventToPosition(event)
        if not p:
            return

        c.setLog()

        c.beginUpdate()
        try:
            if p and not g.doHook("boxclick1", c=c, p=p, v=p, event=event):
                c.endEditing()
                if p == p1 or self.initialClickExpandsOrContractsNode:
                    if p.isExpanded():
                        p.contract()
                    else:
                        p.expand()
                self.select(p)
                if c.frame.findPanel:
                    c.frame.findPanel.handleUserClick(p)
                if self.stayInTree:
                    c.treeWantsFocus()
                else:
                    c.bodyWantsFocus()
            g.doHook("boxclick2", c=c, p=p, v=p, event=event)
        finally:
            c.endUpdate()

    #@< Dragging (swingTree)
    #@> endDrag
    def endDrag(self, event):
        """The official helper of the onEndDrag event handler."""

        c = self.c
        p = self.drag_p
        c.setLog()
        canvas = self.canvas
        if not event:
            return

        c.beginUpdate()
        try:
            #@+<< set vdrag, childFlag >>
            #@> << set vdrag, childFlag >>
            x, y = event.x, event.y
            canvas_x = canvas.canvasx(x)
            canvas_y = canvas.canvasy(y)

            theId = self.canvas.find_closest(canvas_x, canvas_y)
            # theId = self.canvas.find_overlapping(canvas_x,canvas_y,canvas_x,canvas_y)

            vdrag = self.findPositionWithIconId(theId)
            childFlag = vdrag and vdrag.hasChildren() and vdrag.isExpanded()
            #@-<< set vdrag, childFlag >>
            if self.allow_clone_drags:
                if not self.look_for_control_drag_on_mouse_down:
                    self.controlDrag = c.frame.controlKeyIsDown

            redrawFlag = vdrag and vdrag.v.t != p.v.t
            if redrawFlag:  # Disallow drag to joined node.
                #@+<< drag p to vdrag >>
                #@ << drag p to vdrag >>
                # g.trace("*** end drag   ***",theId,x,y,p.h,vdrag.h)

                if self.controlDrag:  # Clone p and move the clone.
                    if childFlag:
                        c.dragCloneToNthChildOf(p, vdrag, 0)
                    else:
                        c.dragCloneAfter(p, vdrag)
                else:  # Just drag p.
                    if childFlag:
                        c.dragToNthChildOf(p, vdrag, 0)
                    else:
                        c.dragAfter(p, vdrag)
                #@-<< drag p to vdrag >>
            elif self.trace and self.verbose:
                g.trace("Cancel drag")

            # Reset the old cursor by brute force.
            self.canvas['cursor'] = "arrow"
            self.dragging = False
            self.drag_p = None
        finally:
            # Must set self.drag_p = None first.
            c.endUpdate(redrawFlag)
            c.recolor_now()  # Dragging can affect coloring.

    #@< startDrag
    # This precomputes numberOfVisibleNodes(), a significant optimization.
    # We also indicate where findPositionWithIconId() should start looking for tree id's.

    def startDrag(self, event, p=None):
        """The official helper of the onDrag event handler."""

        c = self.c
        canvas = self.canvas

        if not p:
            assert not self.drag_p
            x = canvas.canvasx(event.x)
            y = canvas.canvasy(event.y)
            theId = canvas.find_closest(x, y)
            # theId = canvas.find_overlapping(canvas_x,canvas_y,canvas_x,canvas_y)
            if theId is None:
                return
            try:
                theId = theId[0]
            except:
                pass
            p = self.ids.get(theId)
        if not p:
            return
        c.setLog()
        self.drag_p = p.copy()  # defensive programming: not needed.
        self.dragging = True
        # g.trace("*** start drag ***",theId,self.drag_p.h)
        # Only do this once: greatly speeds drags.
        self.savedNumberOfVisibleNodes = self.numberOfVisibleNodes()
        # g.trace('self.controlDrag',self.controlDrag)
        if self.allow_clone_drags:
            self.controlDrag = c.frame.controlKeyIsDown
            if self.look_for_control_drag_on_mouse_down:
                if self.enable_drag_messages:
                    if self.controlDrag:
                        g.es("dragged node will be cloned")
                    else:
                        g.es("dragged node will be moved")
        else:
            self.controlDrag = False
        self.canvas['cursor'] = "hand2"  # "center_ptr"

    #@ onContinueDrag
    def onContinueDrag(self, event):
        p = self.drag_p
        if not p:
            return

        try:
            canvas = self.canvas
            frame = self.c.frame
            if event:
                x, y = event.x, event.y
            else:
                x, y = frame.top.winfo_pointerx(), frame.top.winfo_pointery()
                # Stop the scrolling if we go outside the entire window.
                if x == -1 or y == -1:
                    return
            if self.dragging:  # This gets cleared by onEndDrag()
                #@+<< scroll the canvas as needed >>
                #@> << scroll the canvas as needed >>
                # Scroll the screen up or down one line if the cursor (y) is outside the canvas.
                h = canvas.winfo_height()

                if y < 0 or y > h:
                    lo, hi = frame.canvas.leo_treeBar.get()
                    n = self.savedNumberOfVisibleNodes
                    line_frac = 1.0 / float(n)
                    frac = g.choose(y < 0, lo - line_frac, lo + line_frac)
                    frac = min(frac, 1.0)
                    frac = max(frac, 0.0)
                    # g.es("lo,hi,frac:",lo,hi,frac)
                    canvas.yview("moveto", frac)

                    # Queue up another event to keep scrolling while the cursor is outside the canvas.
                    lo, hi = frame.canvas.leo_treeBar.get()
                    if (y < 0 and lo > 0.1) or (y > h and hi < 0.9):
                        pass  ### canvas.after_idle(self.onContinueDrag,None) # Don't propagate the event.
                #@-<< scroll the canvas as needed >>
        except:
            g.es_event_exception("continue drag")

    #@< onDrag
    def onDrag(self, event):
        c = self.c
        p = self.drag_p
        if not event:
            return

        c.setLog()

        if not self.dragging:
            if not g.doHook("drag1", c=c, p=p, v=p, event=event):
                self.startDrag(event)
            g.doHook("drag2", c=c, p=p, v=p, event=event)

        if not g.doHook("dragging1", c=c, p=p, v=p, event=event):
            self.onContinueDrag(event)
        g.doHook("dragging2", c=c, p=p, v=p, event=event)

    #@ onEndDrag
    def onEndDrag(self, event):
        """Tree end-of-drag handler called from vnode event handler."""

        c = self.c
        p = self.drag_p
        if not p:
            return

        c.setLog()

        if not g.doHook("enddrag1", c=c, p=p, v=p, event=event):
            self.endDrag(event)
        g.doHook("enddrag2", c=c, p=p, v=p, event=event)

    #@< Icon Box...
    #@> onIconBoxClick
    def onIconBoxClick(self, event, p=None):
        c = self.c
        tree = self

        if not p:
            p = self.eventToPosition(event)
        if not p:
            return

        c.setLog()

        if self.trace and self.verbose:
            g.trace()

        if not g.doHook("iconclick1", c=c, p=p, v=p, event=event):
            if event:
                self.onDrag(event)
            tree.endEditLabel()
            tree.select(p, scroll=False)
            if c.frame.findPanel:
                c.frame.findPanel.handleUserClick(p)
        g.doHook("iconclick2", c=c, p=p, v=p, event=event)

        return "break"  # disable expanded box handling.

    #@ onIconBoxRightClick
    def onIconBoxRightClick(self, event, p=None):
        """Handle a right click in any outline widget."""

        c = self.c

        if not p:
            p = self.eventToPosition(event)
        if not p:
            return

        c.setLog()

        try:
            if not g.doHook("iconrclick1", c=c, p=p, v=p, event=event):
                self.OnActivateHeadline(p)
                self.endEditLabel()
                self.OnPopup(p, event)
            g.doHook("iconrclick2", c=c, p=p, v=p, event=event)
        except:
            g.es_event_exception("iconrclick")

        return 'break'

    #@ onIconBoxDoubleClick
    def onIconBoxDoubleClick(self, event, p=None):
        c = self.c

        if not p:
            p = self.eventToPosition(event)
        if not p:
            return

        c.setLog()

        if self.trace and self.verbose:
            g.trace()

        try:
            if not g.doHook("icondclick1", c=c, p=p, v=p, event=event):
                self.endEditLabel()  # Bug fix: 11/30/05
                self.OnIconDoubleClick(p)  # Call the method in the base class.
            g.doHook("icondclick2", c=c, p=p, v=p, event=event)
        except:
            g.es_event_exception("icondclick")

        return 'break'  # 11/19/06

    #@< OnActivateHeadline (swingTree)
    def OnActivateHeadline(self, p, event=None):
        '''Handle common process when any part of a headline is clicked.'''

        # g.trace(p.h)

        returnVal = 'break'  # Default: do nothing more.
        trace = False

        try:
            c = self.c
            c.setLog()
            #@+<< activate this window >>
            #@> << activate this window >>
            if p == c.currentPosition():
                if trace:
                    g.trace('current', 'active', self.active)
                self.editLabel(p)  # sets focus.
                # If we are active, pass the event along so the click gets handled.
                # Otherwise, do *not* pass the event along so the focus stays the same.
                returnVal = g.choose(self.active, 'continue', 'break')
                self.active = True
            else:
                if trace:
                    g.trace("not current")
                self.select(p, scroll=False)
                w = c.frame.body.bodyCtrl
                if c.frame.findPanel:
                    c.frame.findPanel.handleUserClick(p)
                if p.v.t.insertSpot != None:
                    spot = p.v.t.insertSpot
                    w.setInsertPoint(spot)
                    w.see(spot)
                else:
                    w.setInsertPoint(0)
                # An important detail.
                # The *canvas* (not the headline) gets the focus so that
                # tree bindings take priority over text bindings.
                c.treeWantsFocus()
                self.active = False
                returnVal = 'break'
            #@-<< activate this window >>
        except:
            g.es_event_exception("activate tree")

        return returnVal

    #@< Text Box...
    #@> configureTextState
    def configureTextState(self, p):
        c = self.c

        if not p:
            return

        # g.trace(p.h,self.c._currentPosition)

        if c.isCurrentPosition(p):
            if p == self.editPosition():
                self.setEditLabelState(p)  # selected, editing.
            else:
                self.setSelectedLabelState(p)  # selected, not editing.
        else:
            self.setUnselectedLabelState(p)  # unselected

    #@ onCtontrolT
    # This works around an apparent Tk bug.

    def onControlT(self, event=None):
        # If we don't inhibit further processing the Tx.Text widget switches characters!
        return "break"

    #@ onHeadlineClick
    def onHeadlineClick(self, event, p=None):
        # g.trace('p',p)
        c = self.c
        w = event.widget

        if not p:
            try:
                p = w.leo_position
            except AttributeError:
                g.trace('*' * 20, 'oops')
        if not p:
            return 'break'

        # g.trace(g.app.gui.widget_name(w)) #p.h)

        c.setLog()

        try:
            if not g.doHook("headclick1", c=c, p=p, v=p, event=event):
                returnVal = self.OnActivateHeadline(p)
            g.doHook("headclick2", c=c, p=p, v=p, event=event)
        except:
            returnVal = 'break'
            g.es_event_exception("headclick")

        # g.trace('returnVal',returnVal,'stayInTree',self.stayInTree)
        return returnVal

    #@ onHeadlineRightClick
    def onHeadlineRightClick(self, event):
        """Handle a right click in any outline widget."""

        c = self.c
        w = event.widget

        try:
            p = w.leo_position
        except AttributeError:
            g.trace('*' * 20, 'oops')
            return 'break'

        c.setLog()

        try:
            if not g.doHook("headrclick1", c=c, p=p, v=p, event=event):
                self.OnActivateHeadline(p)
                self.endEditLabel()
                self.OnPopup(p, event)
            g.doHook("headrclick2", c=c, p=p, v=p, event=event)
        except:
            g.es_event_exception("headrclick")

        # 'continue' *is* correct here.
        # 'break' would make it impossible to unselect the headline text.
        return 'continue'

    #@< tree.OnDeactivate
    def OnDeactivate(self, event=None):
        """Deactivate the tree pane, dimming any headline being edited."""

        # __pychecker__ = '--no-argsused' # event not used.

        tree = self
        c = self.c

        # g.trace(g.callers())

        c.beginUpdate()
        try:
            tree.endEditLabel()
            tree.dimEditLabel()
        finally:
            c.endUpdate(False)

    #@ tree.OnPopup & allies
    def OnPopup(self, p, event):
        """Handle right-clicks in the outline.

        This is *not* an event handler: it is called from other event handlers."""

        # Note: "headrclick" hooks handled by vnode callback routine.

        if event != None:
            c = self.c
            c.setLog()

            if not g.doHook("create-popup-menu", c=c, p=p, v=p, event=event):
                self.createPopupMenu(event)
            if not g.doHook("enable-popup-menu-items", c=c, p=p, v=p, event=event):
                self.enablePopupMenuItems(p, event)
            if not g.doHook("show-popup-menu", c=c, p=p, v=p, event=event):
                self.showPopupMenu(event)

        return "break"

    #@> OnPopupFocusLost
    # On Linux we must do something special to make the popup menu "unpost" if the
    # mouse is clicked elsewhere. So we have to catch the <FocusOut> event and
    # explicitly unpost. In order to process the <FocusOut> event, we need to be able
    # to find the reference to the popup window again, so this needs to be an
    # attribute of the tree object; hence, "self.popupMenu".
    #
    # Aside: though Tk tries to be muli-platform, the interaction with different
    # window managers does cause small differences that will need to be compensated by
    # system specific application code. :-(
    #@@c

    # 20-SEP-2002 DTHEIN: This event handler is only needed for Linux.

    def OnPopupFocusLost(self, event=None):
        # __pychecker__ = '--no-argsused' # event not used.

        self.popupMenu.unpost()

    #@ createPopupMenu
    def createPopupMenu(self, event):
        # __pychecker__ = '--no-argsused' # event not used.

        c = self.c
        frame = c.frame

        # If we are going to recreate it, we had better destroy it.
        if self.popupMenu:
            self.popupMenu.destroy()
            self.popupMenu = None

        self.popupMenu = menu = Tk.Menu(g.app.root, tearoff=0)

        # Add the Open With entries if they exist.
        if g.app.openWithTable:
            frame.menu.createOpenWithMenuItemsFromTable(menu, g.app.openWithTable)
            table = (("-", None, None),)
            frame.menu.createMenuEntries(menu, table)

        #@+<< Create the menu table >>
        #@> << Create the menu table >>
        table = (
            ("&Read @file Nodes", c.readAtFileNodes),
            ("&Write @file Nodes", c.fileCommands.writeAtFileNodes),
            ("-", None),
            ("&Tangle", c.tangle),
            ("&Untangle", c.untangle),
            ("-", None),
            ("Toggle Angle &Brackets", c.toggleAngleBrackets),
            ("-", None),
            ("Cut Node", c.cutOutline),
            ("Copy Node", c.copyOutline),
            ("&Paste Node", c.pasteOutline),
            ("&Delete Node", c.deleteOutline),
            ("-", None),
            ("&Insert Node", c.insertHeadline),
            ("&Clone Node", c.clone),
            ("Sort C&hildren", c.sortChildren),
            ("&Sort Siblings", c.sortSiblings),
            ("-", None),
            ("Contract Parent", c.contractParent),
        )
        #@-<< Create the menu table >>

        # New in 4.4.  There is no need for a dontBind argument because
        # Bindings from tables are ignored.
        frame.menu.createMenuEntries(menu, table)

    #@< enablePopupMenuItems
    def enablePopupMenuItems(self, v, event):
        """Enable and disable items in the popup menu."""

        # __pychecker__ = '--no-argsused' # event not used.

        c = self.c
        menu = self.popupMenu

        #@+<< set isAtRoot and isAtFile if v's tree contains @root or @file nodes >>
        #@> << set isAtRoot and isAtFile if v's tree contains @root or @file nodes >>
        isAtFile = False
        isAtRoot = False

        for v2 in v.self_and_subtree():
            if isAtFile and isAtRoot:
                break
            if v2.isAtFileNode() or v2.isAtAsisFileNode() or v2.isAtNoSentFileNode():
                isAtFile = True

            isRoot, junk = g.is_special(v2.bodyString(), 0, "@root")
            if isRoot:
                isAtRoot = True
        #@-<< set isAtRoot and isAtFile if v's tree contains @root or @file nodes >>
        isAtFile = g.choose(isAtFile, 1, 0)
        isAtRoot = g.choose(isAtRoot, 1, 0)
        canContract = v.parent() != None
        canContract = g.choose(canContract, 1, 0)

        enable = self.frame.menu.enableMenu

        for name in ("Read @file Nodes", "Write @file Nodes"):
            enable(menu, name, isAtFile)
        for name in ("Tangle", "Untangle"):
            enable(menu, name, isAtRoot)

        enable(menu, "Cut Node", c.canCutOutline())
        enable(menu, "Delete Node", c.canDeleteHeadline())
        enable(menu, "Paste Node", c.canPasteOutline())
        enable(menu, "Sort Children", c.canSortChildren())
        enable(menu, "Sort Siblings", c.canSortSiblings())
        enable(menu, "Contract Parent", c.canContractParent())

    #@< showPopupMenu
    def showPopupMenu(self, event):
        """Show a popup menu."""

        # c = self.c ; menu = self.popupMenu

    #@< onTreeClick
    def onTreeClick(self, event=None):
        '''Handle an event in the tree canvas, outside of any tree widget.'''

        c = self.c

        # New in Leo 4.4.2: a kludge: disable later event handling after a double-click.
        # This allows focus to stick in newly-opened files opened by double-clicking an @url node.
        if c.doubleClickFlag:
            c.doubleClickFlag = False
        else:
            c.treeWantsFocus()

        return 'break'

    #@< Incremental drawing...
    #@> allocateNodes
    def allocateNodes(self, where, lines):
        """Allocate Tk widgets in nodes that will become visible as the result of an upcoming scroll"""

        assert where in ("above", "below")

        # print "allocateNodes: %d lines %s visible area" % (lines,where)

        # Expand the visible area: a little extra delta is safer.
        delta = lines * (self.line_height + 4)
        y1, y2 = self.visibleArea

        if where == "below":
            y2 += delta
        else:
            y1 = max(0.0, y1 - delta)

        self.expandedVisibleArea = y1, y2
        # print "expandedArea:   %5.1f %5.1f" % (y1,y2)

        # Allocate all nodes in expanded visible area.
        self.updatedNodeCount = 0
        self.updateTree(self.c.rootPosition(), self.root_left, self.root_top, 0, 0)
        # if self.updatedNodeCount: print "updatedNodeCount:", self.updatedNodeCount

    #@ allocateNodesBeforeScrolling
    def allocateNodesBeforeScrolling(self, args):
        """Calculate the nodes that will become visible as the result of an upcoming scroll.

        args is the tuple passed to the Tk.Canvas.yview method"""

        if not self.allocateOnlyVisibleNodes:
            return

        # print "allocateNodesBeforeScrolling:",self.redrawCount,args

        assert self.visibleArea
        assert len(args) == 2 or len(args) == 3
        kind = args[0]
        n = args[1]
        lines = 2  # Update by 2 lines to account for rounding.
        if len(args) == 2:
            assert kind == "moveto"
            frac1, frac2 = args
            if float(n) != frac1:
                where = g.choose(n < frac1, "above", "below")
                self.allocateNodes(where=where, lines=lines)
        else:
            assert kind == "scroll"
            linesPerPage = self.canvas.winfo_height() / self.line_height + 2
            n = int(n)
            assert abs(n) == 1
            where = g.choose(n == 1, "below", "above")
            lines = g.choose(args[2] == "pages", linesPerPage, lines)
            self.allocateNodes(where=where, lines=lines)

    #@ updateNode
    def updateNode(self, p, x, y):
        """Draw a node that may have become visible as a result of a scrolling operation"""

        c = self.c

        if self.inExpandedVisibleArea(y):
            # This check is a major optimization.
            if not c.edit_widget(p):
                return self.force_draw_node(p, x, y)
            else:
                return self.line_height

        return self.line_height

    #@ setVisibleAreaToFullCanvas
    def setVisibleAreaToFullCanvas(self):
        if self.visibleArea:
            y1, y2 = self.visibleArea
            y2 = max(y2, y1 + self.canvas.winfo_height())
            self.visibleArea = y1, y2

    #@ setVisibleArea
    def setVisibleArea(self, args):
        r1, r2 = args
        r1, r2 = float(r1), float(r2)
        # print "scroll ratios:",r1,r2

        try:
            s = self.canvas.cget("scrollregion")
            x1, y1, x2, y2 = g.scanf(s, "%d %d %d %d")
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        except:
            self.visibleArea = None
            return

        scroll_h = y2 - y1
        # print "height of scrollregion:", scroll_h

        vy1 = y1 + (scroll_h * r1)
        vy2 = y1 + (scroll_h * r2)
        self.visibleArea = vy1, vy2
        # print "setVisibleArea: %5.1f %5.1f" % (vy1,vy2)

    #@ tree.updateTree
    def updateTree(self, v, x, y, h, level):
        yfirst = y
        if level == 0:
            yfirst += 10
        while v:
            # g.trace(x,y,v)
            h, indent = self.updateNode(v, x, y)
            y += h
            if v.isExpanded() and v.firstChild():
                y = self.updateTree(v.firstChild(), x + indent, y, h, level + 1)
            v = v.next()
        return y

    #@< Selecting & editing... (swingTree)
    #@> dimEditLabel, undimEditLabel
    # Convenience methods so the caller doesn't have to know the present edit node.

    def dimEditLabel(self):
        p = self.c.currentPosition()
        self.setSelectedLabelState(p)

    def undimEditLabel(self):
        p = self.c.currentPosition()
        self.setSelectedLabelState(p)

    #@ tree.editLabel
    def editLabel(self, p, selectAll=False):
        """Start editing p's headline."""

        c = self.c
        trace = not g.app.unitTesting and (False or self.trace_edit)

        if p and p != self.editPosition():
            if trace:
                g.trace(p.h, g.choose(c.edit_widget(p), '', 'no edit widget'))

            c.beginUpdate()
            try:
                self.endEditLabel()
            finally:
                c.endUpdate(True)

        self.setEditPosition(p)  # That is, self._editPosition = p

        if trace:
            g.trace(c.edit_widget(p))

        if p and c.edit_widget(p):
            self.revertHeadline = p.h  # New in 4.4b2: helps undo.
            self.setEditLabelState(p, selectAll=selectAll)  # Sets the focus immediately.
            c.headlineWantsFocus(p)  # Make sure the focus sticks.

    #@ tree.set...LabelState
    #@> setEditLabelState
    def setEditLabelState(self, p, selectAll=False):  # selected, editing
        c = self.c
        w = c.edit_widget(p)

        if p and w:
            # g.trace('*****',g.callers())
            c.widgetWantsFocusNow(w)
            self.setEditHeadlineColors(p)
            selectAll = selectAll or self.select_all_text_when_editing_headlines
            if selectAll:
                w.setSelectionRange(0, 'end', insert='end')
            else:
                w.setInsertPoint('end')  # Clears insert point.
        else:
            g.trace('no edit_widget')

    setNormalLabelState = setEditLabelState  # For compatibility.

    #@ setSelectedLabelState
    def setSelectedLabelState(self, p):  # selected, disabled
        # g.trace(p.h,g.callers())

        c = self.c

        if p and c.edit_widget(p):
            self.setDisabledHeadlineColors(p)

    #@ setUnselectedLabelState
    def setUnselectedLabelState(self, p):  # not selected.
        c = self.c

        if p and c.edit_widget(p):
            self.setUnselectedHeadlineColors(p)

    #@ setDisabledHeadlineColors
    def setDisabledHeadlineColors(self, p):
        c = self.c
        w = c.edit_widget(p)

        if self.trace and self.verbose:
            if not self.redrawing:
                g.trace("%10s %d %s" % ("disabled", id(w), p.h))
                # import traceback ; traceback.print_stack(limit=6)

        fg = self.headline_text_selected_foreground_color or 'black'
        bg = self.headline_text_selected_background_color or 'grey80'
        selfg = self.headline_text_editing_selection_foreground_color
        selbg = self.headline_text_editing_selection_background_color

        try:
            w.configure(
                state="disabled",
                highlightthickness=0,
                fg=fg,
                bg=bg,
                selectbackground=bg,
                selectforeground=fg,
                highlightbackground=bg,
            )
        except:
            g.es_exception()

    #@ setEditHeadlineColors
    def setEditHeadlineColors(self, p):
        c = self.c
        w = c.edit_widget(p)

        if self.trace and self.verbose:
            if not self.redrawing:
                print("%10s %d %s" % ("edit", id(2), p.h))

        fg = self.headline_text_editing_foreground_color or 'black'
        bg = self.headline_text_editing_background_color or 'white'
        selfg = self.headline_text_editing_selection_foreground_color or 'white'
        selbg = self.headline_text_editing_selection_background_color or 'black'

        try:  # Use system defaults for selection foreground/background
            w.configure(
                state="normal",
                highlightthickness=1,
                fg=fg,
                bg=bg,
                selectforeground=selfg,
                selectbackground=selbg,
            )
        except:
            g.es_exception()

    #@ setUnselectedHeadlineColors
    def setUnselectedHeadlineColors(self, p):
        c = self.c
        w = c.edit_widget(p)

        if self.trace and self.verbose:
            if not self.redrawing:
                print("%10s %d %s" % ("unselect", id(w), p.h))
                # import traceback ; traceback.print_stack(limit=6)

        fg = self.headline_text_unselected_foreground_color or 'black'
        bg = self.headline_text_unselected_background_color or 'white'

        try:
            w.configure(
                state="disabled",
                highlightthickness=0,
                fg=fg,
                bg=bg,
                selectbackground=bg,
                selectforeground=fg,
                highlightbackground=bg,
            )
        except:
            g.es_exception()

    #@-others


#@<4 leoSwingGui
class swingGui(leoGui.leoGui):
    """A class encapulating all calls to swing."""

    #@+others
    #@> swingGui birth & death
    #@>  swingGui.__init__
    def __init__(self):
        # Initialize the base class.
        leoGui.leoGui.__init__(self, 'swing')

        self.root = None

        self.bodyTextWidget = leoSwingFrame.leoSwingTextWidget
        self.plainTextWidget = leoSwingFrame.leoSwingTextWidget

        self.bitmap_name = None
        self.bitmap = None

        self.defaultFont = None
        self.defaultFontFamily = None

        # self.win32clipboard = None

    #@ createKeyHandlerClass (swingGui)
    def createKeyHandlerClass(self, c, useGlobalKillbuffer=True, useGlobalRegisters=True):
        import leoSwingFrame  # Do this here to break any circular dependency.

        return leoSwingFrame.swingKeyHandlerClass(c, useGlobalKillbuffer, useGlobalRegisters)

    #@ runMainLoop (swingGui)
    def runMainLoop(self):
        '''Start the swing main loop.'''

        if self.script:
            log = g.app.log
            if log:
                print('Start of batch script...\n')
                log.c.executeScript(script=self.script)
                print('End of batch script')
            else:
                print('no log, no commander for executeScript in swingGui.runMainLoop')
        else:
            pass  # no need to invoke a swing main loop.

    #@ Not used
    def createRootWindow(self):
        pass

    def destroySelf(self):
        pass

    def killGui(self, exitFlag=True):
        """Destroy a gui and terminate Leo if exitFlag is True."""
        pass

    def recreateRootWindow(self):
        """A do-nothing base class to create the hidden root window of a gui
        after a previous gui has terminated with killGui(False)."""
        pass

    if 0:
        #@+others
        #@> swingGui.setDefaultIcon
        def setDefaultIcon(self):
            """Set the icon to be used in all Leo windows.

            This code does nothing for Tk versions before 8.4.3."""

            gui = self

            try:
                version = gui.root.getvar("tk_patchLevel")
                # g.trace(repr(version),g.CheckVersion(version,"8.4.3"))
                if g.CheckVersion(version, "8.4.3") and sys.platform == "win32":
                    # tk 8.4.3 or greater: load a 16 by 16 icon.
                    path = g.os_path_join(g.app.loadDir, "..", "Icons")
                    if g.os_path_exists(path):
                        theFile = g.os_path_join(path, "LeoApp16.ico")
                        if g.os_path_exists(path):
                            self.bitmap = Tk.BitmapImage(theFile)
                        else:
                            g.es("LeoApp16.ico not in Icons directory", color="red")
                    else:
                        g.es("Icons directory not found: " + path, color="red")
            except:
                print("exception setting bitmap")
                import traceback

                traceback.print_exc()

        #@ swingGui.getDefaultConfigFont
        def getDefaultConfigFont(self, config):
            """Get the default font from a new text widget."""

            if not self.defaultFontFamily:
                # WARNING: retain NO references to widgets or fonts here!
                w = g.app.gui.plainTextWidget()
                fn = w.cget("font")
                font = swingFont.Font(font=fn)
                family = font.cget("family")
                self.defaultFontFamily = family[:]
                # print '***** getDefaultConfigFont',repr(family)

            config.defaultFont = None
            config.defaultFontFamily = self.defaultFontFamily

        #@-others

    #@<2 swingGui dialogs & panels
    def runAboutLeoDialog(self, c, version, theCopyright, url, email):
        """Create and run a swing About Leo dialog."""
        d = leoSwingDialog.swingAboutLeo(c, version, theCopyright, url, email)
        return d.run(modal=False)

    def runAskLeoIDDialog(self):
        """Create and run a dialog to get g.app.LeoID."""
        d = leoSwingDialog.swingAskLeoID()
        return d.run(modal=True)

    def runAskOkDialog(self, c, title, message=None, text="Ok"):
        """Create and run a swing an askOK dialog ."""
        d = leoSwingDialog.swingAskOk(c, title, message, text)
        return d.run(modal=True)

    def runAskOkCancelNumberDialog(self, c, title, message):
        """Create and run askOkCancelNumber dialog ."""
        d = leoSwingDialog.swingAskOkCancelNumber(c, title, message)
        return d.run(modal=True)

    def runAskOkCancelStringDialog(self, c, title, message):
        """Create and run askOkCancelString dialog ."""
        d = leoSwingDialog.swingAskOkCancelString(c, title, message)
        return d.run(modal=True)

    def runAskYesNoDialog(self, c, title, message=None):
        """Create and run an askYesNo dialog."""
        d = leoSwingDialog.swingAskYesNo(c, title, message)
        return d.run(modal=True)

    def runAskYesNoCancelDialog(
        self, c, title, message=None, yesMessage="Yes", noMessage="No", defaultButton="Yes"
    ):
        """Create and run an askYesNoCancel dialog ."""
        d = leoSwingDialog.swingAskYesNoCancel(
            c, title, message, yesMessage, noMessage, defaultButton
        )
        return d.run(modal=True)

    #@> swingGui.createSpellTab
    def createSpellTab(self, c, spellHandler, tabName):
        ### return leoSwingFind.swingSpellTab(c,spellHandler,tabName)

        pass

    #@ swingGui file dialogs
    # We no longer specify default extensions so that we can open and save files without extensions.
    #@> runOpenFileDialog
    def runOpenFileDialog(self, title, filetypes, defaultextension, multiple=False):
        """Create and run an swing open file dialog ."""

        # __pychecker__ = '--no-argsused' # defaultextension not used.

        initialdir = g.app.globalOpenDir or g.os_path_abspath(os.getcwd())

        if multiple:
            # askopenfilenames requires Python 2.3 and Tk 8.4.
            version = '.'.join([str(sys.version_info[i]) for i in (0, 1, 2)])
            if g.CheckVersion(version, "2.3") and g.CheckVersion(
                self.root.getvar("tk_patchLevel"), "8.4"
            ):
                files = swingFileDialog.askopenfilenames(
                    title=title, filetypes=filetypes, initialdir=initialdir
                )
                # g.trace(files)
                return list(files)
            else:
                # Get one file and return it as a list.
                theFile = swingFileDialog.askopenfilename(
                    title=title, filetypes=filetypes, initialdir=initialdir
                )
                return [theFile]
        else:
            # Return a single file name as a string.
            return swingFileDialog.askopenfilename(
                title=title, filetypes=filetypes, initialdir=initialdir
            )

    #@ runSaveFileDialog
    def runSaveFileDialog(self, initialfile, title, filetypes, defaultextension):
        """Create and run an swing save file dialog ."""

        # __pychecker__ = '--no-argsused' # defaultextension not used.

        initialdir = (g.app.globalOpenDir or g.os_path_abspath(os.getcwd()),)

        return swingFileDialog.asksaveasfilename(
            initialdir=initialdir, initialfile=initialfile, title=title, filetypes=filetypes
        )

    #@< swingGui panels
    def createComparePanel(self, c):
        """Create a swing color picker panel."""
        # return leoSwingComparePanel.leoSwingComparePanel(c)

    def createFindPanel(self, c):
        """Create a hidden swing find panel."""
        # panel = leoSwingFind.leoSwingFind(c)
        # panel.top.withdraw()
        # return panel

    def createFindTab(self, c, parentFrame):
        """Create a swing find tab in the indicated frame."""
        # return leoSwingFind.swingFindTab(c,parentFrame)

    def createLeoFrame(self, title):
        """Create a new Leo frame."""
        gui = self
        return leoSwingFrame.leoSwingFrame(title, gui)

    #@< swingGui utils (TO DO)
    #@> Clipboard (swingGui)
    #@> replaceClipboardWith
    def replaceClipboardWith(self, s):
        # g.app.gui.win32clipboard is always None.
        wcb = g.app.gui.win32clipboard

        if wcb:
            try:
                wcb.OpenClipboard(0)
                wcb.EmptyClipboard()
                wcb.SetClipboardText(s)
                wcb.CloseClipboard()
            except:
                g.es_exception()
        else:
            self.root.clipboard_clear()
            self.root.clipboard_append(s)

    #@ getTextFromClipboard
    def getTextFromClipboard(self):
        # g.app.gui.win32clipboard is always None.
        wcb = g.app.gui.win32clipboard

        if wcb:
            try:
                wcb.OpenClipboard(0)
                data = wcb.GetClipboardData()
                wcb.CloseClipboard()
                # g.trace(data)
                return data
            except TypeError:
                # g.trace(None)
                return None
            except:
                g.es_exception()
                return None
        else:
            try:
                s = self.root.selection_get(selection="CLIPBOARD")
                return s
            except:
                return None

    #@< color
    # g.es calls gui.color to do the translation,
    # so most code in Leo's core can simply use Tk color names.

    def color(self, color):
        '''Return the gui-specific color corresponding to the Tk color name.'''
        return color

    #@ Dialog
    #@> get_window_info
    # WARNING: Call this routine _after_ creating a dialog.
    # (This routine inhibits the grid and pack geometry managers.)

    def get_window_info(self, top):
        top.update_idletasks()  # Required to get proper info.

        # Get the information about top and the screen.
        geom = top.geometry()  # geom = "WidthxHeight+XOffset+YOffset"
        dim, x, y = string.split(geom, '+')
        w, h = string.split(dim, 'x')
        w, h, x, y = int(w), int(h), int(x), int(y)

        return w, h, x, y

    #@ center_dialog
    def center_dialog(self, top):
        """Center the dialog on the screen.

        WARNING: Call this routine _after_ creating a dialog.
        (This routine inhibits the grid and pack geometry managers.)"""

        sw = top.winfo_screenwidth()
        sh = top.winfo_screenheight()
        w, h, x, y = self.get_window_info(top)

        # Set the new window coordinates, leaving w and h unchanged.
        x = (sw - w) / 2
        y = (sh - h) / 2
        top.geometry("%dx%d%+d%+d" % (w, h, x, y))

        return w, h, x, y

    #@ create_labeled_frame
    # Returns frames w and f.
    # Typically the caller would pack w into other frames, and pack content into f.

    def create_labeled_frame(self, parent, caption=None, relief="groove", bd=2, padx=0, pady=0):
        # Create w, the master frame.
        w = Tk.Frame(parent)
        w.grid(sticky="news")

        # Configure w as a grid with 5 rows and columns.
        # The middle of this grid will contain f, the expandable content area.
        w.columnconfigure(1, minsize=bd)
        w.columnconfigure(2, minsize=padx)
        w.columnconfigure(3, weight=1)
        w.columnconfigure(4, minsize=padx)
        w.columnconfigure(5, minsize=bd)

        w.rowconfigure(1, minsize=bd)
        w.rowconfigure(2, minsize=pady)
        w.rowconfigure(3, weight=1)
        w.rowconfigure(4, minsize=pady)
        w.rowconfigure(5, minsize=bd)

        # Create the border spanning all rows and columns.
        border = Tk.Frame(w, bd=bd, relief=relief)  # padx=padx,pady=pady)
        border.grid(row=1, column=1, rowspan=5, columnspan=5, sticky="news")

        # Create the content frame, f, in the center of the grid.
        f = Tk.Frame(w, bd=bd)
        f.grid(row=3, column=3, sticky="news")

        # Add the caption.
        if caption and len(caption) > 0:
            caption = Tk.Label(parent, text=caption, highlightthickness=0, bd=0)
            # caption.tkraise(w)
            caption.grid(in_=w, row=0, column=2, rowspan=2, columnspan=3, padx=4, sticky="w")

        return w, f

    #@< Events (swingGui)
    def event_generate(self, w, kind, *args, **keys):
        '''Generate an event.'''
        return w.event_generate(kind, *args, **keys)

    def eventChar(self, event, c=None):
        '''Return the char field of an event.'''
        return event and event.char or ''

    def eventKeysym(self, event, c=None):
        '''Return the keysym value of an event.'''
        return event and event.keysym

    def eventWidget(self, event, c=None):
        '''Return the widget field of an event.'''
        return event and event.widget

    def eventXY(self, event, c=None):
        if event:
            return event.x, event.y
        else:
            return 0, 0

    #@ Focus
    #@> swingGui.get_focus
    def get_focus(self, c):
        """Returns the widget that has focus, or body if None."""

        return c.frame.top.focus_displayof()

    #@ swing.Gui.set_focus
    set_focus_count = 0

    def set_focus(self, c, w):
        # __pychecker__ = '--no-argsused' # c not used at present.

        """Put the focus on the widget."""

        if not g.app.unitTesting and c and c.config.getBool('trace_g.app.gui.set_focus'):
            self.set_focus_count += 1
            # Do not call trace here: that might affect focus!
            print(
                'gui.set_focus: %4d %10s %s'
                % (self.set_focus_count, c and c.shortFileName(), c and c.widget_name(w)),
                g.callers(5),
            )

        if w:
            try:
                if 0:  # No longer needed.
                    # A call to findTab.bringToFront caused
                    # the focus problems with Pmw.Notebook.
                    w.update()

                # It's possible that the widget doesn't exist now.
                w.focus_set()
                return True
            except Exception:
                # g.es_exception()
                return False

    #@< Font
    #@> swingGui.getFontFromParams
    def getFontFromParams(self, family, size, slant, weight, defaultSize=12):
        # __pychecker__ = '--no-argsused' # defaultSize not used.

        family_name = family

        try:
            font = swingFont.Font(family=family, size=size, slant=slant, weight=weight)
            # if g.app.trace: g.trace(font)
            return font
        except:
            g.es("exception setting font from ", family_name)
            g.es("family,size,slant,weight:", family, size, slant, weight)
            # g.es_exception() # This just confuses people.
            return g.app.config.defaultFont

    #@< getFullVersion
    def getFullVersion(self):
        swingLevel = '<swingLevel>'
        return 'swing %s' % (swingLevel)

    #@ Icons
    #@> attachLeoIcon & createLeoIcon
    def attachLeoIcon(self, w):
        """Try to attach a Leo icon to the Leo Window.

        Use tk's wm_iconbitmap function if available (tk 8.3.4 or greater).
        Otherwise, try to use the Python Imaging Library and the tkIcon package."""

        if self.bitmap != None:
            # We don't need PIL or tkicon: this is tk 8.3.4 or greater.
            try:
                w.wm_iconbitmap(self.bitmap)
            except:
                self.bitmap = None

        if self.bitmap == None:
            try:
                #@+<< try to use the PIL and tkIcon packages to draw the icon >>
                #@> << try to use the PIL and tkIcon packages to draw the icon >>
                #
                # Download PIL    from http://www.pythonware.com/downloads/index.htm#pil
                # Download tkIcon from http://www.effbot.org/downloads/#tkIcon
                #
                # Many thanks to Jonathan M. Gilligan for suggesting this code.
                #@@c

                import Image
                import tkIcon  # pychecker complains, but this *is* used.

                # Wait until the window has been drawn once before attaching the icon in OnVisiblity.
                def visibilityCallback(event, self=self, w=w):
                    try:
                        self.leoIcon.attach(w.winfo_id())
                    except:
                        pass

                w.bind("<Visibility>", visibilityCallback)

                if not self.leoIcon:
                    # Load a 16 by 16 gif.  Using .gif rather than an .ico allows us to specify transparency.
                    icon_file_name = g.os_path_join(g.app.loadDir, '..', 'Icons', 'LeoWin.gif')
                    icon_file_name = g.os_path_normpath(icon_file_name)
                    icon_image = Image.open(icon_file_name)
                    if 1:  # Doesn't resize.
                        self.leoIcon = self.createLeoIcon(icon_image)
                    else:  # Assumes 64x64
                        self.leoIcon = tkIcon.Icon(icon_image)
                #@-<< try to use the PIL and tkIcon packages to draw the icon >>
            except:
                # import traceback ; traceback.print_exc()
                # g.es_exception()
                self.leoIcon = None

    #@<2 Idle Time
    #@> swingGui.setIdleTimeHook
    def setIdleTimeHook(self, idleTimeHookHandler):
        pass

    #@ setIdleTimeHookAfterDelay
    def setIdleTimeHookAfterDelay(self, idleTimeHookHandler):
        if self.root:
            g.app.root.after(g.app.idleTimeDelay, idleTimeHookHandler)

    #@< isTextWidget
    def isTextWidget(self, w):
        '''Return True if w is a Text widget suitable for text-oriented commands.'''

        return w and isinstance(w, leoFrame.stringTextWidget)  ### Tk.Text)

    #@ makeScriptButton
    def makeScriptButton(
        self,
        c,
        p=None,  # A node containing the script.
        script=None,  # The script itself.
        buttonText=None,
        balloonText='Script Button',
        shortcut=None,
        bg='LightSteelBlue1',
        define_g=True,
        define_name='__main__',
        silent=False,  # Passed on to c.executeScript.
    ):
        '''Create a script button for the script in node p.
        The button's text defaults to p.headString'''

        k = c.k
        if p and not buttonText:
            buttonText = p.h.strip()
        if not buttonText:
            buttonText = 'Unnamed Script Button'
        #@+<< create the button b >>
        #@> << create the button b >>
        iconBar = c.frame.getIconBarObject()
        b = iconBar.add(text=buttonText)

        #@-<< create the button b >>
        #@+<< define the callbacks for b >>
        #@ << define the callbacks for b >>
        def deleteButtonCallback(event=None, b=b, c=c):
            if b:
                b.pack_forget()
            c.bodyWantsFocus()

        def executeScriptCallback(
            event=None, b=b, c=c, buttonText=buttonText, p=p and p.copy(), script=script
        ):
            if c.disableCommandsMessage:
                g.es(c.disableCommandsMessage, color='blue')
            else:
                g.app.scriptDict = {}
                c.executeScript(
                    p=p, script=script, define_g=define_g, define_name=define_name, silent=silent
                )
                # Remove the button if the script asks to be removed.
                if g.app.scriptDict.get('removeMe'):
                    g.es("Removing '%s' button at its request" % buttonText)
                    b.pack_forget()
            # Do not assume the script will want to remain in this commander.

        #@-<< define the callbacks for b >>
        b.configure(command=executeScriptCallback)
        b.bind('<3>', deleteButtonCallback)
        if shortcut:
            #@+<< bind the shortcut to executeScriptCallback >>
            #@ << bind the shortcut to executeScriptCallback >>
            func = executeScriptCallback
            shortcut = k.canonicalizeShortcut(shortcut)
            ok = k.bindKey('button', shortcut, func, buttonText)
            if ok:
                g.es_print('Bound @button %s to %s' % (buttonText, shortcut), color='blue')
            #@-<< bind the shortcut to executeScriptCallback >>
        #@+<< create press-buttonText-button command >>
        #@ << create press-buttonText-button command >>
        aList = [g.choose(ch.isalnum(), ch, '-') for ch in buttonText]

        buttonCommandName = ''.join(aList)
        buttonCommandName = buttonCommandName.replace('--', '-')
        buttonCommandName = 'press-%s-button' % buttonCommandName.lower()

        # This will use any shortcut defined in an @shortcuts node.
        k.registerCommand(
            buttonCommandName, None, executeScriptCallback, pane='button', verbose=False
        )
        #@-<< create press-buttonText-button command >>

    #@<2 class leoKeyEvent (swingGui)
    class leoKeyEvent:
        '''A gui-independent wrapper for gui events.'''

        def __init__(self, event, c):
            # g.trace('leoKeyEvent(swingGui)')
            self.actualEvent = event
            self.c = c  # Required to access c.k tables.
            self.char = hasattr(event, 'char') and event.char or ''
            self.keysym = hasattr(event, 'keysym') and event.keysym or ''
            self.w = hasattr(event, 'widget') and event.widget or None
            self.x = hasattr(event, 'x') and event.x or 0
            self.y = hasattr(event, 'y') and event.y or 0
            # Support for fastGotoNode plugin
            self.x_root = hasattr(event, 'x_root') and event.x_root or 0
            self.y_root = hasattr(event, 'y_root') and event.y_root or 0

            if self.keysym and c.k:
                # Translate keysyms for ascii characters to the character itself.
                self.keysym = c.k.guiBindNamesInverseDict.get(self.keysym, self.keysym)

            self.widget = self.w

        def __repr__(self):
            return 'swingGui.leoKeyEvent: char: %s, keysym: %s' % (
                repr(self.char),
                repr(self.keysym),
            )

    #@-others


#@< leoSwingUtils
#@> class GCEveryOneMinute
class GCEveryOneMinute(java.lang.Thread):
    def __init__(self):
        java.lang.Thread.__init__(self)

    def run(self):
        while 1:
            java.lang.System.gc()
            self.sleep(60000)


#@-others
#@-leo
