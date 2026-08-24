#@+leo-ver=cub-1-thin
#@0 [ekr.20140907085654.18699] @f ../plugins/qt_gui.py
"""This file contains the gui wrapper for Qt: g.app.gui."""

#@+<< qt_gui imports  >>
#@-<< qt_gui imports  >>
#@+<< qt_gui annotations >>
#@> << qt_gui annotations >>
if TYPE_CHECKING:  # pragma: no cover
    from typing import TypeAlias  # Requires Python 3.12+
    from leo.core.leoCommands import Commands as Cmdr
    from leo.core.leoGui import LeoKeyEvent
    from leo.core.leoNodes import Position

    QDialog = QtWidgets.QDialog
    QEvent: TypeAlias = QtCore.QEvent
    QFont = QtGui.QFont
    QFrame = QtWidgets.QFrame
    QGridLayout = QtWidgets.QGridLayout
    QHBoxLayout = QtWidgets.QHBoxLayout
    QIcon = QtGui.QIcon
    QLabel = QtWidgets.QLabel
    QLayout = QtWidgets.QLayout
    QMainWindow = QtWidgets.QMainWindow
    QObject = QtCore.QObject
    QPixmap = QtGui.QPixmap
    QPoint = QtCore.QPoint
    QPushButton = QtWidgets.QPushButton
    QSplitter = QtWidgets.QSplitter
    QTabWidget = QtWidgets.QTabWidget
    QVBoxLayout = QtWidgets.QVBoxLayout


#@-<< qt_gui annotations >>
#@+others
#@ init (qt_gui.py)
def init() -> bool:
    if g.unitTesting:  # Not Ok for unit testing!
        return False
    if not QtCore:
        return False
    if g.app.gui:
        return g.app.gui.guiName() == 'qt'
    g.app.gui = LeoQtGui()
    g.app.gui.finishCreate()
    g.plugin_signon(__name__)
    return True


