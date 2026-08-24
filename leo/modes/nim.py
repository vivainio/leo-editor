#@+leo-ver=cub-1-thin
#@0 [ekr.20240202211600.1] @f ../modes/nim.py
#@@language python
# Leo colorizer control file for nim mode.
# This file is in the public domain.

import re
import sys
from leo.core import leoGlobals as g

assert g

v1, v2, junk1, junk2, junk3 = sys.version_info

#@+<< Nim attributes dicts >>
#@> << Nim attributes dicts >>
# Properties for nim mode.
properties = {
    "indentNextLines": "\\s*[^#]{3,}:\\s*(#.*)?",
    "lineComment": "#",
}

# Attributes dict for nim_main ruleset.
nim_main_attributes_dict = {
    "default": "null",
    "digit_re": "",
    "escape": "\\",
    "highlight_digits": "true",
    "ignore_case": "false",
    "no_word_sep": "",
}

# Dictionary of attributes dictionaries for nim mode.
attributesDictDict = {
    "nim_main": nim_main_attributes_dict,
}
#@-<< Nim attributes dicts >>

# Keywords dict for nim_main ruleset.
nim_main_keywords_dict = {
    #@+<< Nim keywords >>
    #@-<< Nim keywords >>
    #@+<< Nim type names >>
    #@-<< Nim type names >>
    #@+<< Nim constants >>
    #@-<< Nim constants >>
    # https://nim-lang.org/docs/system.html
    #@+<< Nim upper-case constants >>
    #@-<< Nim upper-case constants >>
    #@+<< Nim lower-case functions >>
    #@-<< Nim lower-case functions >>
}

# Dictionary of keywords dictionaries for nim mode.
keywordsDictDict = {
    "nim_main": nim_main_keywords_dict,
}


#@+<< Nim rules >>
#@ << Nim rules >>
#@+others
#@> nim_character_literal
def nim_character_literal(colorer, s, i):
    return colorer.match_span(s, i, kind="literal1", begin="'", end="'")


#@ nim_comment (comment1)
def nim_comment(colorer, s, i):
    return colorer.match_eol_span(s, i, kind="comment1", seq="#")


#@ nim_unusual_single_quote (keyword1)
# Note: The suffix comes *before* the single quote.
lower_suffixes = [z for z in ('b,e,f,o,x,i,i8,i16,i32,i64,u,u8,u16,u32,u64').split(',')]
suffixes = tuple(lower_suffixes + [z.upper() for z in lower_suffixes])
word_pattern = re.compile(r'\b(\w+)')


def nim_unusual_single_quote(colorer, s, i):
    """
    Handle unusual single quotes, including custom_numeric_literals.

    Color all such single quotes as a keyword1.
    """

    def fail() -> int:
        # Color a prefixed "'" as a keyword.
        if i > 0 and s[i - 1] in colorer.word_chars:
            colorer.colorRangeWithTag(s, i, i + 1, tag='keyword1')
            return 1
        return 0

    # Find the suffix.
    # assert s[i : i + 1] == "'", repr(s)
    if s[i : i + 1] != "'":
        return  # TestSyntax.slow_test_all_mode_files only tests signatures.
    head = s[:i]
    for suffix in suffixes:
        if head.endswith(suffix):
            break
    else:
        return fail()  # pragma: no cover

    # Make sure the suffix is a word.
    j = i - len(suffix)
    is_word = j == 0 or j > 0 and s[j - 1] not in colorer.word_chars
    if not is_word:
        return fail()  # pragma: no cover

    # Find the preceding word.
    m = word_pattern.match(s, i + 1)
    if not m:
        return fail()  # pragma: no cover

    # Color the suffix.
    colorer.colorRangeWithTag(s, i - len(suffix), i, tag='literal1')

    # Color the single quote.
    colorer.colorRangeWithTag(s, i, i + 1, tag='keyword1')

    # Color the following word.
    word = m.group(0)
    colorer.colorRangeWithTag(s, i + 1, i + 1 + len(word), tag='literal1')
    return 1 + len(word)


#@ nim_keyword (keyword1)
def nim_keyword(colorer, s, i):
    return colorer.match_keywords(s, i)


#@ nim_multi_line_comment (comment2)
def nim_multi_line_comment(colorer, s, i):
    return colorer.match_span(s, i, kind="comment2", begin="#[", end="]#", nested=True)


