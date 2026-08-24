#@+leo-ver=cub-1-thin
#@0 [ekr.20201202144422.1] @f ../unittests/commands/test_editCommands.py
"""Tests of leo.commands.editCommands."""
# pylint: disable=no-member

import textwrap
from leo.core import leoGlobals as g
from leo.core.leoTest2 import LeoUnitTest
from leo.core.leoGui import LeoKeyEvent


#@+others
#@> class TestEditCommands(LeoUnitTest)
class TestEditCommands(LeoUnitTest):
    """Unit tests for leo/commands/editCommands.py."""

    # For pylint.
    before_p = after_p = parent_p = tempNode = None

    #@+others
    #@> TestEditCommands.run_test
    def run_test(
        self,
        before_b: str,
        after_b: str,  # before/after body text.
        before_sel: str,
        after_sel: str,  # before and after selection ranges.
        command_name: str,
        directives: str = '',
        dedent: bool = True,
    ):
        """
        A helper for many commands tests.
        """
        c = self.c

        def toInt(s):
            return g.toPythonIndex(before_b, s)

        # For shortDescription().
        self.command_name = command_name
        # Compute the result in tempNode.b
        command = c.commandsDict.get(command_name)
        assert command, f"no command: {command_name}"
        # Set the text.
        if dedent:
            parent_b = textwrap.dedent(directives)
            before_b = textwrap.dedent(before_b)
            after_b = textwrap.dedent(after_b)
        else:
            # The unit test is responsible for all indentation.
            parent_b = directives
        self.parent_p.b = parent_b
        self.tempNode.b = before_b
        self.before_p.b = before_b
        self.after_p.b = after_b
        # Set the selection range and insert point.
        w = c.frame.body.wrapper
        i, j = before_sel
        i, j = toInt(i), toInt(j)
        w.setSelectionRange(i, j, insert=j)
        # Run the command!
        event = LeoKeyEvent(c, w=w)  # Leo 6.8.9.
        c.doCommandByName(command_name, event)
        self.assertEqual(self.tempNode.b, self.after_p.b, msg=command_name)

    #@ TestEditCommands.setUp
    def setUp(self):
        """Create the nodes in the commander."""
        super().setUp()
        c = self.c
        # Create top-level parent node.
        self.parent_p = self.root_p.insertAsLastChild()
        # Create children of the parent node.
        self.tempNode = self.parent_p.insertAsLastChild()
        self.before_p = self.parent_p.insertAsLastChild()
        self.after_p = self.parent_p.insertAsLastChild()
        self.tempNode.h = 'tempNode'
        self.before_p.h = 'before'
        self.after_p.h = 'after'
        c.selectPosition(self.tempNode)

    # def tearDown(self):
    # self.c = None
    #@ TestEditCommands: Commands...
    #@> Commands A-B
    #@> test_add-space-to-lines
    def test_add_space_to_lines(self):
        """Test case for add-space-to-lines"""
        before_b = """\
    first line
    line 1
        line a
    line b
    last line
    """
        after_b = """\
    first line
     line 1
         line a
     line b
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.0", "4.6"),
            after_sel=("2.0", "4.7"),
            command_name="add-space-to-lines",
        )

    #@ test_add-tab-to-lines
    def test_add_tab_to_lines(self):
        """Test case for add-tab-to-lines"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
        line 1
            line a
                line b
        line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.0", "5.6"),
            after_sel=("2.0", "5.10"),
            command_name="add-tab-to-lines",
        )

    #@ test_back-char
    def test_back_char(self):
        """Test case for back-char"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.8", "3.8"),
            after_sel=("3.7", "3.7"),
            command_name="back-char",
        )

    #@ test_back-char-extend-selection
    def test_back_char_extend_selection(self):
        """Test case for back-char-extend-selection"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("4.12", "4.12"),
            after_sel=("4.11", "4.12"),
            command_name="back-char-extend-selection",
        )

    #@ test_back-paragraph
    def test_back_paragraph(self):
        """Test case for back-paragraph"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year,
    Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000
    tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly
    weather impacts every American. Communities can now rely on the National Weather
    Service’s StormReady program to help them guard against the ravages of Mother
    Nature.

    Some 90% of all presidentially declared disasters are weather related, leading
    to around 500 deaths per year and nearly $14 billion in damage. StormReady, a
    program started in 1999 in Tulsa, OK, helps arm America's communities with the
    communication and safety skills needed to save lives and property– before and
    during the event. StormReady helps community leaders and emergency managers
    strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of
    severe weather through better planning, education, and awareness. No community
    is storm proof, but StormReady can help communities save lives. Does StormReady
    make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year,
    Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000
    tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly
    weather impacts every American. Communities can now rely on the National Weather
    Service’s StormReady program to help them guard against the ravages of Mother
    Nature.

    Some 90% of all presidentially declared disasters are weather related, leading
    to around 500 deaths per year and nearly $14 billion in damage. StormReady, a
    program started in 1999 in Tulsa, OK, helps arm America's communities with the
    communication and safety skills needed to save lives and property– before and
    during the event. StormReady helps community leaders and emergency managers
    strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of
    severe weather through better planning, education, and awareness. No community
    is storm proof, but StormReady can help communities save lives. Does StormReady
    make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("9.0", "9.0"),
            after_sel=("6.7", "6.7"),
            command_name="back-paragraph",
        )

    #@ test_back-paragraph-extend-selection
    def test_back_paragraph_extend_selection(self):
        """Test case for back-paragraph-extend-selection"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year,
    Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000
    tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly
    weather impacts every American. Communities can now rely on the National Weather
    Service’s StormReady program to help them guard against the ravages of Mother
    Nature.

    Some 90% of all presidentially declared disasters are weather related, leading
    to around 500 deaths per year and nearly $14 billion in damage. StormReady, a
    program started in 1999 in Tulsa, OK, helps arm America's communities with the
    communication and safety skills needed to save lives and property– before and
    during the event. StormReady helps community leaders and emergency managers
    strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of
    severe weather through better planning, education, and awareness. No community
    is storm proof, but StormReady can help communities save lives. Does StormReady
    make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year,
    Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000
    tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly
    weather impacts every American. Communities can now rely on the National Weather
    Service’s StormReady program to help them guard against the ravages of Mother
    Nature.

    Some 90% of all presidentially declared disasters are weather related, leading
    to around 500 deaths per year and nearly $14 billion in damage. StormReady, a
    program started in 1999 in Tulsa, OK, helps arm America's communities with the
    communication and safety skills needed to save lives and property– before and
    during the event. StormReady helps community leaders and emergency managers
    strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of
    severe weather through better planning, education, and awareness. No community
    is storm proof, but StormReady can help communities save lives. Does StormReady
    make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("9.0", "9.5"),
            after_sel=("6.7", "9.5"),
            command_name="back-paragraph-extend-selection",
        )

    #@ test_back-sentence
    def test_back_sentence(self):
        """Test case for back-sentence"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.169", "3.169"),
            after_sel=("3.143", "3.143"),
            command_name="back-sentence",
        )

    #@ test_back-sentence-extend-selection
    def test_back_sentence_extend_selection(self):
        """Test case for back-sentence-extend-selection"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.208", "3.208"),
            after_sel=("3.143", "3.208"),
            command_name="back-sentence-extend-selection",
        )

    #@ test_back-to-home (at end of line)
    def test_back_to_home_at_end_of_line(self):
        """Test case for back-to-home (at end of line)"""
        before_b = """\
    if a:
        b = 'xyz'
    """
        after_b = """\
    if a:
        b = 'xyz'
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.12", "2.12"),
            after_sel=("2.4", "2.4"),
            command_name="back-to-home",
        )

    #@ test_back-to-home (at indentation
    def test_back_to_home_at_indentation(self):
        """Test case for back-to-home (at indentation"""
        before_b = """\
    if a:
        b = 'xyz'
    """
        after_b = """\
    if a:
        b = 'xyz'
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.4", "2.4"),
            after_sel=("2.0", "2.0"),
            command_name="back-to-home",
        )

    #@ test_back-to-home (at start of line)
    def test_back_to_home_at_start_of_line(self):
        """Test case for back-to-home (at start of line)"""
        before_b = """\
    if a:
        b = 'xyz'
    """
        after_b = """\
    if a:
        b = 'xyz'
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.0", "2.0"),
            after_sel=("2.4", "2.4"),
            command_name="back-to-home",
        )

    #@ test_back-to-indentation
    def test_back_to_indentation(self):
        """Test case for back-to-indentation"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("4.13", "4.13"),
            after_sel=("4.8", "4.8"),
            command_name="back-to-indentation",
        )

    #@ test_back-word
    def test_back_word(self):
        """Test case for back-word"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.183", "1.183"),
            after_sel=("1.178", "1.178"),
            command_name="back-word",
        )

    #@ test_back-word-extend-selection
    def test_back_word_extend_selection(self):
        """Test case for back-word-extend-selection"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.342", "3.342"),
            after_sel=("3.332", "3.342"),
            command_name="back-word-extend-selection",
        )

    #@ test_backward-delete-char
    def test_backward_delete_char(self):
        """Test case for backward-delete-char"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first lie
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.9", "1.9"),
            after_sel=("1.8", "1.8"),
            command_name="backward-delete-char",
        )

    #@ test_backward-delete-char  (middle of line)
    def test_backward_delete_char__middle_of_line(self):
        """Test case for backward-delete-char  (middle of line)"""
        before_b = """\
    first line
    last line
    """
        after_b = """\
    firstline
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.6", "1.6"),
            after_sel=("1.5", "1.5"),
            command_name="backward-delete-char",
        )

    #@ test_backward-delete-char (last char)
    def test_backward_delete_char_last_char(self):
        """Test case for backward-delete-char (last char)"""
        before_b = """\
    first line
    last line
    """
        after_b = """\
    first line
    last lin
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.9", "2.9"),
            after_sel=("2.8", "2.8"),
            command_name="backward-delete-char",
        )

    #@ test_backward-delete-word (no selection)
    def test_backward_delete_word_no_selection(self):
        """Test case for backward-delete-word (no selection)"""
        before_b = """\
    aaaa bbbb cccc dddd
    """
        after_b = """\
    aaaa cccc dddd
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.10", "1.10"),
            after_sel=("1.5", "1.5"),
            command_name="backward-delete-word",
        )

    #@ test_backward-delete-word (selection)
    def test_backward_delete_word_selection(self):
        """Test case for backward-delete-word (selection)"""
        before_b = """\
    aaaa bbbb cccc dddd
    """
        after_b = """\
    aaaa bbcc dddd
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.7", "1.12"),
            after_sel=("1.7", "1.7"),
            command_name="backward-delete-word",
        )

    #@ test_backward-kill-paragraph
    def test_backward_kill_paragraph(self):
        """Test case for backward-kill-paragraph"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year,
    Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000
    tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly
    weather impacts every American. Communities can now rely on the National Weather
    Service’s StormReady program to help them guard against the ravages of Mother
    Nature.

    Some 90% of all presidentially declared disasters are weather related, leading
    to around 500 deaths per year and nearly $14 billion in damage. StormReady, a
    program started in 1999 in Tulsa, OK, helps arm America's communities with the
    communication and safety skills needed to save lives and property– before and
    during the event. StormReady helps community leaders and emergency managers
    strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of
    severe weather through better planning, education, and awareness. No community
    is storm proof, but StormReady can help communities save lives. Does StormReady
    make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year,
    Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000
    tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly
    weather impacts every American. Communities can now rely on the National Weather
    Service’s StormReady program to help them guard against the ravages of Mother
    Nature.
    to around 500 deaths per year and nearly $14 billion in damage. StormReady, a
    program started in 1999 in Tulsa, OK, helps arm America's communities with the
    communication and safety skills needed to save lives and property– before and
    during the event. StormReady helps community leaders and emergency managers
    strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of
    severe weather through better planning, education, and awareness. No community
    is storm proof, but StormReady can help communities save lives. Does StormReady
    make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("9.0", "9.0"),
            after_sel=("7.0", "7.0"),
            command_name="backward-kill-paragraph",
        )

    #@ test_backward-kill-sentence
    def test_backward_kill_sentence(self):
        """Test case for backward-kill-sentence"""
        before_b = """\
    This is the first sentence.  This
    is the second sentence.  And
    this is the last sentence.
    """
        after_b = """\
    This is the first sentence.  This
    is the second sentence.
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.2", "3.2"),
            after_sel=("2.23", "2.23"),
            command_name="backward-kill-sentence",
        )

    #@ test_backward-kill-word
    def test_backward_kill_word(self):
        """Test case for backward-kill-word"""
        before_b = """\
    This is the first sentence.  This
    is the second sentence.  And
    this is the last sentence.
    """
        after_b = """\
    This is the first sentence.  This
    is the second sentence.  And
    this  the last sentence.
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.7", "3.7"),
            after_sel=("3.5", "3.5"),
            command_name="backward-kill-word",
        )

    #@ test_beginning-of-buffer
    def test_beginning_of_buffer(self):
        """Test case for beginning-of-buffer"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("5.56", "5.56"),
            after_sel=("1.0", "1.0"),
            command_name="beginning-of-buffer",
        )

    #@ test_beginning-of-buffer-extend-selection
    def test_beginning_of_buffer_extend_selection(self):
        """Test case for beginning-of-buffer-extend-selection"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.423", "3.423"),
            after_sel=("1.0", "3.423"),
            command_name="beginning-of-buffer-extend-selection",
        )

    #@ test_beginning-of-line
    def test_beginning_of_line(self):
        """Test case for beginning-of-line"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.10", "3.10"),
            after_sel=("3.0", "3.0"),
            command_name="beginning-of-line",
        )

    #@ test_beginning-of-line-extend-selection
    def test_beginning_of_line_extend_selection(self):
        """Test case for beginning-of-line-extend-selection"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("4.10", "4.10"),
            after_sel=("4.0", "4.10"),
            command_name="beginning-of-line-extend-selection",
        )

    #@< Commands C-E
    #@> test_capitalize-word
    def test_capitalize_word(self):
        """Test case for capitalize-word"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        Line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.6", "3.6"),
            after_sel=("3.6", "3.6"),
            command_name="capitalize-word",
        )

    #@ test_center-line
    def test_center_line(self):
        """Test case for center-line"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related,
    leading to around 500 deaths per year and nearly $14 billion in damage.
    StormReady, a program started in 1999 in Tulsa, OK,
    helps arm America's communities with the communication and safety
    skills needed to save lives and property– before and during the event.
    StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related,
    leading to around 500 deaths per year and nearly $14 billion in damage.
    StormReady, a program started in 1999 in Tulsa, OK,
    helps arm America's communities with the communication and safety
    skills needed to save lives and property– before and during the event.
    StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.0", "9.0"),
            after_sel=("3.0", "9.0"),
            command_name="center-line",
        )

    #@ test_center-region
    def test_center_region(self):
        """Test case for center-region"""
        before_b = """\
    Some 90% of all presidentially declared disasters are weather related,
    leading to around 500 deaths per year and nearly $14 billion in damage.
    StormReady, a program started in 1999 in Tulsa, OK,
    helps arm America's communities with the communication and safety
    skills needed to save lives and property– before and during the event.
    StormReady helps community leaders and emergency managers strengthen local safety programs.
    """
        after_b = """\
    Some 90% of all presidentially declared disasters are weather related,
    leading to around 500 deaths per year and nearly $14 billion in damage.
             StormReady, a program started in 1999 in Tulsa, OK,
      helps arm America's communities with the communication and safety
    skills needed to save lives and property– before and during the event.
    StormReady helps community leaders and emergency managers strengthen local safety programs.
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "7.0"),
            after_sel=("1.0", "7.0"),
            command_name="center-region",
            directives="@pagewidth 70",
        )

    #@ test_clean-lines
    def test_clean_lines(self):
        """Test case for clean-lines"""
        before_b = self.prep(
            """
            # Should remove all trailing whitespace.

            a = 2

                b = 3
                c  = 4
            d = 5
            e = 6
            x
        """
        )
        after_b = before_b
        # Add some trailing ws to before_b
        i = 1 + before_b.find('3')
        before_b = before_b[:i] + '  ' + before_b[i:]
        self.assertNotEqual(before_b, after_b)
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "1.0"),
            after_sel=("1.0", "1.0"),
            command_name="clean-lines",
        )

    #@ test_clear-selected-text
    def test_clear_selected_text(self):
        """Test case for clear-selected-text"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line    line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.4", "4.4"),
            after_sel=("2.4", "2.4"),
            command_name="clear-selected-text",
        )

    #@ test_count-region
    def test_count_region(self):
        """Test case for count-region"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.4", "4.8"),
            after_sel=("2.4", "4.8"),
            command_name="count-region",
        )

    #@ test_delete-char
    def test_delete_char(self):
        """Test case for delete-char"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    firstline
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.5", "1.5"),
            after_sel=("1.5", "1.5"),
            command_name="delete-char",
        )

    #@ test_delete-indentation
    def test_delete_indentation(self):
        """Test case for delete-indentation"""
        before_b = """\
    first line
        line 1
    last line
    """
        after_b = """\
    first line
    line 1
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.8", "2.8"),
            after_sel=("2.4", "2.4"),
            command_name="delete-indentation",
        )

    #@ test_delete-spaces
    def test_delete_spaces(self):
        """Test case for delete-spaces"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
    line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.2", "3.2"),
            after_sel=("3.0", "3.0"),
            command_name="delete-spaces",
        )

    #@ test_do-nothing
    def test_do_nothing(self):
        """Test case for do-nothing"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "1.0"),
            after_sel=("1.0", "1.0"),
            command_name="do-nothing",
        )

    #@ test_downcase-region
    def test_downcase_region(self):
        """Test case for downcase-region"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. stormready, a program started in 1999 in tulsa, ok, helps arm america's communities with the communication and safety skills needed to save lives and property– before and during the event. stormready helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.0", "4.0"),
            after_sel=("3.0", "4.0"),
            command_name="downcase-region",
        )

    #@ test_downcase-word
    def test_downcase_word(self):
        """Test case for downcase-word"""
        before_b = """\
    XYZZY line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    xyzzy line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.4", "1.4"),
            after_sel=("1.4", "1.4"),
            command_name="downcase-word",
        )

    #@ test_end-of-buffer
    def test_end_of_buffer(self):
        """Test case for end-of-buffer"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.3", "1.3"),
            after_sel=("7.0", "7.0"),
            command_name="end-of-buffer",
        )

    #@ test_end-of-buffer-extend-selection
    def test_end_of_buffer_extend_selection(self):
        """Test case for end-of-buffer-extend-selection"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "1.0"),
            after_sel=("1.0", "7.0"),
            command_name="end-of-buffer-extend-selection",
        )

    #@ test_end-of-line
    def test_end_of_line(self):
        """Test case for end-of-line"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "1.0"),
            after_sel=("1.10", "1.10"),
            command_name="end-of-line",
        )

    #@ test_end-of-line (blank last line)
    def test_end_of_line_blank_last_line(self):
        """Test case for end-of-line (blank last line)"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last non-blank line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last non-blank line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("7.0", "7.0"),
            after_sel=("7.0", "7.0"),
            command_name="end-of-line",
        )

    #@ test_end-of-line (internal blank line)
    def test_end_of_line_internal_blank_line(self):
        """Test case for end-of-line (internal blank line)"""
        before_b = """\
    first line

    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line

    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.0", "2.0"),
            after_sel=("2.0", "2.0"),
            command_name="end-of-line",
        )

    #@ test_end-of-line (single char last line)
    def test_end_of_line_single_char_last_line(self):
        """Test case for end-of-line (single char last line)"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last non-blank line

    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last non-blank line

    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("7.0", "7.0"),
            after_sel=("7.1", "7.1"),
            command_name="end-of-line",
        )

    #@ test_end-of-line 2
    def test_end_of_line_2(self):
        """Test case for end-of-line 2"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("6.0", "6.0"),
            after_sel=("6.9", "6.9"),
            command_name="end-of-line",
        )

    #@ test_end-of-line-extend-selection
    def test_end_of_line_extend_selection(self):
        """Test case for end-of-line-extend-selection"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.0", "3.0"),
            after_sel=("3.0", "3.10"),
            command_name="end-of-line-extend-selection",
        )

    #@ test_end-of-line-extend-selection (blank last line)
    def test_end_of_line_extend_selection_blank_last_line(self):
        """Test case for end-of-line-extend-selection (blank last line)"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last non-blank line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last non-blank line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("7.0", "7.0"),
            after_sel=("7.0", "7.0"),
            command_name="end-of-line-extend-selection",
        )

    #@ test_exchange-point-mark
    def test_exchange_point_mark(self):
        """Test case for exchange-point-mark"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "1.10"),
            after_sel=("1.0", "1.10"),
            command_name="exchange-point-mark",
        )

    #@ test_extend-to-line
    def test_extend_to_line(self):
        """Test case for extend-to-line"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.3", "3.3"),
            after_sel=("3.0", "3.10"),
            command_name="extend-to-line",
        )

    #@ test_extend-to-paragraph
    def test_extend_to_paragraph(self):
        """Test case for extend-to-paragraph"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year,
    Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000
    tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly
    weather impacts every American. Communities can now rely on the National Weather
    Service’s StormReady program to help them guard against the ravages of Mother
    Nature.

    Some 90% of all presidentially declared disasters are weather related, leading
    to around 500 deaths per year and nearly $14 billion in damage. StormReady, a
    program started in 1999 in Tulsa, OK, helps arm America's communities with the
    communication and safety skills needed to save lives and property– before and
    during the event. StormReady helps community leaders and emergency managers
    strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of
    severe weather through better planning, education, and awareness. No community
    is storm proof, but StormReady can help communities save lives. Does StormReady
    make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year,
    Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000
    tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly
    weather impacts every American. Communities can now rely on the National Weather
    Service’s StormReady program to help them guard against the ravages of Mother
    Nature.

    Some 90% of all presidentially declared disasters are weather related, leading
    to around 500 deaths per year and nearly $14 billion in damage. StormReady, a
    program started in 1999 in Tulsa, OK, helps arm America's communities with the
    communication and safety skills needed to save lives and property– before and
    during the event. StormReady helps community leaders and emergency managers
    strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of
    severe weather through better planning, education, and awareness. No community
    is storm proof, but StormReady can help communities save lives. Does StormReady
    make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("9.0", "9.0"),
            after_sel=("8.0", "13.33"),
            command_name="extend-to-paragraph",
        )

    #@ test_extend-to-sentence
    def test_extend_to_sentence(self):
        """Test case for extend-to-sentence"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.5", "3.5"),
            after_sel=("1.395", "3.142"),
            command_name="extend-to-sentence",
        )

    #@ test_extend-to-word
    def test_extend_to_word(self):
        """Test case for extend-to-word"""
        before_b = """\
    first line
    line 1
        line_24a a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line_24a a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.10", "3.10"),
            after_sel=("3.4", "3.12"),
            command_name="extend-to-word",
        )

    #@< Commands F-L
    #@> test_fill-paragraph
    def test_fill_paragraph(self):
        """Test case for fill-paragraph"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Services StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially
    declared disasters are weather related,
    leading to around 500 deaths per year
    and nearly $14 billion in damage.
    StormReady, a program
    started in 1999 in Tulsa, OK,
    helps arm America's
    communities with the communication and
    safety skills needed to save lives and
    property--before and during the event.
    StormReady helps community leaders and
    emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Services StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading
    to around 500 deaths per year and nearly $14 billion in damage. StormReady, a
    program started in 1999 in Tulsa, OK, helps arm America's communities with the
    communication and safety skills needed to save lives and property--before and
    during the event. StormReady helps community leaders and emergency managers
    strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.0", "3.7"),
            after_sel=("10.0", " 10.0"),
            command_name="fill-paragraph",
            directives="@pagewidth 80",
        )

    #@ test_finish-of-line
    def test_finish_of_line(self):
        """Test case for finish-of-line"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.12", "3.12"),
            after_sel=("3.9", "3.9"),
            command_name="finish-of-line",
        )

    #@ test_finish-of-line (2)
    def test_finish_of_line_2(self):
        """Test case for finish-of-line (2)"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.1", "3.1"),
            after_sel=("3.9", "3.9"),
            command_name="finish-of-line",
        )

    #@ test_finish-of-line-extend-selection
    def test_finish_of_line_extend_selection(self):
        """Test case for finish-of-line-extend-selection"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.1", "3.1"),
            after_sel=("3.1", "3.9"),
            command_name="finish-of-line-extend-selection",
        )

    #@ test_forward-char
    def test_forward_char(self):
        """Test case for forward-char"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.2", "1.2"),
            after_sel=("1.3", "1.3"),
            command_name="forward-char",
        )

    #@ test_forward-char-extend-selection
    def test_forward_char_extend_selection(self):
        """Test case for forward-char-extend-selection"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.1", "1.1"),
            after_sel=("1.1", "1.2"),
            command_name="forward-char-extend-selection",
        )

    #@ test_forward-end-word (end of line)
    def test_forward_end_word_end_of_line(self):
        """Test case for forward-end-word (end of line)"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.395", "1.395"),
            after_sel=("3.4", "3.4"),
            command_name="forward-end-word",
        )

    #@ test_forward-end-word (start of word)
    def test_forward_end_word_start_of_word(self):
        """Test case for forward-end-word (start of word)"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.310", "1.310"),
            after_sel=("1.317", "1.317"),
            command_name="forward-end-word",
        )

    #@ test_forward-end-word-extend-selection
    def test_forward_end_word_extend_selection(self):
        """Test case for forward-end-word-extend-selection"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.20", "3.20"),
            after_sel=("3.20", "3.30"),
            command_name="forward-end-word-extend-selection",
        )

    #@ test_forward-paragraph
    def test_forward_paragraph(self):
        """Test case for forward-paragraph"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year,
    Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000
    tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly
    weather impacts every American. Communities can now rely on the National Weather
    Service’s StormReady program to help them guard against the ravages of Mother
    Nature.

    Some 90% of all presidentially declared disasters are weather related, leading
    to around 500 deaths per year and nearly $14 billion in damage. StormReady, a
    program started in 1999 in Tulsa, OK, helps arm America's communities with the
    communication and safety skills needed to save lives and property– before and
    during the event. StormReady helps community leaders and emergency managers
    strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of
    severe weather through better planning, education, and awareness. No community
    is storm proof, but StormReady can help communities save lives. Does StormReady
    make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year,
    Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000
    tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly
    weather impacts every American. Communities can now rely on the National Weather
    Service’s StormReady program to help them guard against the ravages of Mother
    Nature.

    Some 90% of all presidentially declared disasters are weather related, leading
    to around 500 deaths per year and nearly $14 billion in damage. StormReady, a
    program started in 1999 in Tulsa, OK, helps arm America's communities with the
    communication and safety skills needed to save lives and property– before and
    during the event. StormReady helps community leaders and emergency managers
    strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of
    severe weather through better planning, education, and awareness. No community
    is storm proof, but StormReady can help communities save lives. Does StormReady
    make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("9.0", "9.0"),
            after_sel=("15.0", "15.0"),
            command_name="forward-paragraph",
        )

    #@ test_forward-paragraph-extend-selection
    def test_forward_paragraph_extend_selection(self):
        """Test case for forward-paragraph-extend-selection"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year,
    Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000
    tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly
    weather impacts every American. Communities can now rely on the National Weather
    Service’s StormReady program to help them guard against the ravages of Mother
    Nature.

    Some 90% of all presidentially declared disasters are weather related, leading
    to around 500 deaths per year and nearly $14 billion in damage. StormReady, a
    program started in 1999 in Tulsa, OK, helps arm America's communities with the
    communication and safety skills needed to save lives and property– before and
    during the event. StormReady helps community leaders and emergency managers
    strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of
    severe weather through better planning, education, and awareness. No community
    is storm proof, but StormReady can help communities save lives. Does StormReady
    make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year,
    Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000
    tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly
    weather impacts every American. Communities can now rely on the National Weather
    Service’s StormReady program to help them guard against the ravages of Mother
    Nature.

    Some 90% of all presidentially declared disasters are weather related, leading
    to around 500 deaths per year and nearly $14 billion in damage. StormReady, a
    program started in 1999 in Tulsa, OK, helps arm America's communities with the
    communication and safety skills needed to save lives and property– before and
    during the event. StormReady helps community leaders and emergency managers
    strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of
    severe weather through better planning, education, and awareness. No community
    is storm proof, but StormReady can help communities save lives. Does StormReady
    make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("10.0", "10.0"),
            after_sel=("10.0", "15.0"),
            command_name="forward-paragraph-extend-selection",
        )

    #@ test_forward-sentence
    def test_forward_sentence(self):
        """Test case for forward-sentence"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.17", "3.17"),
            after_sel=("3.142", "3.142"),
            command_name="forward-sentence",
        )

    #@ test_forward-sentence-extend-selection
    def test_forward_sentence_extend_selection(self):
        """Test case for forward-sentence-extend-selection"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.264", "1.264"),
            after_sel=("1.264", "1.395"),
            command_name="forward-sentence-extend-selection",
        )

    #@ test_forward-word
    def test_forward_word(self):
        """Test case for forward-word"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.261", "1.261"),
            after_sel=("1.272", "1.272"),
            command_name="forward-word",
        )

    #@ test_forward-word-extend-selection
    def test_forward_word_extend_selection(self):
        """Test case for forward-word-extend-selection"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.395", "1.395"),
            after_sel=("1.395", "3.4"),
            command_name="forward-word-extend-selection",
        )

    #@ test_indent-relative
    def test_indent_relative(self):
        """Test case for indent-relative"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
            line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("5.0", "5.0"),
            after_sel=("5.8", "5.8"),
            command_name="indent-relative",
        )

    #@ test_indent-rigidly
    def test_indent_rigidly(self):
        """Test case for indent-rigidly"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    TABline 1
    TAB    line a
    TAB        line b
    TABline c
    last line
    """.replace('TAB', '\t')
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.0", "5.0"),
            after_sel=("2.0", "5.1"),
            command_name="indent-rigidly",
        )

    #@ test_indent-to-comment-column
    def test_indent_to_comment_column(self):
        """Test case for indent-to-comment-column"""
        before_b = """\
    first line
    line b
    last line
    """
        after_b = """\
    first line
        line b
    last line
    """
        self.c.editCommands.ccolumn = 4  # Set the comment column
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.0", "2.0"),
            after_sel=("2.4", "2.4"),
            command_name="indent-to-comment-column",
        )

    #@ test_insert-newline
    def test_insert_newline(self):
        """Test case for insert-newline"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first li
    ne
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.8", "1.8"),
            after_sel=("2.0", "2.0"),
            command_name="insert-newline",
        )

    #@ test_insert-newline-bug-2230
    def test_insert_newline_bug_2230(self):
        """Test case for insert-newline"""
        before_b = self.prep("""
    #@@language python
            def spam():
                if 1:  # test
            # after line
        """)

        # There are 8 spaces in the line after "if 1:..."
        after_b = self.prep(
            """
    #@@language python
            def spam():
                if 1:  # test

            # after line
        """
        )
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.18", "3.18"),
            after_sel=("4.8", "4.8"),
            command_name="insert-newline",
        )

    #@ test_insert-parentheses
    def test_insert_parentheses(self):
        """Test case for insert-parentheses"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first() line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.5", "1.5"),
            after_sel=("1.6", "1.6"),
            command_name="insert-parentheses",
        )

    #@ test_kill-line end-body-text
    def test_kill_line_end_body_text(self):
        """Test case for kill-line end-body-text"""
        before_b = """\
    line 1
    line 2
    line 3
    """
        after_b = """\
    line 1
    line 2
    line 3"""
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("4.1", "4.1"),
            after_sel=("3.6", "3.6"),
            command_name="kill-line",
        )

    #@ test_kill-line end-line-text
    def test_kill_line_end_line_text(self):
        """Test case for kill-line end-line-text"""
        before_b = """\
    line 1
    line 2
    line 3
    """
        after_b = """\
    line 1
    line 2

    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.5", "3.5"),
            after_sel=("3.0", "3.0"),
            command_name="kill-line",
        )

    #@ test_kill-line start-blank-line
    def test_kill_line_start_blank_line(self):
        """Test case for kill-line start-blank-line"""
        before_b = """\
    line 1
    line 2

    line 4
    """
        after_b = """\
    line 1
    line 2
    line 4
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.0", "3.0"),
            after_sel=("3.0", "3.0"),
            command_name="kill-line",
        )

    #@ test_kill-line start-line
    def test_kill_line_start_line(self):
        """Test case for kill-line start-line"""
        before_b = """\
    line 1
    line 2
    line 3
    line 4
    """
        after_b = """\
    line 1
    line 2

    line 4
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.0", "3.0"),
            after_sel=("3.0", "3.0"),
            command_name="kill-line",
        )

    #@ test_kill-paragraph
    def test_kill_paragraph(self):
        """Test case for kill-paragraph"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year,
    Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000
    tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly
    weather impacts every American. Communities can now rely on the National Weather
    Service’s StormReady program to help them guard against the ravages of Mother
    Nature.

    Some 90% of all presidentially declared disasters are weather related, leading
    to around 500 deaths per year and nearly $14 billion in damage. StormReady, a
    program started in 1999 in Tulsa, OK, helps arm America's communities with the
    communication and safety skills needed to save lives and property– before and
    during the event. StormReady helps community leaders and emergency managers
    strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of
    severe weather through better planning, education, and awareness. No community
    is storm proof, but StormReady can help communities save lives. Does StormReady
    make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year,
    Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000
    tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly
    weather impacts every American. Communities can now rely on the National Weather
    Service’s StormReady program to help them guard against the ravages of Mother
    Nature.



    StormReady communities are better prepared to save lives from the onslaught of
    severe weather through better planning, education, and awareness. No community
    is storm proof, but StormReady can help communities save lives. Does StormReady
    make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("9.0", "9.0"),
            after_sel=("8.0", "8.0"),
            command_name="kill-paragraph",
        )

    #@ test_kill-sentence
    def test_kill_sentence(self):
        """Test case for kill-sentence"""
        before_b = """\
    This is the first sentence.  This
    is the second sentence.  And
    this is the last sentence.
    """
        after_b = """\
    This is the first sentence.  And
    this is the last sentence.
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.2", "2.2"),
            after_sel=("1.27", "1.27"),
            command_name="kill-sentence",
        )

    #@ test_kill-to-end-of-line after last visible char
    def test_kill_to_end_of_line_after_last_visible_char(self):
        """Test case for kill-to-end-of-line after last visible char"""
        before_b = """\
    line 1
    # The next line contains two trailing blanks.
    line 3
    line 4
    """
        after_b = """\
    line 1
    # The next line contains two trailing blanks.
    line 3line 4
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.6", "3.6"),
            after_sel=("3.6", "3.6"),
            command_name="kill-to-end-of-line",
        )

    #@ test_kill-to-end-of-line end-body-text
    def test_kill_to_end_of_line_end_body_text(self):
        """Test case for kill-to-end-of-line end-body-text"""
        before_b = """\
    line 1
    line 2
    line 3
    """
        after_b = """\
    line 1
    line 2
    line 3"""
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("4.1", "4.1"),
            after_sel=("3.6", "3.6"),
            command_name="kill-to-end-of-line",
        )

    #@ test_kill-to-end-of-line end-line
    def test_kill_to_end_of_line_end_line(self):
        """Test case for kill-to-end-of-line end-line"""
        before_b = """\
    line 1
    line 2
    line 3
    """
        after_b = """\
    line 1
    line 2line 3
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.6", "2.6"),
            after_sel=("2.6", "2.6"),
            command_name="kill-to-end-of-line",
        )

    #@ test_kill-to-end-of-line middle-line
    def test_kill_to_end_of_line_middle_line(self):
        """Test case for kill-to-end-of-line middle-line"""
        before_b = """\
    line 1
    line 2
    line 3
    """
        after_b = """\
    line 1
    li
    line 3
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.2", "2.2"),
            after_sel=("2.2", "2.2"),
            command_name="kill-to-end-of-line",
        )

    #@ test_kill-to-end-of-line start-blank-line
    def test_kill_to_end_of_line_start_blank_line(self):
        """Test case for kill-to-end-of-line start-blank-line"""
        before_b = """\
    line 1
    line 2

    line 4
    """
        after_b = """\
    line 1
    line 2
    line 4
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.0", "3.0"),
            after_sel=("3.0", "3.0"),
            command_name="kill-to-end-of-line",
        )

    #@ test_kill-to-end-of-line start-line
    def test_kill_to_end_of_line_start_line(self):
        """Test case for kill-to-end-of-line start-line"""
        before_b = """\
    line 1
    line 2
    line 3
    line 4
    """
        after_b = """\
    line 1
    line 2

    line 4
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.0", "3.0"),
            after_sel=("3.0", "3.0"),
            command_name="kill-to-end-of-line",
        )

    #@ test_kill-word
    def test_kill_word(self):
        """Test case for kill-word"""
        before_b = """\
    This is the first sentence.  This
    is the second sentence.  And
    this is the last sentence.
    """
        after_b = """\
    This is the first sentence.  This
    is the  sentence.  And
    this is the last sentence.
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.6", "2.6"),
            after_sel=("2.7", "2.7"),
            command_name="kill-word",
        )

    #@< Commands M-R
    #@> test_merge-node-with-next-node
    def test_merge_node_with_next_node(self):
        c, u = self.c, self.c.undoer
        prev_b = self.prep(
            """
            def spam():
                pass
        """
        )

        next_b = self.prep("""spam2 = spam""")

        result_b = self.prep(
            """
            def spam():
                pass

            spam2 = spam
        """
        )
        self.before_p.b = prev_b
        self.after_p.b = next_b
        c.selectPosition(self.before_p)
        # Delete 'before', select 'after'
        c.doCommandByName('merge-node-with-next-node')
        self.assertEqual(c.p.h, 'after')
        self.assertEqual(c.p.b, result_b)
        self.assertFalse(c.p.next())
        # Restore 'before', select, 'before'.
        u.undo()
        self.assertEqual(c.p.h, 'before')
        self.assertEqual(c.p.b, prev_b)
        self.assertEqual(c.p.next().h, 'after')
        self.assertEqual(c.p.next().b, next_b)
        u.redo()
        self.assertEqual(c.p.h, 'after')
        self.assertEqual(c.p.b, result_b)
        self.assertFalse(c.p.next())

    #@ test_merge-node-with-prev-node
    def test_merge_node_with_prev_node(self):
        c, u = self.c, self.c.undoer
        prev_b = self.prep(
            """
            def spam():
                pass
        """
        )

        next_b = self.prep(
            """
            spam2 = spam
        """
        )

        result_b = self.prep(
            """
            def spam():
                pass

            spam2 = spam
        """
        )
        self.before_p.b = prev_b
        self.after_p.b = next_b
        c.selectPosition(self.after_p)
        # Delete 'after', select 'before'
        c.doCommandByName('merge-node-with-prev-node')
        self.assertEqual(c.p.h, 'before')
        self.assertEqual(c.p.b, result_b)
        self.assertFalse(c.p.next())
        # Restore 'after', select, 'after'.
        u.undo()
        self.assertEqual(c.p.h, 'after')
        self.assertEqual(c.p.b, next_b)
        self.assertEqual(c.p.back().h, 'before')
        self.assertEqual(c.p.back().b, prev_b)
        u.redo()
        self.assertEqual(c.p.h, 'before')
        self.assertEqual(c.p.b, result_b)
        self.assertFalse(c.p.next())

    #@ test_move-lines-down
    def test_move_lines_down(self):
        """Test case for move-lines-down"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
    line c
        line a
            line b
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.3", "4.3"),
            after_sel=("4.3", "5.3"),
            command_name="move-lines-down",
        )

    #@ test_move-lines-up
    def test_move_lines_up(self):
        """Test case for move-lines-up"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    line 1
    first line
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.2", "2.2"),
            after_sel=("1.2", "1.2"),
            command_name="move-lines-up",
        )

    #@ test_move-lines-up (into docstring)
    def test_move_lines_up_into_docstring(self):
        """Test case for move-lines-up (into docstring)"""
        before_b = '''\
    #@@language python
    def test():
        """ a
        b
        c
        """
        print 1

        print 2
    '''
        after_b = '''\
    #@@language python
    def test():
        """ a
        b
        c
        print 1
        """

        print 2
    '''
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("7.1", "7.1"),
            after_sel=("6.1", "6.1"),
            command_name="move-lines-up",
        )

    #@ test_move-past-close
    def test_move_past_close(self):
        """Test case for move-past-close"""
        before_b = """\
    first (line)
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first (line)
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.10", "1.10"),
            after_sel=("1.12", "1.12"),
            command_name="move-past-close",
        )

    #@ test_move-past-close-extend-selection
    def test_move_past_close_extend_selection(self):
        """Test case for move-past-close-extend-selection"""
        before_b = """\
    first line
    line 1
        (line )a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        (line )a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.7", "3.7"),
            after_sel=("3.7", "3.11"),
            command_name="move-past-close-extend-selection",
        )

    #@ test_newline-and-indent
    def test_newline_and_indent(self):
        """Test case for newline-and-indent"""
        before_b = self.prep(
            """
            first line
            line 1
                line a
                    line b
            line c
            last line
        """
        )

        # docstrings strip blank lines, so we can't use a docstring here!
        after_b = ''.join(
            [
                'first line\nline 1\n    \n',  # Would be stripped in a docstring!
                '    line a\n        line b\nline c\nlast line\n',
            ]
        )
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.6", "2.6"),
            after_sel=("3.4", "3.4"),
            command_name="newline-and-indent",
            dedent=False,
        )

    #@ test_next-line
    def test_next_line(self):
        """Test case for next-line"""
        before_b = """\
    a

    b
    """
        after_b = """\
    a

    b
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.1", "1.1"),
            after_sel=("2.0", "2.0"),
            command_name="next-line",
        )

    #@ test_previous-line
    def test_previous_line(self):
        """Test case for previous-line"""
        before_b = """\
    a

    b
    """
        after_b = """\
    a

    b
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.0", "3.0"),
            after_sel=("2.0", "2.0"),
            command_name="previous-line",
        )

    #@ test_rectangle-clear
    def test_rectangle_clear(self):
        """Test case for rectangle-clear"""
        before_b = """\
    before
    aaaxxxbbb
    aaaxxxbbb
    aaaxxxbbb
    aaaxxxbbb
    after
    """
        after_b = """\
    before
    aaa   bbb
    aaa   bbb
    aaa   bbb
    aaa   bbb
    after
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.3", "5.6"),
            after_sel=("2.3", "5.6"),
            command_name="rectangle-clear",
        )

    #@ test_rectangle-close
    def test_rectangle_close(self):
        """Test case for rectangle-close"""
        before_b = """\
    before
    aaa   bbb
    aaa   bbb
    aaa   bbb
    aaa   bbb
    after
    """
        after_b = """\
    before
    aaabbb
    aaabbb
    aaabbb
    aaabbb
    after
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.3", "5.6"),
            after_sel=("2.3", "5.3"),
            command_name="rectangle-close",
        )

    #@ test_rectangle-delete
    def test_rectangle_delete(self):
        """Test case for rectangle-delete"""
        before_b = """\
    before
    aaaxxxbbb
    aaaxxxbbb
    aaaxxxbbb
    aaaxxxbbb
    after
    """
        after_b = """\
    before
    aaabbb
    aaabbb
    aaabbb
    aaabbb
    after
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.3", "5.6"),
            after_sel=("2.3", "5.3"),
            command_name="rectangle-delete",
        )

    #@ test_rectangle-kill
    def test_rectangle_kill(self):
        """Test case for rectangle-kill"""
        before_b = """\
    before
    aaaxxxbbb
    aaaxxxbbb
    aaaxxxbbb
    aaaxxxbbb
    after
    """
        after_b = """\
    before
    aaabbb
    aaabbb
    aaabbb
    aaabbb
    after
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.3", "5.6"),
            after_sel=("5.3", "5.3"),
            command_name="rectangle-kill",
        )

    #@ test_rectangle-open
    def test_rectangle_open(self):
        """Test case for rectangle-open"""
        before_b = """\
    before
    aaaxxxbbb
    aaaxxxbbb
    aaaxxxbbb
    aaaxxxbbb
    after
    """
        after_b = """\
    before
    aaa   xxxbbb
    aaa   xxxbbb
    aaa   xxxbbb
    aaa   xxxbbb
    after
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.3", "5.6"),
            after_sel=("2.3", "5.6"),
            command_name="rectangle-open",
        )

    #@ test_test_rectangle-string
    def test_rectangle_string(self):
        """Test case for rectangle-string"""
        before_b = self.prep(
            """
            before
            aaaxxxbbb
            aaaxxxbbb
            aaaxxxbbb
            aaaxxxbbb
            after
        """
        )
        after_b = self.prep(
            """
            before
            aaas...sbbb
            aaas...sbbb
            aaas...sbbb
            aaas...sbbb
            after
        """
        )

        # A hack. The command tests for g.unitTesting!
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.3", "5.6"),
            after_sel=("2.3", "5.8"),
            command_name="rectangle-string",
        )

    #@ test_test_rectangle-yank
    def test_rectangle_yank(self):
        """Test case for rectangle-yank"""
        before_b = self.prep(
            """
            before
            aaaxxxbbb
            aaaxxxbbb
            aaaxxxbbb
            aaaxxxbbb
            after
        """
        )

        after_b = self.prep(
            """
            before
            aaaY1Ybbb
            aaaY2Ybbb
            aaaY3Ybbb
            aaaY4Ybbb
            after
        """
        )

        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.3", "5.6"),
            after_sel=("2.3", "5.6"),
            command_name="rectangle-yank",
        )

    #@ test_reformat-paragraph list 1 of 5
    def test_reformat_paragraph_list_1_of_5(self):
        """Test case for reformat-paragraph list 1 of 5"""
        before_b = """\
    This paragraph leads of this test.  It is the "lead"
    paragraph.

      1. This is item
         number 1.  It is the first item in the list.

      2. This is item
         number 2.  It is the second item in the list.

      3. This is item
         number 3.  It is the third item in the list.

    This paragraph ends the test.  It is the "final"
    paragraph.
    """
        after_b = """\
    This paragraph leads of this test. It is
    the "lead" paragraph.

      1. This is item
         number 1.  It is the first item in the list.

      2. This is item
         number 2.  It is the second item in the list.

      3. This is item
         number 3.  It is the third item in the list.

    This paragraph ends the test.  It is the "final"
    paragraph.
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "1.0"),
            after_sel=("4.0", "4.0"),
            command_name="reformat-paragraph",
            directives="@language plain\n@pagewidth 40\n@tabwidth 8",
        )

    #@ test_reformat-paragraph list 2 of 5
    def test_reformat_paragraph_list_2_of_5(self):
        """Test case for reformat-paragraph list 2 of 5"""
        before_b = """\
    This paragraph leads of this test. It is
    the "lead" paragraph.

      1. This is item number 1. It is the
         first item in the list.

      2. This is item
         number 2.  It is the second item in the list.

      3. This is item
         number 3.  It is the third item in the list.

    This paragraph ends the test.  It is the "final"
    paragraph.
    """
        after_b = """\
    This paragraph leads of this test. It is
    the "lead" paragraph.

      1. This is item number 1. It is the
         first item in the list.

      2. This is item
         number 2.  It is the second item in the list.

      3. This is item
         number 3.  It is the third item in the list.

    This paragraph ends the test.  It is the "final"
    paragraph.
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("4.0", "4.0"),
            after_sel=("7.0", "7.0"),
            command_name="reformat-paragraph",
            directives="@language plain\n@pagewidth 40\n@tabwidth 8",
        )

    #@ test_reformat-paragraph list 3 of 5
    def test_reformat_paragraph_list_3_of_5(self):
        """Test case for reformat-paragraph list 3 of 5"""
        before_b = """\
    This paragraph leads of this test. It is
    the "lead" paragraph.

      1. This is item number 1. It is the
         first item in the list.

      2. This is item
         number 2.  It is the second item in the list.

      3. This is item
         number 3.  It is the third item in the list.

    This paragraph ends the test.  It is the "final"
    paragraph.
    """
        after_b = """\
    This paragraph leads of this test. It is
    the "lead" paragraph.

      1. This is item number 1. It is the
         first item in the list.

      2. This is item number 2. It is the
         second item in the list.

      3. This is item
         number 3.  It is the third item in the list.

    This paragraph ends the test.  It is the "final"
    paragraph.
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("7.0", "7.0"),
            after_sel=("10.0", "10.0"),
            command_name="reformat-paragraph",
            directives="@language plain\n@pagewidth 40\n@tabwidth 8",
        )

    #@ test_reformat-paragraph list 4 of 5
    def test_reformat_paragraph_list_4_of_5(self):
        """Test case for reformat-paragraph list 4 of 5"""
        before_b = """\
    This paragraph leads of this test. It is
    the "lead" paragraph.

      1. This is item number 1. It is the
         first item in the list.

      2. This is item number 2. It is the
         second item in the list.

      3. This is item
         number 3.  It is the third item in the list.

    This paragraph ends the test.  It is the "final"
    paragraph.
    """
        after_b = """\
    This paragraph leads of this test. It is
    the "lead" paragraph.

      1. This is item number 1. It is the
         first item in the list.

      2. This is item number 2. It is the
         second item in the list.

      3. This is item number 3. It is the
         third item in the list.

    This paragraph ends the test.  It is the "final"
    paragraph.
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("10.0", "10.0"),
            after_sel=("13.0", "13.0"),
            command_name="reformat-paragraph",
            directives="@language plain\n@pagewidth 40\n@tabwidth 8",
        )

    #@ test_reformat-paragraph list 5 of 5
    def test_reformat_paragraph_list_5_of_5(self):
        """Test case for reformat-paragraph list 5 of 5"""
        before_b = """\
    This paragraph leads of this test. It is
    the "lead" paragraph.

      1. This is item number 1. It is the
         first item in the list.

      2. This is item number 2. It is the
         second item in the list.

      3. This is item number 3. It is the
         third item in the list.

    This paragraph ends the test.  It is the "final"
    paragraph.
    """
        after_b = """\
    This paragraph leads of this test. It is
    the "lead" paragraph.

      1. This is item number 1. It is the
         first item in the list.

      2. This is item number 2. It is the
         second item in the list.

      3. This is item number 3. It is the
         third item in the list.

    This paragraph ends the test. It is the
    "final" paragraph.
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("13.0", "13.0"),
            after_sel=("15.1", "15.1"),
            command_name="reformat-paragraph",
            directives="@language plain\n@pagewidth 40\n@tabwidth 8",
        )

    #@ test_reformat-paragraph new code 1 of 8
    def test_reformat_paragraph_new_code_1_of_8(self):
        """Test case for reformat-paragraph new code 1 of 8"""
        before_b = """\
    #@@pagewidth 40
    '''
    docstring.
    '''
    """
        after_b = """\
    #@@pagewidth 40
    '''
    docstring.
    '''
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "1.0"),
            after_sel=("2.0", "2.0"),
            command_name="reformat-paragraph",
            directives="@language plain\n@pagewidth 40\n@tabwidth 8",
        )

    #@ test_reformat-paragraph new code 2 of 8
    def test_reformat_paragraph_new_code_2_of_8(self):
        """Test case for reformat-paragraph new code 2 of 8"""
        before_b = """\
    #@@pagewidth 40
    '''
    docstring.
    '''
    """
        after_b = """\
    #@@pagewidth 40
    '''
    docstring.
    '''
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.0", "2.0"),
            after_sel=("3.0", "3.0"),
            command_name="reformat-paragraph",
            directives="@language plain\n@pagewidth 40\n@tabwidth 8",
        )

    #@ test_reformat-paragraph new code 3 of 8
    def test_reformat_paragraph_new_code_3_of_8(self):
        """Test case for reformat-paragraph new code 3 of 8"""
        before_b = """\
    #@@pagewidth 40
    '''
    docstring.
    more docstring.
    '''
    """
        after_b = """\
    #@@pagewidth 40
    '''
    docstring. more docstring.
    '''
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.1", "4.1"),
            after_sel=("4.0", "4.0"),
            command_name="reformat-paragraph",
            directives="@language plain\n@pagewidth 40\n@tabwidth 8",
        )

    #@ test_reformat-paragraph new code 4 of 8
    def test_reformat_paragraph_new_code_4_of_8(self):
        """Test case for reformat-paragraph new code 4 of 8"""
        before_b = """\
    - Point 1. xxxxxxxxxxxxxxxxxxxxxxxxxxxx
    Line 11.
    A. Point 2. xxxxxxxxxxxxxxxxxxxxxxxxxxx
    """
        after_b = """\
    - Point 1. xxxxxxxxxxxxxxxxxxxxxxxxxxxx
      Line 11.
    A. Point 2. xxxxxxxxxxxxxxxxxxxxxxxxxxx
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "1.0"),
            after_sel=("3.0", "3.0"),
            command_name="reformat-paragraph",
            directives="@language plain\n@pagewidth 40\n@tabwidth 8",
        )

    #@ test_reformat-paragraph new code 5 of 8
    def test_reformat_paragraph_new_code_5_of_8(self):
        """Test case for reformat-paragraph new code 5 of 8"""
        before_b = """\
    A. Point 2. xxxxxxxxxxxxxxxxxxxxxxxxxxx
      Line 22.
    1. Point 3. xxxxxxxxxxxxxxxxxxxxxxxxxxx
    """
        after_b = """\
    A. Point 2. xxxxxxxxxxxxxxxxxxxxxxxxxxx
       Line 22.
    1. Point 3. xxxxxxxxxxxxxxxxxxxxxxxxxxx
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "2.0"),
            after_sel=("3.0", "3.0"),
            command_name="reformat-paragraph",
            directives="@language plain\n@pagewidth 40\n@tabwidth 8",
        )

    #@ test_reformat-paragraph new code 6 of 8
    def test_reformat_paragraph_new_code_6_of_8(self):
        """Test case for reformat-paragraph new code 6 of 8"""
        before_b = """\
    1. Point 3. xxxxxxxxxxxxxxxxxxxxxxxxxxx
    Line 32.

    2. Point 4  xxxxxxxxxxxxxxxxxxxxxxxxxxx
    """
        after_b = """\
    1. Point 3. xxxxxxxxxxxxxxxxxxxxxxxxxxx
       Line 32.

    2. Point 4  xxxxxxxxxxxxxxxxxxxxxxxxxxx
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "1.0"),
            after_sel=("4.0", "4.0"),
            command_name="reformat-paragraph",
            directives="@language plain\n@pagewidth 40\n@tabwidth 8",
        )

    #@ test_reformat-paragraph new code 7 of 8
    def test_reformat_paragraph_new_code_7_of_8(self):
        """Test case for reformat-paragraph new code 7 of 8"""
        before_b = """\
    1. Point 3. xxxxxxxxxxxxxxxxxxxxxxxxxxx
       Line 32.

    2. Point 4 xxxxxxxxxxxxxxxxxxxxxxxxxxx
            Line 41.
    """
        after_b = """\
    1. Point 3. xxxxxxxxxxxxxxxxxxxxxxxxxxx
       Line 32.

    2. Point 4 xxxxxxxxxxxxxxxxxxxxxxxxxxx
            Line 41.
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.11", "2.11"),
            after_sel=("3.1", "3.1"),
            command_name="reformat-paragraph",
            directives="@language plain\n@pagewidth 40\n@tabwidth 8",
        )

    #@ test_reformat-paragraph new code 8 of 8
    def test_reformat_paragraph_new_code_8_of_8(self):
        """Test case for reformat-paragraph new code 8 of 8"""
        before_b = """\
    2. Point 4 xxxxxxxxxxxxxxxxxxxxxxxxxxx
            Line 41.
    """
        after_b = """\
    2. Point 4 xxxxxxxxxxxxxxxxxxxxxxxxxxx
            Line 41.
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "1.0"),
            after_sel=("3.0", "3.0"),
            command_name="reformat-paragraph",
            directives="@language plain\n@pagewidth 40\n@tabwidth 8",
        )

    #@ test_reformat-paragraph paragraph 1 of 3
    def test_reformat_paragraph_paragraph_1_of_3(self):
        """Test case for reformat-paragraph paragraph 1 of 3"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?

    Last paragraph.
    """
        after_b = """\
    Americans live in the most severe
    weather-prone country on Earth. Each
    year, Americans cope with an average of
    10,000 thunderstorms, 2,500 floods,
    1,000 tornadoes, as well as an average
    of 6 deadly hurricanes. Potentially
    deadly weather impacts every American.
    Communities can now rely on the National
    Weather Service’s StormReady program to
    help them guard against the ravages of
    Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?

    Last paragraph.
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "1.0"),
            after_sel=("13.0", "13.0"),
            command_name="reformat-paragraph",
            directives="@language plain\n@pagewidth 40\n@tabwidth 8",
        )

    #@ test_reformat-paragraph paragraph 2 of 3
    def test_reformat_paragraph_paragraph_2_of_3(self):
        """Test case for reformat-paragraph paragraph 2 of 3"""
        before_b = """\
    Americans live in the most severe
    weather-prone country on Earth. Each
    year, Americans cope with an average of
    10,000 thunderstorms, 2,500 floods,
    1,000 tornadoes, as well as an average
    of 6 deadly hurricanes. Potentially
    deadly weather impacts every American.
    Communities can now rely on the National
    Weather Service’s StormReady program to
    help them guard against the ravages of
    Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?

    Last paragraph.
    """
        after_b = """\
    Americans live in the most severe
    weather-prone country on Earth. Each
    year, Americans cope with an average of
    10,000 thunderstorms, 2,500 floods,
    1,000 tornadoes, as well as an average
    of 6 deadly hurricanes. Potentially
    deadly weather impacts every American.
    Communities can now rely on the National
    Weather Service’s StormReady program to
    help them guard against the ravages of
    Mother Nature.

    Some 90% of all presidentially declared
    disasters are weather related, leading
    to around 500 deaths per year and nearly
    $14 billion in damage. StormReady, a
    program started in 1999 in Tulsa, OK,
    helps arm America's communities with the
    communication and safety skills needed
    to save lives and property– before and
    during the event. StormReady helps
    community leaders and emergency managers
    strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?

    Last paragraph.
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("13.0", "13.0"),
            after_sel=("25.0", "25.0"),
            command_name="reformat-paragraph",
            directives="@language plain\n@pagewidth 40\n@tabwidth 8",
        )

    #@ test_reformat-paragraph paragraph 3 of 3
    def test_reformat_paragraph_paragraph_3_of_3(self):
        """Test case for reformat-paragraph paragraph 3 of 3"""
        before_b = """\
    Americans live in the most severe
    weather-prone country on Earth. Each
    year, Americans cope with an average of
    10,000 thunderstorms, 2,500 floods,
    1,000 tornadoes, as well as an average
    of 6 deadly hurricanes. Potentially
    deadly weather impacts every American.
    Communities can now rely on the National
    Weather Service’s StormReady program to
    help them guard against the ravages of
    Mother Nature.

    Some 90% of all presidentially declared
    disasters are weather related, leading
    to around 500 deaths per year and nearly
    $14 billion in damage. StormReady, a
    program started in 1999 in Tulsa, OK,
    helps arm America's communities with the
    communication and safety skills needed
    to save lives and property– before and
    during the event. StormReady helps
    community leaders and emergency managers
    strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?

    Last paragraph.
    """
        after_b = """\
    Americans live in the most severe
    weather-prone country on Earth. Each
    year, Americans cope with an average of
    10,000 thunderstorms, 2,500 floods,
    1,000 tornadoes, as well as an average
    of 6 deadly hurricanes. Potentially
    deadly weather impacts every American.
    Communities can now rely on the National
    Weather Service’s StormReady program to
    help them guard against the ravages of
    Mother Nature.

    Some 90% of all presidentially declared
    disasters are weather related, leading
    to around 500 deaths per year and nearly
    $14 billion in damage. StormReady, a
    program started in 1999 in Tulsa, OK,
    helps arm America's communities with the
    communication and safety skills needed
    to save lives and property– before and
    during the event. StormReady helps
    community leaders and emergency managers
    strengthen local safety programs.

    StormReady communities are better
    prepared to save lives from the
    onslaught of severe weather through
    better planning, education, and
    awareness. No community is storm proof,
    but StormReady can help communities save
    lives. Does StormReady make a
    difference?

    Last paragraph.
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("25.10", "25.10"),
            after_sel=("34.0", "34.0"),
            command_name="reformat-paragraph",
            directives="@language plain\n@pagewidth 40\n@tabwidth 8",
        )

    #@ test_reformat-paragraph simple hanging indent
    def test_reformat_paragraph_simple_hanging_indent(self):
        """Test case for reformat-paragraph simple hanging indent"""
        before_b = """\
    Honor this line that has a hanging indentation, please.  Hanging
      indentation is valuable for lists of all kinds.  But it is tricky to get right.

    Next paragraph.
    """
        after_b = """\
    Honor this line that has a hanging
      indentation, please. Hanging
      indentation is valuable for lists of
      all kinds. But it is tricky to get
      right.

    Next paragraph.
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "1.0"),
            after_sel=("7.0", "7.0"),
            command_name="reformat-paragraph",
            directives="@language plain\n@pagewidth 40\n@tabwidth 8",
        )

    #@ test_reformat-paragraph simple hanging indent 2
    def test_reformat_paragraph_simple_hanging_indent_2(self):
        """Test case for reformat-paragraph simple hanging indent 2"""
        before_b = """\
    Honor this line that has
      a hanging indentation, please.  Hanging
        indentation is valuable for lists of all kinds.  But it is tricky to get right.

    Next paragraph.
    """
        after_b = """\
    Honor this line that has a hanging
      indentation, please. Hanging
      indentation is valuable for lists of
      all kinds. But it is tricky to get
      right.

    Next paragraph.
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.0", "2.0"),
            after_sel=("7.0", "7.0"),
            command_name="reformat-paragraph",
            directives="@language plain\n@pagewidth 40\n@tabwidth 8",
        )

    #@ test_reformat-paragraph simple hanging indent 3
    def test_reformat_paragraph_simple_hanging_indent_3(self):
        """Test case for reformat-paragraph simple hanging indent 3"""
        before_b = """\
    Honor this line that
      has a hanging indentation,
      please.  Hanging
       indentation is valuable
        for lists of all kinds.  But
        it is tricky to get right.

    Next Paragraph.
    """
        after_b = """\
    Honor this line that has a hanging
      indentation, please. Hanging
      indentation is valuable for lists of
      all kinds. But it is tricky to get
      right.

    Next Paragraph.
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "1.0"),
            after_sel=("7.0", "7.0"),
            command_name="reformat-paragraph",
            directives="@language plain\n@pagewidth 40\n@tabwidth 8",
        )

    #@ test_remove-blank-lines
    def test_remove_blank_lines(self):
        """Test case for remove-blank-lines"""
        before_b = """\
    first line

    line 1
        line a
            line b

    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "9.0"),
            after_sel=("1.0", "6.9"),
            command_name="remove-blank-lines",
        )

    #@ test_remove-space-from-lines
    def test_remove_space_from_lines(self):
        """Test case for remove-space-from-lines"""
        before_b = """\
    first line

    line 1
        line a
            line b

    line c
    last line
    """
        after_b = """\
    first line

    line 1
       line a
           line b

    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "9.0"),
            after_sel=("1.0", "9.0"),
            command_name="remove-space-from-lines",
        )

    #@ test_remove-tab-from-lines
    def test_remove_tab_from_lines(self):
        """Test case for remove-tab-from-lines"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
    line a
        line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "7.0"),
            after_sel=("1.0", "7.0"),
            command_name="remove-tab-from-lines",
        )

    #@ test_reverse-region
    def test_reverse_region(self):
        """Test case for reverse-region"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\

    last line
    line c
            line b
        line a
    line 1
    first line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "7.0"),
            after_sel=("7.10", "7.10"),
            command_name="reverse-region",
        )

    #@ test_reverse-sort-lines
    def test_reverse_sort_lines(self):
        """Test case for reverse-sort-lines"""
        before_b = """\
    a
    d
    e
    z
    x
    """
        after_b = """\
    z
    x
    e
    d
    a
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "5.1"),
            after_sel=("1.0", "5.1"),
            command_name="reverse-sort-lines",
        )

    #@ test_reverse-sort-lines-ignoring-case
    def test_reverse_sort_lines_ignoring_case(self):
        """Test case for reverse-sort-lines-ignoring-case"""
        before_b = """\
    c
    A
    z
    X
    Y
    b
    """
        after_b = """\
    z
    Y
    X
    c
    b
    A
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "6.1"),
            after_sel=("1.0", "6.1"),
            command_name="reverse-sort-lines-ignoring-case",
        )

    #@< Commands S-Z
    #@> test_sort-columns
    def test_sort_columns(self):
        """Test case for sort-columns"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
            line b
        line a
    first line
    last line
    line 1
    line c
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "6.2"),
            after_sel=("1.0", "7.0"),
            command_name="sort-columns",
        )

    #@ test_sort-lines
    def test_sort_lines(self):
        """Test case for sort-lines"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
            line b
        line a
    line 1
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.0", "5.6"),
            after_sel=("2.0", "5.6"),
            command_name="sort-lines",
        )

    #@ test_sort-lines-ignoring-case
    def test_sort_lines_ignoring_case(self):
        """Test case for sort-lines-ignoring-case"""
        before_b = """\
    x
    z
    A
    c
    B
    """
        after_b = """\
    A
    B
    c
    x
    z
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "5.1"),
            after_sel=("1.0", "5.1"),
            command_name="sort-lines-ignoring-case",
        )

    #@ test_split-line
    def test_split_line(self):
        """Test case for split-line"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first
     line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.5", "1.5"),
            after_sel=("2.0", "2.0"),
            command_name="split-line",
        )

    #@ test_start-of-line
    def test_start_of_line(self):
        """Test case for start-of-line"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.10", "3.10"),
            after_sel=("3.4", "3.4"),
            command_name="start-of-line",
        )

    #@ test_start-of-line (2)
    def test_start_of_line_2(self):
        """Test case for start-of-line (2)"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.1", "3.1"),
            after_sel=("3.4", "3.4"),
            command_name="start-of-line",
        )

    #@ test_start-of-line-extend-selection
    def test_start_of_line_extend_selection(self):
        """Test case for start-of-line-extend-selection"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.10", "3.10"),
            after_sel=("3.4", "3.10"),
            command_name="start-of-line-extend-selection",
        )

    #@ test_start-of-line-extend-selection (2)
    def test_start_of_line_extend_selection_2(self):
        """Test case for start-of-line-extend-selection (2)"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.1", "3.1"),
            after_sel=("3.1", "3.4"),
            command_name="start-of-line-extend-selection",
        )

    #@ test_tabify
    def test_tabify(self):
        """Test case for tabify"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
    TABline a
    TABTABline b
    line c
    last line
    """.replace('TAB', '\t')
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "7.0"),
            after_sel=("7.0", "7.0"),
            command_name="tabify",
        )

    #@ test_transpose-chars
    def test_transpose_chars(self):
        """Test case for transpose-chars"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    frist line
    line 1
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.2", "1.2"),
            after_sel=("1.2", "1.2"),
            command_name="transpose-chars",
        )

    #@ test_transpose-lines
    def test_transpose_lines(self):
        """Test case for transpose-lines"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    line 1
    first line
        line a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.2", "2.2"),
            after_sel=("2.10", "2.10"),
            command_name="transpose-lines",
        )

    #@ test_transpose-words
    def test_transpose_words(self):
        """Test case for transpose-words"""
        before_b = """\
    first line
    before bar2 += foo after
    last line
    """
        after_b = """\
    first line
    before foo += bar2 after
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("2.9", "2.9"),
            after_sel=("2.11", "2.11"),
            command_name="transpose-words",
        )

    #@ test_untabify
    def test_untabify(self):
        """Test case for untabify"""
        before_b = """\
    first line
    line 1
    TABline a
    TABTABline b
    line c
    last line
    """.replace('TAB', '\t')
        after_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """.replace('TAB', '\t')
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("1.0", "7.0"),
            after_sel=("7.0", "7.0"),
            command_name="untabify",
        )

    #@ test_upcase-region
    def test_upcase_region(self):
        """Test case for upcase-region"""
        before_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    Some 90% of all presidentially declared disasters are weather related, leading to around 500 deaths per year and nearly $14 billion in damage. StormReady, a program started in 1999 in Tulsa, OK, helps arm America's communities with the communication and safety skills needed to save lives and property– before and during the event. StormReady helps community leaders and emergency managers strengthen local safety programs.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        after_b = """\
    Americans live in the most severe weather-prone country on Earth. Each year, Americans cope with an average of 10,000 thunderstorms, 2,500 floods, 1,000 tornadoes, as well as an average of 6 deadly hurricanes. Potentially deadly weather impacts every American. Communities can now rely on the National Weather Service’s StormReady program to help them guard against the ravages of Mother Nature.

    SOME 90% OF ALL PRESIDENTIALLY DECLARED DISASTERS ARE WEATHER RELATED, LEADING TO AROUND 500 DEATHS PER YEAR AND NEARLY $14 BILLION IN DAMAGE. STORMREADY, A PROGRAM STARTED IN 1999 IN TULSA, OK, HELPS ARM AMERICA'S COMMUNITIES WITH THE COMMUNICATION AND SAFETY SKILLS NEEDED TO SAVE LIVES AND PROPERTY– BEFORE AND DURING THE EVENT. STORMREADY HELPS COMMUNITY LEADERS AND EMERGENCY MANAGERS STRENGTHEN LOCAL SAFETY PROGRAMS.

    StormReady communities are better prepared to save lives from the onslaught of severe weather through better planning, education, and awareness. No community is storm proof, but StormReady can help communities save lives. Does StormReady make a difference?
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.0", "4.0"),
            after_sel=("3.0", "4.0"),
            command_name="upcase-region",
        )

    #@ test_upcase-word
    def test_upcase_word(self):
        """Test case for upcase-word"""
        before_b = """\
    first line
    line 1
        line a
            line b
    line c
    last line
    """
        after_b = """\
    first line
    line 1
        LINE a
            line b
    line c
    last line
    """
        self.run_test(
            before_b=before_b,
            after_b=after_b,
            before_sel=("3.7", "3.7"),
            after_sel=("3.7", "3.7"),
            command_name="upcase-word",
        )

    #@<2 TestEditCommands: Others
    #@> test_capitalizeHelper
    def test_capitalizeHelper(self):
        c, w = self.c, self.c.frame.body.wrapper
        w.setAllText('# TARGETWORD\n')
        table = (
            ('cap', 'Targetword'),
            ('low', 'targetword'),
            ('up',  'TARGETWORD'),
        )  # fmt: skip
        for which, result in table:
            w.setInsertPoint(5)  # Must be inside the target.
            event = LeoKeyEvent(c, w=w)  # Leo 6.8.9.
            c.editCommands.capitalizeHelper(event=event, which=which, undoType='X')
            s = w.getAllText()
            word = s[2:12]
            self.assertEqual(word, result, msg=which)
            i = w.getInsertPoint()
            self.assertEqual(i, 5, msg=which)

    #@ test_delete_key_sticks_in_body
    def test_delete_key_sticks_in_body(self):
        c = self.c
        w = c.frame.body.wrapper
        h = 'Test headline abc'
        p = c.rootPosition().insertAfter()
        p.h = h
        c.selectPosition(p)
        s = 'ABC'
        c.setBodyString(p, s)
        c.bodyWantsFocus()
        w.setInsertPoint(2)
        c.outerUpdate()  # This fixed the problem.
        event = LeoKeyEvent(c, w=w)  # Leo 6.8.9.
        c.doCommandByName('delete-char', event)
        self.assertEqual(p.b, s[:-1])
        c.selectPosition(p.threadBack())
        c.selectPosition(p)
        self.assertEqual(p.b, s[:-1])

    #@ test_delete_key_sticks_in_headline
    def test_delete_key_sticks_in_headline(self):
        c = self.c
        h = 'Test headline abc'
        p = c.rootPosition().insertAfter()
        p.h = h
        c.selectPosition(p)
        c.redraw(p)  # To make node visible
        c.frame.tree.editLabel(p)
        w = c.headline_wrapper(p)
        try:
            assert w
            end = w.getLastIndex()
            w.setSelectionRange(end, end)
        finally:
            if 1:
                c.setHeadString(p, h)  # Essential
                c.redraw(p)

    #@ test_dynamicExpandHelper
    def test_dynamicExpandHelper(self):
        c = self.c
        # A totally wimpy test.
        # And it somehow prints a newline to the console.
        if 0:
            c.abbrevCommands.dynamicExpandHelper(event=None, prefix='', aList=[], w=None)

    #@ test_extendHelper
    def test_extendHelper(self):
        c = self.c
        ec = c.editCommands
        w = c.frame.body.wrapper
        for i, j, python in (
            # ('1.0','4.5',False),
            (5, 50, True),
        ):
            extend = True
            ec.moveSpot = None  # It's hard to init this properly.
            ec.extendHelper(w, extend, j)
            i2, j2 = w.getSelectionRange()

    #@ test_findWord
    def test_findWord(self):
        c = self.c
        ec, k, w = c.editCommands, c.k, c.frame.body.wrapper
        w.setAllText('start\ntargetWord\n')
        w.setInsertPoint(0)
        k.arg = 't'  # 'targetWord'
        ec.w = w
        ec.oneLineFlag = False
        ec.findWord1(event=None)
        i, j = w.getSelectionRange()
        self.assertEqual(i, 6)

    #@ test_findWordInLine
    def test_findWordInLine(self):
        c = self.c
        ec, k, w = c.editCommands, c.k, c.frame.body.wrapper
        w.setAllText('abc\ntargetWord\n')
        k.arg = 't'  # 'targetWord'
        w.setInsertPoint(0)
        ec.w = w
        ec.oneLineFlag = False
        ec.findWord1(event=None)
        i, j = w.getSelectionRange()
        self.assertEqual(i, 4)

    #@ test_helpForMinibuffer
    def test_helpForMinibuffer(self):
        c = self.c
        c.helpCommands.helpForMinibuffer()

    #@ test_helpForPython
    def test_helpForPthon(self):
        c, k = self.c, self.c.k
        k.arg = 'os'
        s = c.helpCommands.pythonHelp1(event=None)
        self.assertTrue('Help on module os' in s)

    #@ test_insert_node_before_node_can_be_undone_and_redone
    def test_insert_node_before_node_can_be_undone_and_redone(self):
        c = self.c
        u = c.undoer
        assert u
        c.insertHeadlineBefore()
        self.assertEqual(u.undoMenuLabel, 'Undo Insert Node Before')
        c.undoer.undo()
        self.assertEqual(u.redoMenuLabel, 'Redo Insert Node Before')

    #@ test_insert_node_can_be_undone_and_redone
    def test_insert_node_can_be_undone_and_redone(self):
        c = self.c
        u = c.undoer
        assert u
        c.insertHeadline()
        self.assertEqual(u.undoMenuLabel, 'Undo Insert Node')
        c.undoer.undo()
        self.assertEqual(u.redoMenuLabel, 'Redo Insert Node')

    #@ test_inserting_a_new_node_draws_the_screen_exactly_once
    def test_inserting_a_new_node_draws_the_screen_exactly_once(self):
        c = self.c
        n = c.frame.tree.redrawCount
        c.insertHeadline()
        c.outerUpdate()  # Not actually needed, but should not matter.
        n2 = c.frame.tree.redrawCount
        self.assertEqual(n2, n + 1)

    #@ test_most_toggle_commands
    def test_most_toggle_commands(self):
        c, k = self.c, self.c.k
        ed = c.editCommands
        # These don't set ivars
        # 'toggle-active-pane'),
        # 'toggle-angle-brackets',
        # 'toggle-input-state'),
        # 'toggle-mini-buffer'),
        # 'toggle-split-direction'),
        table = [
            (k, 'abbrevOn', 'toggle-abbrev-mode'),
            (ed, 'extendMode', 'toggle-extend-mode'),
        ]
        for obj, ivar, command in table:
            val1 = getattr(obj, ivar)
            k.simulateCommand(command)
            val2 = getattr(obj, ivar)
            self.assertEqual(val2, not val1, msg=command)
            k.simulateCommand(command)
            val3 = getattr(obj, ivar)
            self.assertEqual(val3, val1, msg=command)

    #@ test_moveToHelper
    def test_moveToHelper(self):
        c = self.c
        ec = c.editCommands
        w = c.frame.body.wrapper
        for i, j, python in (
            # ('1.0','4.5',False),
            (5, 50, True),
        ):
            event = LeoKeyEvent(c, w=w)  # Leo 6.8.9.
            extend = True
            ec.moveSpot = None
            w.setInsertPoint(i)
            ec.moveToHelper(event, j, extend)
            i2, j2 = w.getSelectionRange()
            self.assertEqual(i, i2)
            self.assertEqual(j, j2)
            w.setSelectionRange(0, 0, insert=None)

    #@ test_moveUpOrDownHelper
    def test_moveUpOrDownHelper(self):
        c = self.c
        ec = c.editCommands
        w = c.frame.body.wrapper

        def toInt(index: str) -> int:
            return g.toPythonIndex(w.getAllText(), index)

        table = (
            ('5.8', '4.8', 'up'),
            ('5.8', '6.8', 'down'),
        )
        for i, result, direction in table:
            w.setInsertPoint(toInt(i))
            ec.moveUpOrDownHelper(event=None, direction=direction, extend=False)
            w.getSelectionRange()

    #@ test_paste_and_undo_in_headline__at_end
    def test_paste_and_undo_in_headline__at_end(self):
        c, k = self.c, self.c.k
        h = 'Test headline abc'
        p = c.rootPosition().insertAfter()
        p.h = h
        c.selectPosition(p)
        c.frame.tree.editLabel(p)
        w = c.headline_wrapper(p)
        assert w
        end = w.getLastIndex()
        w.setSelectionRange(end, end)
        paste = 'ABC'
        g.app.gui.replaceClipboardWith(paste)
        w.setSelectionRange(end, end)
        c.frame.pasteText(event=g.app.gui.create_key_event(c, w=w))
        g.app.gui.event_generate(c, '\n', 'Return', w)
        self.assertEqual(p.h, h + paste)
        k.manufactureKeyPressForCommandName(w, 'undo')
        self.assertEqual(p.h, h)

    #@ test_paste_and_undo_in_headline__with_selection
    def test_paste_and_undo_in_headline__with_selection(self):
        c, k = self.c, self.c.k
        h = 'Test headline abc'
        p = c.rootPosition().insertAfter()
        p.h = h
        c.selectPosition(p)
        c.frame.tree.editLabel(p)
        w = c.headline_wrapper(p)
        assert w
        paste = 'ABC'
        g.app.gui.replaceClipboardWith(paste)
        w.setSelectionRange(1, 2)
        c.frame.pasteText(event=g.app.gui.create_key_event(c, w=w))
        g.app.gui.event_generate(c, '\n', 'Return', w)
        self.assertEqual(p.h, h[0] + paste + h[2:])
        k.manufactureKeyPressForCommandName(w, 'undo')
        self.assertEqual(p.h, h)

    #@ test_paste_at_end_of_headline
    def test_paste_at_end_of_headline(self):
        c = self.c
        h = 'Test headline abc'
        p = c.rootPosition().insertAfter()
        p.h = h
        c.selectPosition(p)
        c.frame.tree.editLabel(p)
        w = c.headline_wrapper(p)
        assert w
        end = w.getLastIndex()
        g.app.gui.set_focus(c, w)
        paste = 'ABC'
        g.app.gui.replaceClipboardWith(paste)
        g.app.gui.set_focus(c, w)
        w.setSelectionRange(end, end)
        c.frame.pasteText(event=g.app.gui.create_key_event(c, w=w))
        g.app.gui.event_generate(c, '\n', 'Return', w)
        self.assertEqual(p.h, h + paste)

    #@ test_paste_from_menu_into_headline_sticks
    def test_paste_from_menu_into_headline_sticks(self):
        c = self.c
        h = 'Test headline abc'
        p = c.rootPosition().insertAfter()
        p.h = h
        c.selectPosition(p)
        c.selectPosition(p)
        c.frame.tree.editLabel(p)
        w = c.headline_wrapper(p)
        end = w.getLastIndex()
        w.setSelectionRange(end, end, insert=end)
        paste = 'ABC'
        g.app.gui.replaceClipboardWith(paste)
        c.frame.pasteText(event=g.app.gui.create_key_event(c, w=w))
        # Move around and and make sure it doesn't change.
        try:
            # g.trace('before select',w,w.getAllText())
            c.selectPosition(p.threadBack())
            self.assertEqual(p.h, h + paste)
            c.selectPosition(p)
            self.assertEqual(p.h, h + paste)
        finally:
            if 1:
                c.setHeadString(p, h)  # Essential
                c.redraw(p)

    #@ test_return_ends_editing_of_headline
    def test_return_ends_editing_of_headline(self):
        c = self.c
        h = 'test that return ends editing of headline'
        p = c.rootPosition().insertAfter()
        p.h = h
        c.selectPosition(p)
        c.redraw(p)  # To make node visible
        c.frame.tree.editLabel(p)
        w = c.headline_wrapper(p)
        wName = g.app.gui.widget_name(w)
        assert wName.startswith('head'), 'w.name:%s' % wName
        g.app.gui.event_generate(c, '\n', 'Return', w)
        c.outerUpdate()
        assert w != c.get_focus(), 'oops2: focus in headline'

    #@ test_scrollHelper
    def test_scrollHelper(self):
        c = self.c
        ec = c.editCommands
        w = c.frame.body.wrapper

        for direction in ('up', 'down'):
            for distance in ('line', 'page', 'half-page'):
                event = g.app.gui.create_key_event(c, w=w)
                ec.scrollHelper(event, direction, distance)

    #@ test_selecting_new_node_retains_paste_in_headline
    def test_selecting_new_node_retains_paste_in_headline(self):
        c = self.c
        h = 'Test headline abc'
        p = c.rootPosition().insertAfter()
        p.h = h
        c.selectPosition(p)
        c.redraw(p)  # To make node visible
        c.frame.tree.editLabel(p)
        w = c.headline_wrapper(p)
        end = w.getLastIndex()
        w.setSelectionRange(end, end)
        paste = 'ABC'
        g.app.gui.replaceClipboardWith(paste)
        w.setSelectionRange(end, end)
        c.frame.pasteText(event=g.app.gui.create_key_event(c, w=w))
        c.selectPosition(p.visBack(c))
        self.assertEqual(p.h, h + paste)
        c.undoer.undo()
        self.assertEqual(p.h, h)

    #@ test_selecting_new_node_retains_typing_in_headline
    def test_selecting_new_node_retains_typing_in_headline(self):
        c, k = self.c, self.c.k
        k.defaultUnboundKeyAction = 'insert'
        h = 'Test headline abc'
        p = c.rootPosition().insertAfter()
        p.h = h
        c.selectPosition(p)
        c.redraw(p)  # Required
        c.frame.tree.editLabel(p)
        w = c.headline_wrapper(p)
        end = w.getLastIndex()
        w.setSelectionRange(end, end)
        # char, shortcut.
        g.app.gui.event_generate(c, 'X', 'Shift+X', w)
        g.app.gui.event_generate(c, 'Y', 'Shift+Y', w)
        g.app.gui.event_generate(c, 'Z', 'Shift+Z', w)
        g.app.gui.event_generate(c, '\n', 'Return', w)
        expected = h + 'XYZ'
        self.assertEqual(p.h, expected)
        k.manufactureKeyPressForCommandName(w, 'undo')
        self.assertEqual(p.h, h)

    #@ test_setMoveCol
    def test_setMoveCol(self):
        c = self.c
        ec, w = c.editCommands, c.frame.body.wrapper
        table = (
            (0, 0),
            (5, 5),
        )
        w.setAllText('1234567890')
        for spot, result in table:
            ec.setMoveCol(w, spot)
            self.assertEqual(ec.moveSpot, result)
            self.assertEqual(ec.moveCol, result)

    #@ test_toggle_extend_mode
    def test_toggle_extend_mode(self):
        c = self.c
        # backward-find-character and find-character
        # can't be tested this way because they prompt for input.
        #@+<< define table >>
        #@> << define table >>
        # Cursor movement commands affected by extend mode.
        # The x-extend-selection commands are not so affected.
        table = (
            'back-to-indentation',
            'back-to-home',
            'back-char',
            'back-page',
            'back-paragraph',
            'back-sentence',
            'back-word',
            'beginning-of-buffer',
            'beginning-of-line',
            'end-of-buffer',
            'end-of-line',
            'forward-char',
            'forward-page',
            'forward-paragraph',
            'forward-sentence',
            'forward-end-word',
            'forward-word',
            'move-past-close',
            'next-line',
            'previous-line',
        )
        #@-<< define table >>
        w = c.frame.body.wrapper
        s = self.prep(
            """
            Paragraph 1.
                line 2.

            Paragraph 2.
            line 2, paragraph 2
        """
        )
        w.setAllText(s)
        child = c.rootPosition().insertAfter()
        c.selectPosition(child)
        for commandName in table:
            # Put the cursor in the middle of the middle line
            # so all cursor moves will actually do something.
            w.setInsertPoint(15)
            c.editCommands.extendMode = True
            c.keyHandler.simulateCommand(commandName)
            # i, j = w.getSelectionRange()
            # self.assertNotEqual(i, j, msg=commandName)

    #@< test_typing_and_undo_in_headline_at_end
    def test_typing_and_undo_in_headline_at_end(self):
        c, k = self.c, self.c.k
        k.defaultUnboundKeyAction = 'insert'
        h = 'Test headline abc'
        p = c.rootPosition().insertAfter()
        p.h = h
        c.redrawAndEdit(p)  # Required
        w = c.headline_wrapper(p)
        assert w
        end = w.getLastIndex()
        wName = g.app.gui.widget_name(w)
        self.assertTrue(wName.startswith('head'))
        w.setSelectionRange(end, end)
        g.app.gui.event_generate(c, 'X', 'Shift+X', w)
        g.app.gui.event_generate(c, 'Y', 'Shift+Y', w)
        g.app.gui.event_generate(c, 'Z', 'Shift+Z', w)
        g.app.gui.event_generate(c, '\n', 'Return', w)
        self.assertEqual(p.h, h + 'XYZ')
        self.assertEqual(c.undoer.undoMenuLabel, 'Undo Typing')
        k.manufactureKeyPressForCommandName(w, 'undo')
        self.assertEqual(c.undoer.redoMenuLabel, 'Redo Typing')
        self.assertEqual(p.h, h)

    #@ test_typing_in_non_empty_body_text_does_not_redraw_the_screen
    def test_typing_in_non_empty_body_text_does_not_redraw_the_screen(self):
        c = self.c
        w = c.frame.body.wrapper
        h = 'Test headline abc'
        p = c.rootPosition().insertAfter()
        p.h = h
        c.setBodyString(p, 'a')
        p.v.iconVal = p.computeIcon()  # To suppress redraw!
        c.redraw(p)  # To make node visible
        c.bodyWantsFocus()
        n = c.frame.tree.redrawCount
        g.app.gui.event_generate(c, 'a', 'a', w)
        n2 = c.frame.tree.redrawCount
        self.assertEqual(n2, n)

    #@ test_undoing_insert_node_restores_previous_node_s_body_text
    def test_undoing_insert_node_restores_previous_node_s_body_text(self):
        c = self.c
        h = 'Test headline abc'
        p = c.rootPosition().insertAfter()
        p.h = h
        c.selectPosition(p)
        body = 'This is a test'
        c.setBodyString(p, body)
        self.assertEqual(p.b, body)
        c.insertHeadline()
        c.undoer.undo()
        self.assertEqual(p.b, body)

    #@-others


#@-others
#@-leo