#@ class LeoQtGui(leoGui.LeoGui)
class LeoQtGui(leoGui.LeoGui):
    """A class implementing Leo's Qt gui."""

    #@+others
    #@>  LeoQtGui.__init__ (sets qtApp)
    def __init__(self) -> None:
        """Ctor for LeoQtGui class."""
        super().__init__('qt')  # Initialize the base class.
        self.active = True
        self.consoleOnly = False  # Console is separate from the log.
        self.iconimages: dict[str, QIcon] = {}  # Keys are paths, values are Icons.
        self.globalFindDialog: QDialog | None = None
        self.idleTimeClass = qt_idle_time.IdleTime
        self.mGuiName = 'qt'
        self.show_tips_flag = False  # #2390: Can't be inited in reload_settings.
        self.styleSheetManagerClass = StyleSheetManager
        if g.isMac and g.app.config.getBool('qt-mac-dont-swap-ctrl-and-meta', default=False):
            attr = getattr(Qt.ApplicationAttribute, 'AA_MacDontSwapCtrlAndMeta', None)
            if attr is not None:
                QtWidgets.QApplication.setAttribute(attr, True)
        # Be aware of the systems native colors, fonts, etc.
        QtWidgets.QApplication.setDesktopSettingsAware(True)
        # Create objects...
        self.qtApp = QtWidgets.QApplication(sys.argv)
        self.reloadSettings()
        self.appIcon = self.getIconImage('leoapp32.png')

        # Define various classes key stokes.
        #@+<< define FKeys >>
        #@> << define FKeys >>
        self.FKeys = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12']
        # These do not generate keystrokes on MacOs.
        #@-<< define FKeys >>
        #@+<< define ignoreChars >>
        #@ << define ignoreChars >>
        # Always ignore these characters
        self.ignoreChars = [
            # These are in ks.special characters.
            # They should *not* be ignored.
            # 'Left', 'Right', 'Up', 'Down',
            # 'Next', 'Prior',
            # 'Home', 'End',
            # 'Delete', 'Escape',
            # 'BackSpace', 'Linefeed', 'Return', 'Tab',
            # F-Keys are also ok.
            # 'F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12',
            'KP_0',
            'KP_1',
            'KP_2',
            'KP_3',
            'KP_4',
            'KP_5',
            'KP_6',
            'KP_7',
            'KP_8',
            'KP_9',
            'KP_Multiply, KP_Separator,KP_Space, KP_Subtract, KP_Tab',
            'KP_F1',
            'KP_F2',
            'KP_F3',
            'KP_F4',
            # Keypad chars should be have been converted to other keys.
            # Users should just bind to the corresponding normal keys.
            'KP_Add',
            'KP_Decimal',
            'KP_Divide',
            'KP_Enter',
            'KP_Equal',
            'CapsLock',
            'Caps_Lock',
            'NumLock',
            'Num_Lock',
            'ScrollLock',
            'Alt_L',
            'Alt_R',
            'Control_L',
            'Control_R',
            'Meta_L',
            'Meta_R',
            'Shift_L',
            'Shift_R',
            'Win_L',
            'Win_R',  # Clearly, these should never be generated.
            # These are real keys, but they don't mean anything.
            'Break',
            'Pause',
            'Sys_Req',
            'Begin',
            'Clear',  # Don't know what these are.
        ]
        #@-<< define ignoreChars >>
        #@+<< define specialChars >>
        #@ << define specialChars >>
        # Keys whose names must never be inserted into text.
        self.specialChars = [
            # These are *not* special keys.
            # 'BackSpace', 'Linefeed', 'Return', 'Tab',
            'Left',
            'Right',
            'Up',
            'Down',  # Arrow keys
            'Next',
            'Prior',  # Page up/down keys.
            'Home',
            'End',  # Home end keys.
            'Delete',
            'Escape',  # Others.
            'Enter',
            'Insert',
            'Ins',  # These should only work if bound.
            'Menu',  # #901.
            'PgUp',
            'PgDn',  # #868.
        ]
        #@-<< define specialChars >>
        # Put up the splash screen()
        if (
            g.app.use_splash_screen
            and not g.app.batchMode
            and not g.app.silentMode
            and not g.unitTesting
        ):
            self.splashScreen = self.createSplashScreen()
        # qtFrame.finishCreate does all the other work.
        self.frameFactory = qt_frame.TabbedFrameFactory()

    def reloadSettings(self) -> None:
        pass  # Note: self.c does not exist.

    #@<  LeoQtGui.destroySelf (calls qtApp.quit)
    def destroySelf(self) -> None:
        """Stop executing the qt gui after printing any stats."""
        if g.app.statsDict:
            g.printStats()
        QtCore.pyqtRemoveInputHook()
        if 'shutdown' in g.app.debug:
            g.pr('LeoQtGui.destroySelf: calling qtApp.Quit')
        self.qtApp.quit()

    #@ LeoQtGui.getFontFromParams
    size_warnings: list[str] = []
    font_ids: list[int] = []  # id's of traced fonts.

    def getFontFromParams(
        self,
        family: str,
        size: str,
        slant: str,
        weight: str,
        defaultSize: int = 12,
        tag='',
    ) -> QFont | None:
        """Required to handle syntax coloring."""
        if isinstance(size, str):
            if size.endswith('pt'):
                size = size[:-2].strip()
            elif size.endswith('px'):
                if size not in self.size_warnings:
                    self.size_warnings.append(size)
                    g.es(f"px ignored in font setting: {size}")
                size = size[:-2].strip()
        try:
            i_size = int(size)
        except Exception:
            i_size = 0
        if i_size < 1:
            i_size = defaultSize
        d = {
            'black': Weight.Black,
            'bold': Weight.Bold,
            'demibold': Weight.DemiBold,
            'light': Weight.Light,
            'normal': Weight.Normal,
        }
        weight_val = d.get(weight.lower(), Weight.Normal)
        italic = slant == 'italic'
        if not family:
            family = 'DejaVu Sans Mono'
        try:
            font = QtGui.QFont(family, i_size, weight_val, italic)
            if sys.platform.startswith('linux'):
                try:
                    font.setHintingPreference(font.PreferFullHinting)
                except AttributeError:
                    pass
            return font
        except Exception:
            g.es_print("exception setting font", g.callers(4))
            g.es_print(f"family: {family}\n  size: {i_size}\n slant: {slant}\nweight: {weight}")
            # g.es_exception() # Confusing for most users.
            return None

    #@ LeoQtGui.getFullVersion
    def getFullVersion(self, c: Cmdr | None = None) -> str:
        """Return the PyQt version (for signon)"""
        try:
            qtLevel = f"version {QtCore.qVersion()}"
        except Exception:
            # g.es_exception()
            qtLevel = '<qtLevel>'
        return f"PyQt {qtLevel}"

    #@ LeoQtGui.makeScriptButton
    def makeScriptButton(
        self,
        c: Cmdr,
        args: Any | None = None,
        p: Position | None = None,  # A node containing the script.
        script: str | None = None,  # The script itself.
        buttonText: str | None = None,
        balloonText: str = 'Script Button',
        shortcut: str | None = None,
        bg: str = 'LightSteelBlue1',
        define_g: bool = True,
        define_name: str = '__main__',
        silent: bool = False,  # Passed on to c.executeScript.
    ) -> None:
        """
        Create a script button for the script in node p.
        The button's text defaults to p.headString.
        """
        k = c.k
        if p and not buttonText:
            buttonText = p.h.strip()
        if not buttonText:
            buttonText = 'Unnamed Script Button'
        # create the button.
        iconBar = c.frame.getIconBarObject()
        b = iconBar.add(text=buttonText)

        #@+<< define the callbacks for b >>
        #@> << define the callbacks for b >>
        def deleteButtonCallback(event: LeoKeyEvent, b: QPushButton = b, c: Cmdr = c) -> None:
            if b:
                b.pack_forget()
            c.bodyWantsFocus()

        def executeScriptCallback(
            event: LeoKeyEvent,
            b: QPushButton = b,
            c: Cmdr = c,
            buttonText: str = buttonText,
            p: Position | None = p and p.copy(),
            script: str | None = script,
        ) -> None:
            if c.disableCommandsMessage:
                g.blue('', c.disableCommandsMessage)
            else:
                g.app.scriptDict = {'script_gnx': p.gnx}
                c.executeScript(
                    args=args,
                    p=p,
                    script=script,
                    define_g=define_g,
                    define_name=define_name,
                    silent=silent,
                )
                # Remove the button if the script asks to be removed.
                if g.app.scriptDict.get('removeMe'):
                    g.es('removing', f"'{buttonText}'", 'button at its request')
                    b.pack_forget()
            # Do not assume the script will want to remain in this commander.

        #@-<< define the callbacks for b >>
        b.configure(command=executeScriptCallback)
        if shortcut:
            if k.bindKey('button', shortcut, executeScriptCallback, buttonText):
                g.blue(f"bound @button {buttonText} to: {shortcut}")

        # #1121: create press-buttonText-button command
        buttonCommandName = f"press-{buttonText.replace(' ', '-').strip('-')}-button"
        # This will use any shortcut defined in an @shortcuts node.
        k.registerCommand(buttonCommandName, executeScriptCallback, pane='button')

    #@< LeoQtGui.onContextMenu
    def onContextMenu(self, c: Cmdr, w: QTextMixin, point: QPoint) -> None:
        """LeoQtGui: Common context menu handling."""
        # #1286.
        handlers = g.tree_popup_handlers
        if not handlers:
            return  # #4164: The "No popup handlers" message is annoying.
        menu = QtWidgets.QMenu(c.frame.top)  # #1995.
        menuPos = w.mapToGlobal(point)
        p = c.p.copy()
        done: set[Callable] = set()
        for handler in handlers:
            # every handler has to add it's QActions by itself
            if handler in done:
                # do not run the same handler twice
                continue
            try:
                handler(c, p, menu)
                done.add(handler)
            except Exception:
                g.es_print('Exception executing right-click handler')
                g.es_exception()
        menu.popup(menuPos)
        self._contextmenu = menu

    #@ LeoQtGui.put_help
    def put_help(self, c: Cmdr, s: str, short_title: str = '') -> Any:
        """Put the help command."""
        s = textwrap.dedent(s.rstrip())
        if s.startswith('<') and not s.startswith('<<'):
            pass  # how to do selective replace??
        pc = g.app.pluginsController
        table = (
            'viewrendered3.py',
            'viewrendered.py',
        )
        for name in table:
            if pc.isLoaded(name):
                vr = pc.loadOnePlugin(name)
                break
        else:
            vr = pc.loadOnePlugin('viewrendered.py')
        if vr:
            kw = {
                'c': c,
                'flags': 'rst',
                'kind': 'rst',
                'label': '',
                'msg': s,
                'name': 'Apropos',
                'short_title': short_title,
                'title': '',
            }
            vr.show_scrolled_message(tag='Apropos', kw=kw)
            c.bodyWantsFocus()
            if g.unitTesting:
                vr.close_rendering_pane(event={'c': c})
        elif g.unitTesting:
            pass
        else:
            g.es(s)
        return vr  # For unit tests

    #@ LeoQtGui.runAtIdle
    def runAtIdle(self, aFunc: Callable) -> None:
        """This can not be called in some contexts."""
        QtCore.QTimer.singleShot(0, aFunc)

    #@ LeoQtGui.runMainLoop
    def runMainLoop(self) -> None:
        """Start the Qt main loop."""
        try:  # #2127: A crash here hard-crashes Leo: There is no main loop!
            g.app.gui.dismiss_splash_screen()
            c = g.app.log and g.app.log.c
            if c and c.config.getBool('show-tips', default=False):
                g.app.gui.show_tips(c)
        except Exception:
            g.es_exception()
        if self.script:
            if log := g.app.log:
                g.pr('Start of batch script...\n')
                log.c.executeScript(script=self.script)
                g.pr('End of batch script')
            else:
                g.pr('no log, no commander for executeScript in LeoQtGui.runMainLoop')
        else:
            # This can be alarming when using Python's -i option.
            sys.exit(self.qtApp.exec())

    #@ LeoQtGui.show_tips & helpers
    @g.command('show-tips')
    def show_next_tip(self, event: LeoKeyEvent | None = None) -> None:
        if c := g.app.log and g.app.log.c:
            g.app.gui.show_tips(c)

    #@+<< define DialogWithCheckBox >>
    #@> << define DialogWithCheckBox >>
    class DialogWithCheckBox(QtWidgets.QMessageBox):
        def __init__(self, controller: LeoQtGui, checked: bool, tip: UserTip) -> None:
            super().__init__()
            c = g.app.log.c
            self.leo_checked = True
            self.setObjectName('TipMessageBox')
            self.setIcon(Icon.Information)  # #2127.
            self.setWindowTitle('Leo Tips')
            self.setText(repr(tip))
            self.next_tip_button = self.addButton('Show Next Tip', ButtonRole.ActionRole)
            self.addButton('Ok', ButtonRole.YesRole)
            c.styleSheetManager.set_style_sheets(w=self)
            # Workaround #693.
            layout = self.layout()
            checkbox = QtWidgets.QCheckBox()
            checkbox.setObjectName('TipCheckbox')
            checkbox.setText('Show Tip On Startup')
            # #2383: State is a tri-state, so use the official constants.
            checkbox.setCheckState(Checked if checked else Unchecked)  # #2127.
            checkbox.stateChanged.connect(controller.onClick)
            # A mypy bug? layout is a QGridLayout. mypy thinks it's a plain QLayout.
            layout.addWidget(checkbox, 4, 0, -1, -1)  # type:ignore
            if 0:  # Does not work well.
                sizePolicy = QtWidgets.QSizePolicy
                vSpacer = QtWidgets.QSpacerItem(200, 200, sizePolicy.Minimum, sizePolicy.Expanding)
                layout.addItem(vSpacer)

    #@-<< define DialogWithCheckBox >>

    def show_tips(self, c: Cmdr) -> None:
        if g.unitTesting:
            return
        from leo.core import leoTips

        tm = leoTips.TipManager()
        self.show_tips_flag = c.config.getBool('show-tips', default=False)  # 2390.
        while True:  # QMessageBox is always a modal dialog.
            tip = tm.get_next_tip()
            m = self.DialogWithCheckBox(controller=self, checked=self.show_tips_flag, tip=tip)
            try:
                c.in_qt_dialog = True
                m.exec()
            finally:
                c.in_qt_dialog = False
            b = m.clickedButton()
            if b != m.next_tip_button:
                break

    #@< LeoQtGui: Clipboard
    #@> LeoQtGui.replaceClipboardWith
    def replaceClipboardWith(self, s: str) -> None:
        """Replace the clipboard with the string s."""
        if cb := self.qtApp.clipboard():
            # cb.clear()  # unnecessary, breaks on some Qt versions
            s = g.toUnicode(s)
            QtWidgets.QApplication.processEvents()
            # Fix #241: QMimeData object error
            cb.setText(s)
            QtWidgets.QApplication.processEvents()
        else:
            g.trace('no clipboard!')

    #@ LeoQtGui.getTextFromClipboard
    def getTextFromClipboard(self) -> str:
        """Get a unicode string from the clipboard."""
        if cb := self.qtApp.clipboard():
            QtWidgets.QApplication.processEvents()
            return cb.text()
        g.trace('no clipboard!')
        return ''

    #@ LeoQtGui.setClipboardSelection
    def setClipboardSelection(self, s: str) -> None:
        """
        Set the clipboard selection to s.
        There are problems with PyQt5.
        """
        # Alas, returning s reopens #218.
        return

    #@< LeoQtGui: Dialogs & panels
    #@> LeoQtGui._save/_restore_focus
    def _save_focus(self, c):
        """
        Save the data needed to restore focus to the body.

        We have to guess: the user may have executed the save commands from the
        minibuffer. There is no way to know what the "original" focus was!
        """
        c.p.saveCursorAndScroll()

    def _restore_focus(self, c):
        """Restore focus to the body pane."""
        # Fix #3601 by brute force.
        c.bringToFront()
        c.bodyWantsFocusNow()
        c.p.restoreCursorAndScroll()

    #@ LeoQtGui.alert
    def alert(self, c: Cmdr, message: str) -> None:
        if g.unitTesting:
            return
        dialog = QtWidgets.QMessageBox(None)
        dialog.setWindowTitle('Alert')
        dialog.setText(message)
        dialog.setIcon(Icon.Warning)
        dialog.addButton('Ok', ButtonRole.YesRole)
        try:
            c.in_qt_dialog = True
            dialog.raise_()
            dialog.exec()
        finally:
            c.in_qt_dialog = False

    #@ LeoQtGui.makeFilter
    def makeFilter(self, filetypes: list[tuple[str, str]]) -> str:
        """Return the Qt-style dialog filter from filetypes list."""
        # Careful: the second %s is *not* replaced.
        filters = ['%s (%s)' % (z) for z in filetypes]
        return ';;'.join(filters)

    #@ LeoQtGui.openFindDialog & helper
    def openFindDialog(self, c: Cmdr) -> None:
        if g.unitTesting:
            return
        dialog = self.globalFindDialog
        if not dialog:
            dialog = self.createFindDialog(c)
            self.globalFindDialog = dialog
            # Fix #516: Do the following only once...
            if c:
                # dialog.setStyleSheet(c.active_stylesheet)
                # Set the commander's FindTabManager.
                assert g.app.globalFindTabManager
                cast(Any, c).ftm = g.app.globalFindTabManager
                fn = c.shortFileName() or 'Untitled'
            else:
                fn = 'Untitled'
            dialog.setWindowTitle(f"Find in {fn}")
        if c:
            c.inCommand = False
        if dialog.isVisible():
            # The order is important, and tricky.
            dialog.focusWidget()
            dialog.show()
            dialog.raise_()
            dialog.activateWindow()
        else:
            dialog.show()
            dialog.exec()

    #@> LeoQtGui.createFindDialog
    def createFindDialog(self, c: Cmdr) -> QDialog | None:
        """Create and init a non-modal Find dialog."""
        if not c:
            return None  # #4753
        g.app.globalFindTabManager = c.findCommands.ftm
        top = c.frame.top
        w = top.findTab
        dialog = QtWidgets.QDialog()

        # Fix #516: Hide the dialog. Never delete it.

        def closeEvent(event: QEvent) -> None:
            event.ignore()
            dialog.hide()

        dialog.closeEvent = closeEvent  # type:ignore # cannot assign to method.
        layout = QtWidgets.QVBoxLayout(dialog)
        layout.addWidget(w)
        self.attachLeoIcon(dialog)
        dialog.setLayout(layout)
        if c:
            # c.styleSheetManager.set_style_sheets(w=dialog)
            g.app.gui.setFilter(c, dialog, dialog, 'find-dialog')
            # This makes most standard bindings available.
        dialog.setModal(False)
        return dialog

    #@< LeoQtGui.panels
    def createComparePanel(self, c: Cmdr) -> None:
        """Create a qt color picker panel."""
        # This window is optional.

    def createFindTab(self, c: Cmdr, parentFrame: QWidget) -> None:
        """Create a qt find tab in the indicated frame."""
        # Now done in dw.createFindTab.

    def createLeoFrame(self, c: Cmdr, title: str) -> qt_frame.LeoQtFrame:
        """Create a new Leo frame."""
        return qt_frame.LeoQtFrame(c, title, gui=self)

    def createSpellTab(
        self, c: Cmdr, spellHandler: Callable, tabName: str
    ) -> qt_frame.LeoQtSpellTab | None:
        if g.unitTesting:
            return None
        return qt_frame.LeoQtSpellTab(c, spellHandler, tabName)

    #@ LeoQtGui.runAboutLeoDialog
    def runAboutLeoDialog(
        self,
        c: Cmdr,
        version: str,
        theCopyright: str,
        url: str,
        email: str,
    ) -> None:
        """Create and run a qt About Leo dialog."""
        if g.unitTesting:
            return

        # Create the dialog.
        top_frame: QWidget | None = c.frame.top if c else None
        dialog = QtWidgets.QMessageBox(top_frame)
        ssm = g.app.gui.styleSheetManagerClass(c)
        w = ssm.get_master_widget()
        if sheet := w.styleSheet():
            dialog.setStyleSheet(sheet)
        dialog.setText(f"{version}\n{theCopyright}\n{url}\n{email}")
        dialog.setIcon(Icon.Information)
        yes = dialog.addButton('Ok', ButtonRole.YesRole)
        dialog.setDefaultButton(yes)

        # Run the dialog, saving and restoring focus.
        try:
            self._save_focus(c)
            c.in_qt_dialog = True
            dialog.raise_()
            dialog.exec()
        finally:
            c.in_qt_dialog = False
            self._restore_focus(c)

    #@ LeoQtGui.runAskDateTimeDialog
    def runAskDateTimeDialog(
        self,
        c: Cmdr,
        title: str,
        message: str = 'Select Date/Time',
        init: dt.datetime | None = None,
        step_min: dict | None = None,
    ) -> dt.datetime | None:
        """Create and run a qt date/time selection dialog.

        init - a datetime, default now
        step_min - a dict, keys are QtWidgets.QDateTimeEdit Sections, like
          QtWidgets.QDateTimeEdit.MinuteSection, and values are integers,
          the minimum amount that section of the date/time changes
          when you roll the mouse wheel.

        E.g. (5 minute increments in minute field):

            g.app.gui.runAskDateTimeDialog(c, 'When?',
                message="When is it?",
                step_min={QtWidgets.QDateTimeEdit.MinuteSection: 5})

        """

        #@+<< define date/time classes >>
        #@> << define date/time classes >>
        class DateTimeEditStepped(QtWidgets.QDateTimeEdit):
            """
            QDateTimeEdit which allows you to set minimum steps on fields, e.g.
              DateTimeEditStepped(parent, {QtWidgets.QDateTimeEdit.MinuteSection: 5})
            for a minimum 5 minute increment on the minute field.
            """

            def __init__(
                self,
                parent: QWidget | None = None,
                init: dt.datetime | None = None,
                step_min: dict | None = None,
            ) -> None:
                if step_min is None:
                    step_min = {}
                self.step_min = step_min
                if init:
                    super().__init__(init, parent)
                else:
                    super().__init__(parent)

            def stepBy(self, steps: int) -> None:
                cs = self.currentSection()
                if cs in self.step_min and abs(steps) < self.step_min[cs]:
                    steps = self.step_min[cs] if steps > 0 else -self.step_min[cs]
                QtWidgets.QDateTimeEdit.stepBy(self, steps)

        class Calendar(QtWidgets.QDialog):
            def __init__(
                self,
                parent: QWidget | None = None,
                message: str = 'Select Date/Time',
                init: dt.datetime | None = None,
                step_min: dict | None = None,
            ) -> None:
                if step_min is None:
                    step_min = {}
                super().__init__(parent)
                layout = QtWidgets.QVBoxLayout()
                self.setLayout(layout)
                layout.addWidget(QtWidgets.QLabel(message))
                self.dt = DateTimeEditStepped(init=init, step_min=step_min)
                self.dt.setCalendarPopup(True)
                layout.addWidget(self.dt)
                buttonBox = QtWidgets.QDialogButtonBox(StandardButton.Ok | StandardButton.Cancel)
                layout.addWidget(buttonBox)
                buttonBox.accepted.connect(self.accept)
                buttonBox.rejected.connect(self.reject)

        #@-<< define date/time classes >>
        if g.unitTesting:
            return None
        if step_min is None:
            step_min = {}
        if not init:
            init = dt.datetime.now(tz=dt.timezone.utc)
        top_frame: QWidget | None = c.frame.top if c else None
        dialog = Calendar(top_frame, message=message, init=init, step_min=step_min)
        if c:
            ssm = g.app.gui.styleSheetManagerClass(c)
            w = ssm.get_master_widget()
            if sheet := w.styleSheet():
                dialog.setStyleSheet(sheet)
            dialog.setStyleSheet(c.active_stylesheet)
            dialog.setWindowTitle(title)
            try:
                c.in_qt_dialog = True
                dialog.raise_()
                val = dialog.exec()
            finally:
                c.in_qt_dialog = False
        else:
            dialog.setWindowTitle(title)
            dialog.raise_()
            val = dialog.exec()
        if val == DialogCode.Accepted:
            return dialog.dt.dateTime().toPyDateTime()
        return None

    #@< LeoQtGui.runAskOkCancelNumberDialog (not used)
    def runAskOkCancelNumberDialog(
        self,
        c: Cmdr,
        title: str,
        message: str,
        cancelButtonText: str | None = None,
        okButtonText: str | None = None,
    ) -> int | None:
        """Create and run askOkCancelNumber dialog ."""
        if g.unitTesting:
            return None
        # n,ok = QtWidgets.QInputDialog.getDouble(None,title,message)
        dialog = QtWidgets.QInputDialog()
        ssm = g.app.gui.styleSheetManagerClass(c)
        w = ssm.get_master_widget()
        if sheet := w.styleSheet():
            dialog.setStyleSheet(sheet)
        dialog.setWindowTitle(title)
        dialog.setLabelText(message)
        if cancelButtonText:
            dialog.setCancelButtonText(cancelButtonText)
        if okButtonText:
            dialog.setOkButtonText(okButtonText)
        self.attachLeoIcon(dialog)
        dialog.raise_()
        ok = dialog.exec()
        if not ok:
            return None
        n = dialog.textValue()
        int_n: int | None
        try:
            int_n = int(n)
        except ValueError:
            int_n = None
        return int_n

    #@ LeoQtGui.runAskOkCancelStringDialog
    def runAskOkCancelStringDialog(
        self,
        c: Cmdr,
        title: str,
        message: str,
        cancelButtonText: str | None = None,
        okButtonText: str | None = None,
        default: str = "",
        wide: bool = False,
    ) -> str | None:
        """Create and run askOkCancelString dialog.

        wide - edit a long string
        """
        if g.unitTesting:
            return None
        dialog = QtWidgets.QInputDialog()
        ssm = g.app.gui.styleSheetManagerClass(c)
        w = ssm.get_master_widget()
        if sheet := w.styleSheet():
            dialog.setStyleSheet(sheet)
        dialog.setWindowTitle(title)
        dialog.setLabelText(message)
        dialog.setTextValue(default)
        if wide and (windows := g.windows()):
            dialog.resize(int(windows[0].get_window_info()[0] * 0.9), 100)
        if cancelButtonText:
            dialog.setCancelButtonText(cancelButtonText)
        if okButtonText:
            dialog.setOkButtonText(okButtonText)
        self.attachLeoIcon(dialog)
        dialog.raise_()
        ok = dialog.exec()
        return str(dialog.textValue()) if ok else None

    #@ LeoQtGui.runAskOkDialog
    def runAskOkDialog(
        self, c: Cmdr, title: str, message: str | None = None, text: str = "Ok"
    ) -> None:
        """Create and run a qt askOK dialog ."""
        if g.unitTesting:
            return

        # Create the dialog.
        top_frame: QWidget | None = c.frame.top if c else None
        dialog = QtWidgets.QMessageBox(top_frame)
        dialog.setWindowTitle(title)
        if message:
            dialog.setText(message)
        dialog.setIcon(Information.Information)
        yes = dialog.addButton(text, ButtonRole.YesRole)
        dialog.setDefaultButton(yes)  # 2023/10/10.

        # Run the dialog.
        try:
            self._save_focus(c)
            c.in_qt_dialog = True
            dialog.raise_()
            dialog.exec()
        finally:
            c.in_qt_dialog = False
            self._restore_focus(c)

    #@ LeoQtGui.runAskYesNoCancelDialog
    def runAskYesNoCancelDialog(
        self,
        c: Cmdr,
        title: str,
        message: str | None = None,
        yesMessage: str = "&Yes",
        noMessage: str = "&No",
        yesToAllMessage: str | None = None,
        defaultButton: str = "Yes",
        cancelMessage: str | None = None,
    ) -> str:
        """
        Create and run an askYesNo dialog.

        Return one of ('yes', 'no', 'cancel', 'yes-to-all').

        """
        if g.unitTesting:
            return 'cancel'

        # Create the dialog.
        top_frame: QWidget | None = c.frame.top if c else None
        dialog = QtWidgets.QMessageBox(top_frame)
        if message:
            dialog.setText(message)

        dialog.setIcon(Information.Warning)
        dialog.setWindowTitle(title)

        yes = dialog.addButton(yesMessage, ButtonRole.YesRole)
        yes.setObjectName('yes')

        no = dialog.addButton(noMessage, ButtonRole.NoRole)
        no.setObjectName('no')

        cancel = dialog.addButton(cancelMessage or 'Cancel', ButtonRole.RejectRole)
        cancel.setObjectName('cancel')

        if yesToAllMessage:
            yes_to_all = dialog.addButton(yesToAllMessage, ButtonRole.YesRole)
            yes_to_all.setObjectName('yes-to-all')

        dialog.setDefaultButton(
            yes if defaultButton == 'Yes' else no if defaultButton == 'No' else cancel
        )

        # Run the dialog, saving and restoring focus.
        try:
            self._save_focus(c)
            c.in_qt_dialog = True
            dialog.raise_()  # #2246.
            dialog.exec()
        finally:
            c.in_qt_dialog = False
            self._restore_focus(c)

        # #4012: use clickedButton() to determine which button was clicked.
        button = dialog.clickedButton()
        return button.objectName() if button else 'yes'

    #@ LeoQtGui.runAskYesNoDialog
    def runAskYesNoDialog(
        self,
        c: Cmdr,
        title: str,
        message: str | None = None,
        yes_all: bool = False,
        no_all: bool = False,
    ) -> str:
        """
        Create and run an askYesNo dialog.
        Return one of ('yes','yes-all','no','no-all')

        :Parameters:
        - `c`: commander
        - `title`: dialog title
        - `message`: dialog message
        - `yes_all`: bool - show YesToAll button
        - `no_all`: bool - show NoToAll button
        """
        if g.unitTesting:
            return 'no'

        # Create the dialog.
        top_frame: QWidget | None = c.frame.top if c else None
        dialog = QtWidgets.QMessageBox(top_frame)

        # #4012: set the button's name to the desired return value!
        cancel = dialog.addButton('Cancel', ButtonRole.RejectRole)
        cancel.setObjectName('cancel')

        no = dialog.addButton('No', ButtonRole.NoRole)
        no.setObjectName('no')

        yes = dialog.addButton('Yes', ButtonRole.YesRole)
        yes.setObjectName('yes')

        if no_all:
            no_all_button = dialog.addButton('No To All', ButtonRole.NoRole)
            no_all_button.setObjectName('no-all')

        if yes_all:
            yes_all_button = dialog.addButton('Yes To All', ButtonRole.YesRole)
            yes_all_button.setObjectName('yes-all')

        dialog.setWindowTitle(title)
        if message:
            dialog.setText(message)
        dialog.setIcon(Information.Warning)
        dialog.setDefaultButton(yes)

        if c:
            # Run the dialog, saving and restoring focus.
            try:
                self._save_focus(c)
                c.in_qt_dialog = True
                dialog.raise_()
                dialog.exec()
            finally:
                c.in_qt_dialog = False
                self._restore_focus(c)
        else:
            # There is no way to save/restore focus.
            dialog.raise_()
            dialog.exec()

        # #4012: use clickedButton() to determine which button was clicked.
        button = dialog.clickedButton()
        return button.objectName() or 'cancel'

    #@ LeoQtGui.runOpenDirectoryDialog
    def runOpenDirectoryDialog(self, title: str, startdir: str) -> str | None:
        """Create and run an Qt open directory dialog ."""
        if g.unitTesting:
            return None
        dialog = QtWidgets.QFileDialog()
        self.attachLeoIcon(dialog)
        return dialog.getExistingDirectory(None, title, startdir)

    #@ LeoQtGui.runOpenFileDialog
    def runOpenFileDialog(
        self,
        c: Cmdr,
        title: str,
        *,
        filetypes: list[tuple[str, str]],
        defaultextension: str = '',  # Not used
        startpath: str | None = None,
    ) -> str:
        """
        Create and run an Qt open file dialog.
        """
        if g.unitTesting:
            return ''

        # 2018/03/14: Bug fixes:
        # - Use init_dialog_folder only if a path is not given
        # - *Never* Use os.curdir by default!
        if not startpath:
            # Returns c.last_dir or os.curdir
            startpath = g.init_dialog_folder(c, c.p, use_at_path=True)
        filter_ = self.makeFilter(filetypes)
        dialog = QtWidgets.QFileDialog()
        self.attachLeoIcon(dialog)
        dialog_val: tuple[str, Any]
        val: str
        if c:
            try:
                c.in_qt_dialog = True
                dialog_val = dialog.getOpenFileName(
                    parent=None, caption=title, directory=startpath, filter=filter_
                )
            finally:
                c.in_qt_dialog = False
        else:
            dialog_val = dialog.getOpenFileName(
                parent=None, caption=title, directory=startpath, filter=filter_
            )
        # This is a *PyQt* change, not a Qt change.
        val, junk_selected_filter = dialog_val
        s = g.os_path_normslashes(val)
        if c and s:
            c.last_dir = g.os_path_dirname(s)
        return s

    #@ LeoQtGui.runOpenFilesDialog
    def runOpenFilesDialog(
        self,
        c: Cmdr,
        title: str,
        *,
        filetypes: list[tuple[str, str]],
        defaultextension: str = '',  # Not used.
        startpath: str | None = None,
    ) -> list[str]:
        """
        Create and run an Qt open file dialog.
        """
        if g.unitTesting:
            return []

        # 2018/03/14: Bug fixes:
        # - Use init_dialog_folder only if a path is not given
        # - *Never* Use os.curdir by default!
        if not startpath:
            # Returns c.last_dir or os.curdir
            startpath = g.init_dialog_folder(c, c.p, use_at_path=True)
        filter_ = self.makeFilter(filetypes)
        dialog = QtWidgets.QFileDialog()
        self.attachLeoIcon(dialog)
        dialog_val: Any
        val = list[str]
        if c:
            try:
                c.in_qt_dialog = True
                dialog_val = dialog.getOpenFileNames(
                    parent=None, caption=title, directory=startpath, filter=filter_
                )
            finally:
                c.in_qt_dialog = False

        else:
            dialog_val = dialog.getOpenFileNames(
                parent=None, caption=title, directory=startpath, filter=filter_
            )
        # This is a *PyQt* change, not a Qt change.
        val, _ = dialog_val
        files = [g.os_path_normslashes(s) for s in val]
        if c and files:
            c.last_dir = g.os_path_dirname(files[-1])
        return files

    #@ LeoQtGui.runPropertiesDialog
    def runPropertiesDialog(
        self,
        title: str = 'Properties',
        data: Any | None = None,
        callback: Callable | None = None,
        buttons: list[str] | None = None,
    ) -> tuple[str, dict]:
        """Display a modal TkPropertiesDialog"""
        if not g.unitTesting:
            g.warning('Properties menu not supported for Qt gui')
        return 'Cancel', {}

    #@ LeoQtGui.runSaveFileDialog
    def runSaveFileDialog(
        self,
        c: Cmdr,
        title: str = 'Save',
        *,
        filetypes: list[tuple[str, str]] | None = None,
        defaultextension: str = '',  # Not used.
    ) -> str:
        """Create and run an Qt save file dialog ."""
        if g.unitTesting:
            return ''
        dialog = QtWidgets.QFileDialog()
        if c:
            # dialog.setStyleSheet(c.active_stylesheet)
            self.attachLeoIcon(dialog)
            try:
                self._save_focus(c)
                c.in_qt_dialog = True
                obj = dialog.getSaveFileName(
                    None,  # parent
                    title,
                    # os.curdir,
                    g.init_dialog_folder(c, c.p, use_at_path=True),
                    self.makeFilter(filetypes or []),
                )
            finally:
                c.in_qt_dialog = False
                self._restore_focus(c)
        else:
            self.attachLeoIcon(dialog)
            obj = dialog.getSaveFileName(
                None,  # parent
                title,
                # os.curdir,
                g.init_dialog_folder(None, None, use_at_path=True),
                self.makeFilter(filetypes or []),
            )
        # PyQt may return a tuple.
        s = obj[0] if isinstance(obj, (list, tuple)) else obj
        s = s or ''
        if c and s:
            c.last_dir = g.os_path_dirname(s)
        return s

    #@ LeoQtGui.runScrolledMessageDialog
    def runScrolledMessageDialog(
        self,
        short_title: str = '',
        title: str = 'Message',
        label: str = '',
        msg: str = '',
        c: Cmdr | None = None,
        **keys: Any,
    ) -> None:
        if g.unitTesting:
            return None

        def send() -> Any:
            return g.doHook(
                'scrolledMessage',
                short_title=short_title,
                title=title,
                label=label,
                msg=msg,
                c=c,
                **keys,
            )

        if not c or not c.exists:
            #@+<< no c error>>
            #@> << no c error>>
            g.es_print_error(
                '%s\n%s\n\t%s'
                % (
                    "The qt plugin requires calls to g.app.gui.scrolledMessageDialog to include 'c'",
                    "as a keyword argument",
                    g.callers(),
                )
            )
            #@-<< no c error>>
        else:
            if retval := send():
                return retval
            #@+<< load viewrendered plugin >>
            #@ << load viewrendered plugin >>
            pc = g.app.pluginsController
            # Load viewrendered (and call vr.onCreate) *only* if not already loaded.
            if not pc.isLoaded('viewrendered.py') and not pc.isLoaded('viewrendered3.py'):
                if vr := pc.loadOnePlugin('viewrendered.py'):
                    g.blue('viewrendered plugin loaded.')
                    vr.onCreate('tag', {'c': c})
            #@-<< load viewrendered plugin >>
            if retval := send():
                return retval
            #@+<< no dialog error >>
            #@ << no dialog error >>
            g.es_print_error(f'No handler for the "scrolledMessage" hook.\n\t{g.callers()}')
            #@-<< no dialog error >>
        #@+<< emergency fallback >>
        #@ << emergency fallback >>
        dialog = QtWidgets.QMessageBox(None)
        # That is, not a fixed size dialog.
        dialog.setWindowFlags(WindowType.Dialog)
        dialog.setWindowTitle(title)
        if msg:
            dialog.setText(msg)
        dialog.setIcon(Icon.Information)
        dialog.addButton('Ok', ButtonRole.YesRole)
        try:
            if c:
                c.in_qt_dialog = True
            dialog.exec()
        finally:
            if c:
                c.in_qt_dialog = False
        #@-<< emergency fallback >>

    #@<2 LeoQtGui: Event handlers
    #@> LeoQtGui.close_event
    def close_event(self, event: QEvent) -> None:
        # Save session data.
        g.app.saveSession()

        # Attempt to close all windows.
        for c in g.app.commanders():
            allow = c.exists and g.app.closeLeoWindow(c.frame)
            if not allow:
                event.ignore()
                return
        event.accept()

    #@ LeoQtGui.onDeactiveEvent
    # deactivated_name = ''

    deactivated_widget = None

    def onDeactivateEvent(self, event: QEvent, c: Cmdr, obj: object, tag: str) -> None:
        """
        Gracefully deactivate the Leo window.
        Called several times for each window activation.
        """
        w = self.get_focus()
        w_name = w and w.objectName()
        if 'focus' in g.app.debug:
            g.trace(repr(w_name))
        self.active = False  # Used only by c.idle_focus_helper.
        # Careful: never save headline widgets.
        if w_name == 'headline':
            self.deactivated_widget = c.frame.tree.treeWidget
        else:
            self.deactivated_widget = w if w_name else None
        # Causes problems elsewhere...
        # if c.exists and not self.deactivated_name:
        # self.deactivated_name = self.widget_name(self.get_focus())
        # self.active = False
        # c.k.keyboardQuit(setFocus=False)
        g.doHook('deactivate', c=c, p=c.p, v=c.p, event=event)

    #@ LeoQtGui.onActivateEvent
    # Called from eventFilter

    def onActivateEvent(self, event: QEvent, c: Cmdr, obj: object, tag: str) -> None:
        """
        Restore the focus when the Leo window is activated.
        Called several times for each window activation.
        """
        trace = 'focus' in g.app.debug
        w = self.get_focus() or self.deactivated_widget
        self.deactivated_widget = None
        w_name = w and w.objectName()
        # Fix #270: Vim keys don't always work after double Alt+Tab.
        # Fix #359: Leo hangs in LeoQtEventFilter.eventFilter
        # #1273: add test on c.vim_mode.
        if c.exists and c.vim_mode and c.vimCommands and not self.active and not g.app.killed:
            c.vimCommands.on_activate()
        self.active = True  # Used only by c.idle_focus_helper.
        if g.isMac:
            pass  # Fix #757: MacOS: replace-then-find does not work in headlines.
        else:
            # Leo 5.6: Recover from missing focus.
            # c.idle_focus_handler can't do this.
            if w and w_name in ('log-widget', 'richTextEdit', 'treeWidget'):
                # Restore focus **only** to body or tree
                if trace:
                    g.trace('==>', w_name)
                c.widgetWantsFocusNow(w)
            else:
                if trace:
                    g.trace(repr(w_name), '==> BODY')
                c.bodyWantsFocusNow()
        # Cause problems elsewhere.
        # if c.exists and self.deactivated_name:
        # self.active = True
        # w_name = self.deactivated_name
        # self.deactivated_name = None
        # if c.p.v:
        # c.p.v.restoreCursorAndScroll()
        # if w_name.startswith('tree') or w_name.startswith('head'):
        # c.treeWantsFocusNow()
        # else:
        # c.bodyWantsFocusNow()
        g.doHook('activate', c=c, p=c.p, v=c.p, event=event)

    #@ LeoQtGui.setFilter
    def setFilter(self, c: Cmdr, obj: object, w: QWidget, tag: str) -> None:
        """
        Create an event filter in obj.
        w is a wrapper object, not necessarily a QWidget.
        """
        # w's type is in (DynamicWindow,QMinibufferWrapper,LeoQtLog,LeoQtTree,
        # QTextEditWrapper,LeoQTextBrowser,LeoQuickSearchWidget,cleoQtUI)
        # g.trace(f"{id(w)} {self.widget_name(w):>22} {w.__class__.__name__}")
        assert isinstance(obj, QtWidgets.QWidget), obj
        theFilter = qt_events.LeoQtEventFilter(c, w=w, tag=tag)
        obj.installEventFilter(theFilter)
        w.ev_filter = theFilter  # Set the official ivar in w.

    #@< LeoQtGui: Focus
    #@> LeoQtGui.ensure_commander_visible
    def ensure_commander_visible(self, c: Cmdr) -> None:
        """
        Check to see if c.frame is in a tabbed ui, and if so, make sure
        the tab is visible
        """
        if 'focus' in g.app.debug:
            g.trace(c)
        if hasattr(g.app.gui, 'frameFactory'):
            factory = g.app.gui.frameFactory
            if factory and hasattr(factory, 'setTabForCommander'):
                factory.setTabForCommander(c)
                c.bodyWantsFocusNow()

    #@ LeoQtGui.get_focus
    def get_focus(
        self, c: Cmdr | None = None, raw: bool = False, at_idle: bool = False
    ) -> QWidget | None:
        """Returns the widget that has focus."""
        trace = 'focus' in g.app.debug and not at_idle
        w = QtWidgets.QApplication.focusWidget()
        if trace:
            name = w.objectName() if hasattr(w, 'objectName') else w.__class__.__name__
            g.trace('(LeoQtGui)', name)
        return w

    #@ LeoQtGui.set_focus
    def set_focus(self, c: Cmdr, w: QWidget) -> None:
        """Put the focus on the widget."""
        if not w:
            return
        if getattr(w, 'widget', None):
            if not isinstance(w, QtWidgets.QWidget):
                # w should be a wrapper.
                w = w.widget
        if 'focus' in g.app.debug:
            name = w.objectName() if hasattr(w, 'objectName') else w.__class__.__name__
            g.trace('(LeoQtGui)', name)
        w.setFocus()

    #@< LeoQtGui: Icons
    #@> LeoQtGui.attachLeoIcon
    def attachLeoIcon(self, window: QMainWindow | QDialog) -> None:
        """Attach a Leo icon to the window."""
        if self.appIcon:
            window.setWindowIcon(self.appIcon)

    #@ LeoQtGui.getIconImage
    def getIconImage(self, name: str) -> QIcon | None:
        """Load the icon and return it."""
        # Return the image from the cache if possible.
        if name in self.iconimages:
            image = self.iconimages.get(name)
            return image
        try:
            iconsDir = g.os_path_join(g.app.loadDir, "..", "Icons")
            homeIconsDir = g.os_path_join(g.app.homeLeoDir, "Icons")
            for theDir in (homeIconsDir, iconsDir):
                fullname = g.finalize_join(theDir, name)
                if g.os_path_exists(fullname):
                    if 0:  # Not needed: use QTreeWidget.setIconsize.
                        pixmap = QtGui.QPixmap()
                        pixmap.load(fullname)
                        image = QtGui.QIcon(pixmap)
                    else:
                        image = QtGui.QIcon(fullname)
                    self.iconimages[name] = image
                    return image
            # No image found.
            return None
        except Exception:
            g.es_print("exception loading:", fullname)
            g.es_exception()
            return None

    #@ LeoQtGui.getImageImage
    @functools.lru_cache(maxsize=128)
    def getImageImage(self, name: str) -> QPixmap | None:
        """Load the image in file named `name` and return it."""
        fullname = self.getImageFinder(name)
        try:
            pixmap = QtGui.QPixmap()
            pixmap.load(fullname)
            return pixmap
        except Exception:
            g.es("exception loading:", name)
            g.es_exception()
            return None

    #@ LeoQtGui.getImageFinder
    dump_given = False

    @functools.lru_cache(maxsize=128)
    def getImageFinder(self, name: str) -> str | None:
        """Theme aware image (icon) path searching."""
        trace = 'themes' in g.app.debug
        exists = g.os_path_exists
        getString = g.app.config.getString

        def dump(var: str, val: str) -> None:
            print(f"{var:20}: {val}")

        join = g.os_path_join

        # "Just works" for --theme and theme .leo files *provided* that
        # theme .leo files actually contain these settings!

        theme_name1 = getString('color-theme')
        theme_name2 = getString('theme-name')
        roots = [
            g.os_path_join(g.computeHomeDir(), '.leo'),
            g.computeLeoDir(),
        ]
        theme_subs = [
            "themes/{theme}/Icons",
            "themes/{theme}",
            "Icons/{theme}",
        ]
        # "." for icons referred to as Icons/blah/blah.png
        bare_subs = ["Icons", "."]
        paths = []
        for theme_name in (theme_name1, theme_name2):
            for root in roots:
                for sub in theme_subs:
                    paths.append(join(root, sub.format(theme=theme_name)))
        for root in roots:
            for sub in bare_subs:
                paths.append(join(root, sub))
        table = [z for z in paths if exists(z)]
        for base_dir in table:
            path = join(base_dir, name)
            if exists(path):
                if trace:
                    g.trace(f"Found {name} in {base_dir}")
                return path
            # if trace: g.trace(name, 'not in', base_dir)
        if trace:
            g.trace('not found:', name)
        return None

    #@ LeoQtGui.getTreeImage
    @functools.lru_cache(maxsize=128)
    def getTreeImage(self, c: Cmdr, path: str) -> tuple[QPixmap, int] | tuple[None, None]:
        image = QtGui.QPixmap(path)
        if image.height() > 0 and image.width() > 0:
            return image, image.height()
        return None, None

    #@< LeoQtGui: Splash Screen
    #@> LeoQtGui.createSplashScreen
    def createSplashScreen(self) -> QWidget | None:
        """Put up a splash screen with Leo's logo."""
        try:
            QApplication = QtWidgets.QApplication
            QPixmap = QtGui.QPixmap
            QSvgRenderer = QtSvg.QSvgRenderer
            QPainter = QtGui.QPainter
            QImage = QtGui.QImage
            QScreen = QtGui.QScreen
        except Exception:
            return None

        Format_RGB32 = 4  # a Qt enumeration value

        splash = None
        for fn in (
            'SplashScreen.svg',  # Leo's licensed .svg logo.
            'Leosplash.GIF',  # Leo's public domain bitmapped image.
        ):
            path = g.finalize_join(g.app.loadDir, '..', 'Icons', fn)
            if g.os_path_exists(path):
                if fn.endswith('svg'):
                    # Convert SVG to un-pixilated pixmap
                    renderer = QSvgRenderer(path)
                    size = renderer.defaultSize()
                    svg_height, svg_width = size.height(), size.width()

                    # Scale to fraction of screen height
                    screen = QApplication.primaryScreen()
                    assert screen is not None
                    geom = QScreen.availableGeometry(screen)
                    screen_height = geom.height()
                    target_height_px = screen_height // 4
                    scaleby = target_height_px / svg_height
                    target_width_px = int(svg_width * scaleby)

                    image = QImage(target_width_px, target_height_px, QImage.Format(Format_RGB32))
                    image.fill(0xFFFFFFFF)  # MUST fill background
                    painter = QPainter(image)
                    renderer.render(painter)
                    painter.end()

                    pixmap = QPixmap.fromImage(image)
                else:
                    pixmap = QtGui.QPixmap(path)
                if not pixmap.isNull():
                    splash = QtWidgets.QSplashScreen(pixmap, WindowType.WindowStaysOnTopHint)
                    splash.show()
                    sleep(0.2)
                    splash.repaint()
                    break  # Done.
        return splash

    #@ LeoQtGui.dismiss_splash_screen
    def dismiss_splash_screen(self) -> None:
        gui = self
        # Warning: closing the splash screen must be done in the main thread!
        if g.unitTesting:
            return
        if gui.splashScreen:
            gui.splashScreen.hide()
            # gui.splashScreen.deleteLater()
            gui.splashScreen = None

    #@< LeoQtGui: Utils
    #@> LeoQtGui._self_and_subtree
    def _self_and_subtree(self, qt_obj: QObject) -> Generator[Any, None, None]:
        """Yield w and all of w's descendants."""
        if not qt_obj:
            return
        yield qt_obj
        for child in qt_obj.children():
            yield from self._self_and_subtree(child)

    #@ LeoQtGui.enableSignalDebugging
    from PyQt6 import QtTest

    QSignalSpy = QtTest.QSignalSpy
    assert QSignalSpy

    #@ LeoQtGui.equalize_splitter
    def equalize_splitter(self, splitter):
        """Equalize all the splitter's contents."""
        if not splitter:
            return
        if isinstance(splitter, QtWidgets.QSplitter):
            splitter.setSizes([100000] * len(splitter.sizes()))
        else:
            g.trace(f"Not a QSplitter: {splitter.__class__.__name__}")

    #@ LeoQtGui.find_parent_splitter
    def find_parent_splitter(self, widget: QWidget) -> tuple[QSplitter, QWidget] | None:
        """
        Find the nearest parent QSplitter widget for the given widget.

        Return (splitter, child) where:
        - splitter is the QSplitter containing the widget.
        - child is the *direct* child of the splitter that contains the widget.
          The child might or might not be the widget itself.
        """
        direct_child: Any = widget
        parent = widget.parent()
        while parent:
            if isinstance(parent, QtWidgets.QSplitter):
                return parent, cast(QWidget, direct_child)
            direct_child = parent
            parent = parent.parent()
        return None

    #@ LeoQtGui.find_widget_by_name
    def find_widget_by_name(self, c: Cmdr, name: str) -> QWidget | None:
        for w in self._self_and_subtree(c.frame.top):
            if w is not None and w.objectName() == name:
                return w
        return None

    #@ LeoQtGui.get_top_splitter
    def get_top_splitter(self, c: Cmdr) -> QWidget | None:
        return self.find_widget_by_name(c, 'main_splitter')

    #@ LeoQtGui.isTextWidget/Wrapper
    def isTextWidget(self, w: Any) -> bool:
        """Return True if w is some kind of Qt text widget."""
        if Qsci:
            return isinstance(w, (Qsci.QsciScintilla, QtWidgets.QTextEdit))
        return isinstance(w, QtWidgets.QTextEdit)

    def isTextWrapper(self, w: Any) -> bool:
        """Return True if w is a Text widget suitable for text-oriented commands."""
        if w is None:
            return False
        if isinstance(w, (g.NullObject, g.TracingNullObject)):
            return True
        return issubclass(w.__class__, QTextMixin)

    #@ LeoQtGui.widget_name
    def widget_name(self, w: QWidget) -> str:
        return (
                 cast(Any, w).getName() or '' if hasattr(w, 'getName')
            else w.objectName() or '' if hasattr(w, 'objectName')
            else ''
        )  # fmt: skip

    #@< LeoQtGui: Widget constructors
    #@> LeoQtGui.createButton
    def createButton(self, parent: QWidget, name: str, label: str) -> QPushButton:
        w = QtWidgets.QPushButton(parent)
        w.setObjectName(name)
        w.setText(label)
        return w

    #@ LeoQtGui.createFrame
    def createFrame(
        self,
        parent: QWidget,
        name: str,
        hPolicy: Policy | None = None,
        vPolicy: Policy | None = None,
        lineWidth: int = 1,
        shadow: Shadow | None = None,
        shape: Shape | None = None,
    ) -> QFrame:
        """Create a Qt Frame."""
        if shadow is None:
            shadow = Shadow.Plain
        if shape is None:
            shape = Shape.NoFrame

        w = QtWidgets.QFrame(parent)
        self.setSizePolicy(w, kind1=hPolicy, kind2=vPolicy)
        w.setFrameShape(shape)
        w.setFrameShadow(shadow)
        w.setLineWidth(lineWidth)
        w.setObjectName(name)
        return w

    #@ LeoQtGui.createGrid
    def createGrid(
        self, parent: QWidget, name: str, margin: int = 0, spacing: int = 0
    ) -> QGridLayout:
        w = QtWidgets.QGridLayout(parent)
        w.setContentsMargins(QtCore.QMargins(margin, margin, margin, margin))
        w.setSpacing(spacing)
        w.setObjectName(name)
        return w

    #@ LeoQtGui.createHLayout & createVLayout
    def createHLayout(
        self, parent: QWidget, name: str, margin: int = 0, spacing: int = 0
    ) -> QHBoxLayout:
        hLayout = QtWidgets.QHBoxLayout(parent)
        hLayout.setObjectName(name)
        hLayout.setSpacing(spacing)
        hLayout.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        return hLayout

    def createVLayout(
        self, parent: QWidget, name: str, margin: int = 0, spacing: int = 0
    ) -> QVBoxLayout:
        vLayout = QtWidgets.QVBoxLayout(parent)
        vLayout.setObjectName(name)
        vLayout.setSpacing(spacing)
        vLayout.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        return vLayout

    #@ LeoQtGui.createLabel
    def createLabel(self, parent: QWidget, name: str, label: str) -> QLabel:
        w = QtWidgets.QLabel(parent)
        w.setObjectName(name)
        w.setText(label)
        return w

    #@ LeoQtGui.createTabWidget
    def createTabWidget(
        self,
        parent: QWidget,
        name: str,
        hPolicy: Policy | None = None,
        vPolicy: Policy | None = None,
    ) -> QTabWidget:
        w = QtWidgets.QTabWidget(parent)
        self.setSizePolicy(w, kind1=hPolicy, kind2=vPolicy)
        w.setObjectName(name)
        return w

    #@ LeoQtGui.setSizePolicy
    def setSizePolicy(
        self, widget: QWidget, kind1: Policy | None = None, kind2: Policy | None = None
    ) -> None:
        if kind1 is None:
            kind1 = Policy.Ignored
        if kind2 is None:
            kind2 = Policy.Ignored
        sizePolicy = QtWidgets.QSizePolicy(kind1, kind2)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(sizePolicy)

    #@-others