#@ nim_number (do-nothing)
# Only an approximation.
# Underscores are allowed in numbers.
number_regex = re.compile(r'([0-9_]+)(b|B|d|D|f|F|i|I|u|U|x|X|32|64)*')


def nim_number(colorer, s, i):
    # return colorer.match_compiled_regexp(s, i, 'literal2', regexp=number_regex)
    return 0


#@ nim_op (do-nothing)
def nim_op(colorer, s: str, i: int) -> int:
    # Don't color ordinary ops.
    return 0


#@ nim_string (literal1)
def nim_string(colorer, s, i):
    return colorer.match_span(s, i, kind="literal1", begin="\"", end="\"")


#@ nim_triple_quote (literal2)
def nim_triple_quote(colorer, s, i):
    return colorer.match_span(s, i, kind="literal2", begin="\"\"\"", end="\"\"\"")


#@ nim_unary (do-nothing
unary_pattern = re.compile(r'(\+|\-)')


def nim_unary(colorer, s, i):
    # return colorer.match_seq_regexp(s, i, kind="keyword1", regexp=unary_pattern)
    return 0


#@-others
#@-<< Nim rules >>
#@+<< nim_rules_dict >>
#@< << nim_rules_dict >>
# Rules dict for nim_main ruleset.
nim_rules_dict = {
    '"': [nim_triple_quote, nim_string],
    "#": [nim_multi_line_comment, nim_comment],
    "'": [nim_unusual_single_quote, nim_character_literal],
    ".": [nim_number, nim_op],
    "+": [nim_unary],
    "-": [nim_unary],
    "0": [nim_number],
    "1": [nim_number],
    "2": [nim_number],
    "3": [nim_number],
    "4": [nim_number],
    "5": [nim_number],
    "6": [nim_number],
    "7": [nim_number],
    "8": [nim_number],
    "9": [nim_number],
    "A": [nim_keyword],
    "B": [nim_keyword],
    "C": [nim_keyword],
    "D": [nim_keyword],
    "E": [nim_keyword],
    "F": [nim_keyword],
    "G": [nim_keyword],
    "H": [nim_keyword],
    "I": [nim_keyword],
    "J": [nim_keyword],
    "K": [nim_keyword],
    "L": [nim_keyword],
    "M": [nim_keyword],
    "N": [nim_keyword],
    "O": [nim_keyword],
    "P": [nim_keyword],
    "Q": [nim_keyword],
    "R": [nim_keyword],
    "S": [nim_keyword],
    "T": [nim_keyword],
    "U": [nim_keyword],
    "V": [nim_keyword],
    "W": [nim_keyword],
    "X": [nim_keyword],
    "Y": [nim_keyword],
    "Z": [nim_keyword],
    "_": [nim_keyword],
    "a": [nim_keyword],
    "b": [nim_keyword],
    "c": [nim_keyword],
    "d": [nim_keyword],
    "e": [nim_keyword],
    "f": [nim_keyword],
    "g": [nim_keyword],
    "h": [nim_keyword],
    "i": [nim_keyword],
    "j": [nim_keyword],
    "k": [nim_keyword],
    "l": [nim_keyword],
    "m": [nim_keyword],
    "n": [nim_keyword],
    "o": [nim_keyword],
    "p": [nim_keyword],
    "q": [nim_keyword],
    "r": [nim_keyword],
    "s": [nim_keyword],
    "t": [nim_keyword],
    "u": [nim_keyword],
    "v": [nim_keyword],
    "w": [nim_keyword],
    "x": [nim_keyword],
    "y": [nim_keyword],
    "z": [nim_keyword],
    # The following are all do-notings.
    "!": [nim_op],
    "%": [nim_op],
    "&": [nim_op],
    "(": [nim_op],
    "*": [nim_op],
    "/": [nim_op],
    "<": [nim_op],
    "=": [nim_op],
    ">": [nim_op],
    "@": [nim_op],
    "^": [nim_op],
    "|": [nim_op],
    "~": [nim_op],
}
#@-<< nim_rules_dict >>

rulesDictDict = {
    "nim_main": nim_rules_dict,
}

# Import dict for nim mode.
importDict = {}
#@-leo
