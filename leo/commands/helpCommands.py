#@+leo-ver=cub-1-thin
#@0 [ekr.20150514040138.1] @f ../commands/helpCommands.py
"""Leo's help commands."""

#@+<< helpCommands imports & annotations >>
#@> << helpCommands imports & annotations >>
from __future__ import annotations
from collections.abc import Callable
import io
import re
import sys
import textwrap
from typing import TYPE_CHECKING
from leo.core import leoGlobals as g
from leo.commands.baseCommands import BaseEditCommandsClass

if TYPE_CHECKING:  # pragma: no cover
    from leo.core.leoGui import LeoKeyEvent
#@-<< helpCommands imports & annotations >>


def cmd(name: str) -> Callable:
    """Command decorator for the helpCommands class."""
    return g.new_cmd_decorator(name, ['c', 'helpCommands'])


#@+others
#@ class HelpCommandsClass
class HelpCommandsClass(BaseEditCommandsClass):
    """A class containing Leo's help-for commands."""

    #@+others
    #@> help
    @cmd('help')
    def help_command(self, event: LeoKeyEvent | None = None) -> None:
        """Prints an introduction to Leo's help system."""
        #@+<< define rst_s >>
        #@-<< define rst_s >>
        self.c.putHelpFor(rst_s)

    #@ helpForAbbreviations
    @cmd('help-for-abbreviations')
    def helpForAbbreviations(self, event: LeoKeyEvent | None = None) -> None:
        """Explains Leo's abbreviations."""
        #@+<< define s >>
        #@-<< define s >>
        self.c.putHelpFor(s)

    #@ helpForAutocompletion
    @cmd('help-for-autocompletion')
    def helpForAutocompletion(self, event: LeoKeyEvent | None = None) -> None:
        """Explains how to use autocompletion."""
        #@+<< define s >>
        #@-<< define s >>
        self.c.putHelpFor(s)

    #@ helpForBindings
    @cmd('help-for-bindings')
    def helpForBindings(self, event: LeoKeyEvent | None = None) -> None:
        """Explains Leo's keyboard bindings."""
        #@+<< define s >>
        #@-<< define s >>
        self.c.putHelpFor(s)

    #@ helpForCommand & helpers
    @cmd('help-for-command')
    def helpForCommand(self, event: LeoKeyEvent | None = None) -> None:
        """Prompts for a command name and prints the help message for that command."""
        c, k = self.c, self.c.k
        s = '''\
    Alt-0 (vr-toggle) hides this help message.

    Type the name of the command, followed by Return.
    '''
        c.putHelpFor(s)
        c.minibufferWantsFocusNow()
        k.fullCommand(event, help=True, helpHandler=self.helpForCommandFinisher)

    #@> getBindingsForCommand
    def getBindingsForCommand(self, commandName: str) -> str:
        k = self.c.k
        data = []
        n1, n2 = 4, 20
        d = k.bindingsDict
        for stroke in sorted(d):
            assert g.isStroke(stroke), repr(stroke)
            aList = d.get(stroke, [])
            for bi in aList:
                if bi.commandName == commandName:
                    pane = '' if bi.pane == 'all' else f" {bi.pane}:"
                    s1 = pane
                    s2 = k.prettyPrintKey(stroke)
                    s3 = bi.commandName
                    n1 = max(n1, len(s1))
                    n2 = max(n2, len(s2))
                    data.append(
                        (s1, s2, s3),
                    )
        data.sort(key=lambda x: x[1])
        return ','.join([f"{z1} {z2}" for z1, z2, z3 in data]).strip()

    #@ helpForCommandFinisher
    def helpForCommandFinisher(self, commandName: str) -> None:
        c, s = self.c, None
        if commandName and commandName.startswith('help-for-'):
            # Execute the command itself.
            c.doCommandByName(commandName)
        else:
            if commandName:
                bindings = self.getBindingsForCommand(commandName)
                s = 'no docstring available'
                if func := c.commandsDict.get(commandName):
                    if s := g.getDocStringForFunction(func):
                        s = self.replaceBindingPatterns(s)
                # Create the title.
                s2 = f"{commandName} ({bindings})" if bindings else commandName
                underline = '+' * len(s2)
                title = f"{s2}\n{underline}\n\n"
                if 1:  # 2015/03/24
                    s = title + textwrap.dedent(s)
                else:
                    # Fixes bug 618570:
                    s = title + ''.join(
                        [line.lstrip() if line.strip() else '\n' for line in g.splitLines(s)]
                    )
            else:
                #@+<< set s to about help-for-command >>
                #@> << set s to about help-for-command >>
                s = '''\

                ++++++++++++++++++++++++
                About Leo's help command
                ++++++++++++++++++++++++

                Invoke Leo's help-for-command as follows::

                    <F1>
                    <Alt-X>help-for-command<return>

                Next, type the name of one of Leo's commands.
                You can use tab completion.  Examples::

                    <F1><tab>           shows all commands.
                    <F1>help-for<tab>   shows all help-for- commands.

                Here are the help-for commands::

                    help-for-abbreviations
                    help-for-autocompletion
                    help-for-bindings
                    help-for-command
                    help-for-debugging-commands
                    help-for-dynamic-abbreviations
                    help-for-find-commands
                    help-for-minibuffer
                    help-for-python
                    help-for-regular-expressions

                '''
                #@-<< set s to about help-for-command >>
            c.putHelpFor(s)

    #@< replaceBindingPatterns
    def replaceBindingPatterns(self, s: str) -> str:
        """
        For each instance of the pattern !<command-name>! in s,
        replace the pattern by the key binding for command-name.
        """
        c = self.c
        pattern = re.compile(r'!<(.*)>!')
        while True:
            m = pattern.search(s, 0)
            if m is None:
                break
            name = m.group(1)
            _, aList = c.config.getShortcut(name)
            for bi in aList:
                if bi.pane == 'all':
                    key = c.k.prettyPrintKey(bi.stroke.s)
                    break
            else:
                key = f"<Alt-X>{name}<Return>"
            s = s[: m.start()] + key + s[m.end() :]
        return s

    #@< helpForCreatingExternalFiles
    @cmd('help-for-creating-external-files')
    def helpForCreatingExternalFiles(self, event: LeoKeyEvent | None = None) -> None:
        """Explains how to create external files."""
        #@+<< define s >>
        #@-<< define s >>
        s = s.replace('\\', '')
        self.c.putHelpFor(s)

    #@ helpForDebuggingCommands
    @cmd('help-for-debugging-commands')
    def helpForDebuggingCommands(self, event: LeoKeyEvent | None = None) -> None:
        """Explains Leo's debugging commands."""
        #@+<< define s >>
        #@-<< define s >>
        self.c.putHelpFor(s)

    #@ helpForDragAndDrop
    @cmd('help-for-drag-and-drop')
    def helpForDragAndDrop(self, event: LeoKeyEvent | None = None) -> None:
        """Explains Leo's drag-and-drop commands."""
        #@+<< define s >>
        #@-<< define s >>
        self.c.putHelpFor(s)

    #@ helpForDynamicAbbreviations
    @cmd('help-for-dynamic-abbreviations')
    def helpForDynamicAbbreviations(self, event: LeoKeyEvent | None = None) -> None:
        """Explains Leo's abbreviations."""
        #@+<< define s >>
        #@-<< define s >>
        self.c.putHelpFor(s)

    #@ helpForFindCommands
    @cmd('help-for-find-commands')
    def helpForFindCommands(self, event: LeoKeyEvent | None = None) -> None:
        """Explains Leo's find commands."""
        c = self.c
        d = c.k.computeInverseBindingDict()

        def find_binding(command: str) -> str:
            aList = d.get(command) or []
            for pane, stroke in aList:
                if pane == 'all':
                    return stroke.s
            return ''

        #@+<< help-for-find-commands: define s >>
        #@> << help-for-find-commands: define s >>
        #@@language rest

        s = '''

        Finding & replacing text
        ------------------------

        vr-toggle (<vr-toggle>) hides this help message.

        **<start-search>** (start-search) shows the Find pane
        and puts focus in the find box.

        Enter the find text and the replacement text if desired::

            Tab switches focus from widget to widget.
            Return executes the find-next command.

        When Leo selects the found text you can do the following commands::

            find-next:          <find-next>
            find-prev:           <find-prev>
            replace:            <replace>
            replace-all:        <replace-all>
            replace-then-find:  <replace-then-find>
            keyboard-quit:      <keyboard-quit>

        You may use Leo's find-toggle commands to toggle check boxes and radio buttons::

            toggle-find-ignore-case-option:  <Alt+Ctrl+i>
            toggle-find-in-body-option:      <Alt+Ctrl+b>
            toggle-find-in-headline-option:  <Alt+Ctrl+h>
            toggle-find-mark-changes-option: <Alt+Ctrl+c>
            toggle-find-mark-finds-option:   <Alt+Ctrl+f>
            toggle-find-regex-option:        <Alt+Ctrl+x>
            toggle-find-word-option:         <Alt+Ctrl+w>

        These commands are listed in the Search menu.

        Incremental searching
        ---------------------

        Incremental search is done only from the minibuffer::

            isearch-forward:        <isearch-forward>
            isearch-backward:       <isearch-backward>
            isearch-forward-regex:  <isearch-forward-regex>
            isearch-backward-regex: <isearch-backward-regex>

            BackSpace retracts the search
            All other characters extend the search

        During an incremental search::

            Enter or Ctrl-G stops the search.
            Alt-S finds the search string again.
            Alt-R ditto for reverse searches.
        '''
        #@-<< help-for-find-commands: define s >>

        table = (
            'find-next',
            'find-prev',
            'isearch-backward',
            'isearch-backward-regex',
            'isearch-forward',
            'isearch-forward-regex',
            'keyboard-quit',
            'replace',
            'replace-all',
            'replace-then-find',
            'start-search',
            'toggle-find-ignore-case-option',
            'toggle-find-in-body-option',
            'toggle-find-in-headline-option',
            'toggle-find-mark-changes-option',
            'toggle-find-mark-finds-option',
            'toggle-find-regex-option',
            'toggle-find-word-option',
            'vr-toggle',
        )
        for command in table:
            s = s.replace(f"<{command}>", find_binding(command))
        self.c.putHelpFor(s)

    #@< helpForKeystroke
    @cmd('help-for-keystroke')
    def helpForKeystroke(self, event: LeoKeyEvent | None = None) -> None:
        """Prompts for any key and prints the bindings for that key."""
        c, k = self.c, self.c.k
        if not event:
            return  # PR #4812
        state_name = 'help-for-keystroke'
        state = k.getState(state_name)
        if state == 0:
            k.setLabelBlue('Enter any key: ')
            k.setState(state_name, 1, self.helpForKeystroke)
            c.minibufferWantsFocus()
        else:
            d = k.bindingsDict
            k.clearState()
            result = []
            for bi in d.get(event.stroke, []):  # a list of BindingInfo objects.
                pane, cmd = bi.pane, bi.commandName
                result.append(cmd if pane == 'all' else f"{pane}: {cmd}")
            s = f"{event.stroke.s}: {','.join(result)}"
            k.showStateAndMode()
            c.frame.putStatusLine(s, bg='blue', fg='white')
            c.bodyWantsFocus()

    #@ helpForLayouts
    @cmd('help-for-layouts')
    def helpForLayouts(self, event: LeoKeyEvent | None = None) -> None:
        """Print a message telling you how to use Leo's layouts."""
        c = self.c
        #@+<< create listing list>>
        #@-<< create listing list>>
        c.putHelpFor(''.join(listing))

    #@ helpForMinibuffer
    @cmd('help-for-minibuffer')
    def helpForMinibuffer(self, event: LeoKeyEvent | None = None) -> None:
        """Print a messages telling you how to get started with Leo."""
        # A bug in Leo: triple quotes puts indentation before each line.
        c = self.c
        #@+<< define s >>
        #@-<< define s >>
        c.putHelpFor(s)

    #@ helpForRegularExpressions
    @cmd('help-for-regular-expressions')
    def helpForRegularExpressions(self, event: LeoKeyEvent | None = None) -> None:
        """Explains the regular expressions used by Leo's find commands."""
        #@+<< define s >>
        #@-<< define s >>
        self.c.putHelpFor(s)

    #@ helpForScripting
    @cmd('help-for-scripting')
    def helpForScripting(self, event: LeoKeyEvent | None = None) -> None:
        """Shows a tutorial about scripting Leo."""
        #@+<< define s >>
        #@-<< define s >>
        self.c.putHelpFor(s)

    #@ helpForSettings
    @cmd('help-for-settings')
    def helpForSettings(self, event: LeoKeyEvent | None = None) -> None:
        """Explains Leo's settings."""
        #@+<< define s >>
        #@-<< define s >>
        self.c.putHelpFor(s)

    #@ help.showColorSettings
    @cmd('show-color-settings')
    def showColorSettings(self, event: LeoKeyEvent | None = None) -> None:
        """
        Print the value of all @color settings.

        The following shows where the each setting comes from:

        -     leoSettings.leo,
        -  @  @button, @command, @mode.
        - [D] default settings.
        - [F] indicates the file being loaded,
        - [M] myLeoSettings.leo,
        - [T] theme .leo file.
        """
        self.c.config.printColorSettings()

    #@ help.showFontSettings
    @cmd('show-font-settings')
    def showFontSettings(self, event: LeoKeyEvent | None = None) -> None:
        """
        Print the value of every @font setting.

        The following shows where the each setting comes from:

        -     leoSettings.leo,
        -  @  @button, @command, @mode.
        - [D] default settings.
        - [F] indicates the file being loaded,
        - [M] myLeoSettings.leo,
        - [T] theme .leo file.
        """
        self.c.config.printFontSettings()

    #@ help.showSettings
    @cmd('show-settings')
    def showSettings(self, event: LeoKeyEvent | None = None) -> None:
        """
        Print the value of every setting, except key bindings, commands, and
        open-with tables.

        The following shows where the each setting comes from:

        -     leoSettings.leo,
        -  @  @button, @command, @mode.
        - [D] default settings.
        - [F] indicates the file being loaded,
        - [M] myLeoSettings.leo,
        - [T] theme .leo file.
        """
        self.c.config.printSettings()

    #@ help.showSettingsOutline
    @cmd('show-settings-outline')
    def showSettingsOutline(self, event: LeoKeyEvent | None = None) -> None:
        """
        Create and open an outline, summarizing all presently active settings.

        The outline retains the organization of all active settings files.

        See #852: https://github.com/leo-editor/leo-editor/issues/852
        """

        self.c.config.createActivesSettingsOutline()

    #@ pythonHelp
    @cmd('help-for-python')
    def pythonHelp(self, event: LeoKeyEvent | None = None) -> None:
        """Prompt for a arg for Python's help function, and put it to the VR pane."""
        c, k = self.c, self.c.k
        c.minibufferWantsFocus()
        k.setLabelBlue('Python help: ')
        k.get1Arg(event, handler=self.pythonHelp1)

    def pythonHelp1(self, event: LeoKeyEvent | None = None) -> str:
        c, k = self.c, self.c.k
        k.clearState()
        k.resetLabel()
        s = k.arg.strip()
        if not s:
            return ''
        old = sys.stdout
        try:
            sys.stdout = io.StringIO()
            #  If the argument is a string, the string is looked up as a name...
            # and a help page is printed on the console.
            help(str(s))
            s2 = sys.stdout.getvalue()  # #2165
        finally:
            sys.stdout = old
        if not s2:
            return ''
        # Send it to the vr pane as a <pre> block
        s2 = '<pre>' + s2 + '</pre>'
        c.putHelpFor(s2)
        return s2  # For unit tests.

    #@-others


#@-others
#@-leo