#@<2 class StyleClassManager
class StyleClassManager:
    style_sclass_property = 'style_class'  # name of QObject property for styling

    #@+others
    #@> StyleClassManager.update_view
    def update_view(self, w: QTextMixin) -> None:
        """update_view - Make Qt apply w's style

        :param QWidgit w: widget to style
        """

        w.setStyleSheet("/* */")  # forces visual update

    #@ StyleClassManager.add_sclass
    def add_sclass(self, w: QTextMixin, prop: str) -> None:
        """Add style class to QWidget w"""
        if not prop:
            return
        props = self.sclasses(w)
        if prop not in props:
            props.append(prop)
            self.set_sclasses(w, props)

    #@ StyleClassManager.clear_sclasses
    def clear_sclasses(self, w: QTextMixin) -> None:
        """Remove all style classes from QWidget w"""
        w.setProperty(self.style_sclass_property, '')

    #@ StyleClassManager.has_sclass
    def has_sclass(self, w: QTextMixin, prop: str) -> bool:
        """Check for style class or list of classes prop on QWidget w"""
        if not prop:
            return False
        props = self.sclasses(w)
        if isinstance(prop, str):
            ans = [prop in props]
        else:
            ans = [i in props for i in prop]
        return all(ans)

    #@ StyleClassManager.remove_sclass
    def remove_sclass(self, w: QTextMixin, prop: str) -> None:
        """Remove style class or list of classes prop from QWidget w"""
        if not prop:
            return
        props = self.sclasses(w)
        if isinstance(prop, str):
            props = [i for i in props if i != prop]
        else:
            props = [i for i in props if i not in prop]

        self.set_sclasses(w, props)

    #@ StyleClassManager.sclasses
    def sclasses(self, w: QTextMixin) -> list[str]:
        """return list of style classes for QWidget w"""
        return str(w.property(self.style_sclass_property) or '').split()

    #@ StyleClassManager.set_sclasses
    def set_sclasses(self, w: QTextMixin, classes: list[str]) -> None:
        """Set style classes for QWidget w to list in classes"""
        w.setProperty(self.style_sclass_property, f" {' '.join(set(classes))} ")

    #@-others


#@< class StyleSheetManager
class StyleSheetManager:
    """A class to manage (reload) Qt style sheets."""

    #@+others
    #@>  StyleSheetManager.__init__
    def __init__(self, c: Cmdr, safe: bool = False) -> None:
        """Ctor the ReloadStyle class."""
        self.c = c
        self.color_db = leoColor.leo_color_database
        self.safe = safe
        self.settings_p = g.findNodeAnywhere(c, '@settings')
        self.mng = StyleClassManager()
        # This warning is inappropriate in some contexts.
        # if not self.settings_p:
        # g.es("No '@settings' node found in outline.  See:")
        # g.es("https://leo-editor.github.io/leo-editor/tutorial-basics.html#configuring-leo")

    #@  StyleSheetManager.reload_settings
    def reload_settings(self, sheet: str | None = None) -> None:
        """
        Recompute and apply the stylesheet.
        Called automatically by the reload-settings commands.
        """
        if not sheet:
            sheet = self.get_style_sheet_from_settings()
        if sheet:
            w = self.get_master_widget()
            w.setStyleSheet(sheet)
        # self.c.redraw()

    reloadSettings = reload_settings

    #@ StyleSheetManager: Paths...
    #@> StyleSheetManager.compute_icon_directories
    def compute_icon_directories(self) -> list[str]:
        """
        Return a list of *existing* directories that could contain theme-related icons.
        """
        exists = g.os_path_exists
        home = g.app.homeDir
        join = g.finalize_join
        leo = join(g.app.loadDir, '..')
        table = [
            join(home, '.leo', 'Icons'),
            # join(home, '.leo'),
            join(leo, 'themes', 'Icons'),
            join(leo, 'themes'),
            join(leo, 'Icons'),
        ]
        table = [z for z in table if exists(z)]
        for directory in self.compute_theme_directories():
            if directory not in table:
                table.append(directory)
            directory2 = join(directory, 'Icons')
            if directory2 not in table:
                table.append(directory2)
        return [g.os_path_normslashes(z) for z in table if g.os_path_exists(z)]

    #@ StyleSheetManager.compute_theme_directories
    def compute_theme_directories(self) -> list[str]:
        """
        Return a list of *existing* directories that could contain theme .leo files.
        """
        lm = g.app.loadManager
        table = lm.computeThemeDirectories()[:]
        directory = g.os_path_normslashes(g.app.theme_directory)
        if directory and directory not in table:
            table.insert(0, directory)
        # All entries are known to exist and have normalized slashes.
        return table

    #@ StyleSheetManager.find_icon_path
    def find_icon_path(self, setting: str) -> str | None:
        """Return the path to the open/close indicator icon."""
        c = self.c
        s = c.config.getString(setting)
        if not s:
            return None  # Not an error.
        for directory in self.compute_icon_directories():
            path = g.finalize_join(directory, s)
            if g.os_path_exists(path):
                return path
        g.es_print('no icon found for:', setting)
        return None

    #@< StyleSheetManager: Settings
    #@> StyleSheetManager.default_style_sheet
    def default_style_sheet(self) -> str:
        """Return a reasonable default style sheet."""
        # Valid color names: http://www.w3.org/TR/SVG/types.html#ColorKeywords
        g.trace('===== using default style sheet =====')
        return '''\

    /* A QWidget: supports only background attributes.*/
    QSplitter::handle {
        background-color: #CAE1FF; /* Leo's traditional lightSteelBlue1 */
    }
    QSplitter {
        border-color: white;
        background-color: white;
        border-width: 3px;
        border-style: solid;
    }
    QTreeWidget {
        background-color: #ffffec; /* Leo's traditional tree color */
    }
    QsciScintilla {
        background-color: pink;
    }
    '''

    #@ StyleSheetManager.get_data
    def get_data(self, setting: str) -> list:
        """Return the value of the @data node for the setting."""
        c = self.c
        return c.config.getData(setting, strip_comments=False, strip_data=False) or []

    #@ StyleSheetManager.get_style_sheet_from_settings
    def get_style_sheet_from_settings(self) -> str:
        """
        Scan for themes or @data qt-gui-plugin-style-sheet nodes.
        Return the text of the relevant node.
        """
        aList1 = self.get_data('qt-gui-plugin-style-sheet')
        aList2 = self.get_data('qt-gui-user-style-sheet')
        if aList2:
            aList1.extend(aList2)
        sheet = ''.join(aList1)
        sheet = self.expand_css_constants(sheet)
        return sheet

    #@ StyleSheetManager.print_style_sheet
    def print_style_sheet(self) -> None:
        """Show the top-level style sheet."""
        w = self.get_master_widget()
        sheet = w.styleSheet()
        print(f"style sheet for: {w}...\n\n{sheet}")

    #@ StyleSheetManager.set_style_sheets
    def set_style_sheets(
        self, all: bool = True, top: QWidget | None = None, w: QWidget | None = None
    ) -> None:
        """Set the master style sheet for all widgets using config settings."""
        c = self.c
        if top is None:
            top = c.frame.top
        selectors = ['qt-gui-plugin-style-sheet']
        if all:
            selectors.append('qt-gui-user-style-sheet')
        sheets = []
        sheet = ""
        for name in selectors:
            # don't strip `#selector_name { ...` type syntax
            if sheet_data := c.config.getData(name, strip_comments=False):
                if '\n' in sheet_data[0]:
                    sheet = ''.join(sheet_data)
                else:
                    sheet = '\n'.join(sheet_data)
            if sheet and sheet.strip():
                line0 = f"\n/* ===== From {name} ===== */\n\n"
                sheet = line0 + sheet
                sheets.append(sheet)
        if sheets:
            sheet = "\n".join(sheets)
            # store *before* expanding, so later expansions get new zoom
            c.active_stylesheet = sheet
            sheet = self.expand_css_constants(sheet)
            if not sheet:
                sheet = self.default_style_sheet()
            if w is None:
                w = self.get_master_widget(top)
            w.setStyleSheet(sheet)

    #@< StyleSheetManager: Stylesheets
    # Computations on stylesheets themselves.
    #@> StyleSheetManager.expand_css_constants & helpers
    css_warning_given = False  # For do_pass.

    def expand_css_constants(self, sheet: str, settingsDict: g.SettingsDict | None = None) -> str:
        """Expand @ settings into their corresponding constants."""
        c = self.c
        trace = 'zoom' in g.app.debug
        if settingsDict is None:
            settingsDict = c.config.settingsDict  # A g.SettingsDict.
        constants, deltas = self.adjust_sizes(settingsDict)
        if trace:
            print('')
            g.trace(f"zoom constants: {constants}")
            g.printObj(deltas, tag='zoom deltas')  # A defaultdict
        sheet = self.replace_indicator_constants(sheet)
        for pass_n in range(10):
            to_do = self.find_constants_referenced(sheet)
            if not to_do:
                break
            old_sheet = sheet
            sheet = self.do_pass(constants, deltas, settingsDict, sheet, to_do)
            if sheet == old_sheet:
                break
        else:
            g.trace('Too many iterations')
        if to_do:
            g.trace('Unresolved @constants')
            g.printObj(to_do)
        sheet = self.resolve_urls(sheet)
        sheet = sheet.replace('\\\n', '')  # join lines ending in \
        return sheet

    #@> StyleSheetManager.adjust_sizes
    def adjust_sizes(self, settingsDict: dict) -> tuple[dict, Any]:
        """Adjust constants to reflect c._style_deltas."""
        c = self.c
        constants = {}
        deltas = c._style_deltas
        for delta in c._style_deltas:
            # adjust @font-size-body by font_size_delta
            # easily extendable to @font-size-*
            val = c.config.getString(delta)
            passes = 10
            while passes and val and val.startswith('@'):
                key = g.app.config.canonicalizeSettingName(val[1:])
                if val := settingsDict.get(key):
                    val = val.val
                passes -= 1
            if deltas[delta] and (val is not None):
                size = ''.join(i for i in val if i in '01234567890.')
                units = ''.join(i for i in val if i not in '01234567890.')
                size = max(1, float(size) + deltas[delta])
                constants['@' + delta] = f"{size}{units}"
        return constants, deltas

    #@ StyleSheetManager.do_pass
    def do_pass(
        self,
        constants: dict,
        deltas: list[str],
        settingsDict: dict[str, Any],
        sheet: str,
        to_do: list[str],
    ) -> str:
        to_do.sort(key=len, reverse=True)
        for const in to_do:
            value = None
            if const in constants:
                # This constant is about to be removed.
                value = constants[const]
                if const[1:] not in deltas and not self.css_warning_given:
                    self.css_warning_given = True
                    g.es_print(f"'{const}' from style-sheet comment definition, ")
                    g.es_print("please use regular @string / @color type @settings.")
            else:
                # lowercase, without '@','-','_', etc.
                key = g.app.config.canonicalizeSettingName(const[1:])
                value = settingsDict.get(key)
                if value is not None:
                    # New in Leo 5.5: Do NOT add comments here.
                    # They RUIN style sheets if they appear in a nested comment!
                    # value = '%s /* %s */' % (value.val, key)
                    value = value.val
                elif key in self.color_db:
                    # New in Leo 5.5: Do NOT add comments here.
                    # They RUIN style sheets if they appear in a nested comment!
                    value = self.color_db.get(key)
            if value:
                # Partial fix for #780.
                try:
                    # Don't replace shorter constants occurring in larger.
                    sheet = re.sub(
                        const + "(?![-A-Za-z0-9_])",
                        value,
                        sheet,
                    )
                except Exception:
                    g.es_print('Exception handling style sheet')
                    g.es_print(sheet)
                    g.es_exception()
            else:
                pass
                # tricky, might be an undefined identifier, but it might
                # also be a @foo in a /* comment */, where it's harmless.
                # So rely on whoever calls .setStyleSheet() to do the right thing.
        return sheet

    #@ StyleSheetManager.find_constants_referenced
    def find_constants_referenced(self, text: str) -> list[str]:
        """find_constants - Return a list of constants referenced in the supplied text,
        constants match::

            @[A-Za-z_][-A-Za-z0-9_]*
            i.e. @foo_1-5

        :Parameters:
        - `text`: text to search
        """
        aList = sorted(set(re.findall(r"@[A-Za-z_][-A-Za-z0-9_]*", text)))
        # Exempt references to Leo constructs.
        for s in ('@button', '@constants', '@data', '@language'):
            if s in aList:
                aList.remove(s)
        return aList

    #@ StyleSheetManager.replace_indicator_constants
    def replace_indicator_constants(self, sheet: str) -> str:
        """
        In the stylesheet, replace (if they exist)::

            image: @tree-image-closed
            image: @tree-image-open

        by::

            url(path/closed.png)
            url(path/open.png)

        path can be relative to ~ or to leo/Icons.

        Assuming that ~/myIcons/closed.png exists, either of these will work::

            @string tree-image-closed = nodes-dark/triangles/closed.png
            @string tree-image-closed = myIcons/closed.png

        Return the updated stylesheet.
        """
        close_path = self.find_icon_path('tree-image-closed')
        open_path = self.find_icon_path('tree-image-open')
        # Make all substitutions in the stylesheet.
        table = (
            (open_path,  re.compile(r'\bimage:\s*@tree-image-open', re.IGNORECASE)),
            (close_path, re.compile(r'\bimage:\s*@tree-image-closed', re.IGNORECASE)),
            # (open_path,  re.compile(r'\bimage:\s*at-tree-image-open', re.IGNORECASE)),
            # (close_path, re.compile(r'\bimage:\s*at-tree-image-closed', re.IGNORECASE)),
        )  # fmt: skip
        for path, pattern in table:
            for mo in pattern.finditer(sheet):
                old = mo.group(0)
                new = f"image: url({path})"
                sheet = sheet.replace(old, new)
        return sheet

    #@ StyleSheetManager.resolve_urls
    def resolve_urls(self, sheet: str) -> str:
        """Resolve all relative url's so they use absolute paths."""
        trace = 'themes' in g.app.debug
        pattern = re.compile(r'url\((.*)\)')
        join = g.finalize_join
        directories = self.compute_icon_directories()
        paths_traced = False
        if trace:
            paths_traced = True
            g.trace('Search paths...')
            g.printObj(directories)
        # Pass 1: Find all replacements without changing the sheet.
        replacements = []
        for mo in pattern.finditer(sheet):
            url = mo.group(1)
            if url.startswith(':/'):
                url = url[2:]
            elif g.os_path_isabs(url):
                if trace:
                    g.trace('ABS:', url)
                continue
            for directory in directories:
                path = join(directory, url)
                if g.os_path_exists(path):
                    if trace:
                        g.trace(f"{url:35} ==> {path}")
                    old = mo.group(0)
                    new = f"url({path})"
                    replacements.append(
                        (old, new),
                    )
                    break
            else:
                g.trace(f"{url:35} ==> NOT FOUND")
                if not paths_traced:
                    paths_traced = True
                    g.trace('Search paths...')
                    g.printObj(directories)
        # Pass 2: Now we can safely make the replacements.
        for old, new in reversed(replacements):
            sheet = sheet.replace(old, new)
        return sheet

    #@< StyleSheetManager.munge
    def munge(self, stylesheet: str) -> str:
        """
        Return the stylesheet without extra whitespace.

        To avoid false mismatches, this should approximate what Qt does.
        To avoid false matches, this should not munge too much.
        """
        s = ''.join(
            [s.lstrip().replace('  ', ' ').replace(' \n', '\n') for s in g.splitLines(stylesheet)]
        )
        return s.rstrip()  # Don't care about ending newline.

    #@ StyleSheetManager.rescale_sizes
    def rescale_sizes(self, sheet: str, factor: float) -> str:
        """
        #@+<< docstring >>
        #@> << docstring >>
        Rescale all pt or px sizes in CSS stylesheet or Leo theme.

        Sheets can have either "logical" or "actual" sizes.
        "Logical" sizes are ones like "@font-family-base = 10.6pt".
        "Actual" sizes are the ones in the "qt-gui-plugin-style-sheet" subtree.
        They look like "font-size: 11pt;"

        In Qt stylesheets, only sizes in pt or px are honored, so
        those are the only ones changed by this method.  Padding,
        margin, etc. sizes will be changed as well as font sizes.

        Sizes do not have to be integers (e.g., 10.5 pt).  Qt honors
        non-integer point sizes, with at least a 0.5pt granularity.
        It's currently unknown how non-integer px sizes are handled.

        No size will be scaled down to less than 1.

        ARGUMENTS
        sheet -- a CSS stylesheet or a Leo theme as a string.  The Leo
                 theme file should be read as a string before being passed
                 to this method.  If a Leo theme, the output will be a
                 well-formed Leo outline.

        scale -- the scaling factor as a float or integer.  For example,
                 a scale of 1.5 will increase all the sizes by a factor of 1.5.

        RETURNS
        the modified sheet as a string.

        #@-<< docstring >>
        """
        RE = r'([=:])[ ]*([.1234567890]+)(p[tx])'

        def scale(matchobj: re.Match, scale: float = factor) -> str:
            prefix = matchobj.group(1)
            sz = matchobj.group(2)
            units = matchobj.group(3)
            try:
                scaled = max(float(sz) * factor, 1)
            except Exception as e:
                g.es('ssm.rescale_fonts:', e)
                return matchobj.group(0)
            return f'{prefix} {scaled:.1f}{units}'

        newsheet = re.sub(RE, scale, sheet)
        return newsheet

    #@<2 StyleSheetManager: Widgets
    #@> StyleSheetManager.get_master_widget
    def get_master_widget(self, top: QWidget | None = None) -> QWidget:
        """
        Carefully return the master widget.
        c.frame.top is a DynamicWindow.
        """
        if top is None:
            top = self.c.frame.top
        master = top.leo_master or top
        return master

    #@ StyleSheetManager.set selected_style_sheet
    def set_selected_style_sheet(self) -> None:
        """For manual testing: update the stylesheet using c.p.b."""
        if not g.unitTesting:
            c = self.c
            sheet = c.p.b
            sheet = self.expand_css_constants(sheet)
            w = self.get_master_widget(c.frame.top)
            w.setStyleSheet(sheet)

    #@-others


#@-others
#@@language python
#@@tabwidth -4
#@@pagewidth 70
#@-leo
