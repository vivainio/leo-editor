#@+leo-ver=cub-1-thin
#@0 [ekr.20250330150257.1] @f ../modes/c.py
# Leo colorizer control file for c mode.
# This file is in the public domain.

import string

#@+others
#@-others

#@+<< c: properties >>
#@> << c: properties >>

# Properties for c mode.
properties = {
    "commentEnd": "*/",
    "commentStart": "/*",
    "doubleBracketIndent": "false",
    "indentCloseBrackets": "}",
    "indentNextLine": "\\s*(((if|while)\\s*\\(|else\\s*|else\\s+if\\s*\\(|for\\s*\\(.*\\))[^{;]*)",
    "indentOpenBrackets": "{",
    "lineComment": "//",
    "lineUpClosingBracket": "true",
    "wordBreakChars": ",+-=<>/?^&*",
}
#@-<< c: properties >>
#@+<< c: attributes & dict >>
#@ << c: attributes & dict >>

# Attributes dict for c_main ruleset.
c_main_attributes_dict = {
    "default": "null",
    "digit_re": "(0x[[:xdigit:]]+[lL]?|[[:digit:]]+(e[[:digit:]]*)?[lLdDfF]?)",
    "escape": "\\",
    "highlight_digits": "true",
    "ignore_case": "false",
    "no_word_sep": "",
}

# Attributes dict for c_cpp ruleset.
c_cpp_attributes_dict = {
    "default": "KEYWORD2",
    "digit_re": "(0x[[:xdigit:]]+[lL]?|[[:digit:]]+(e[[:digit:]]*)?[lLdDfF]?)",
    "escape": "\\",
    "highlight_digits": "true",
    "ignore_case": "false",
    "no_word_sep": "",
}

# Attributes dict for c_include ruleset.
c_include_attributes_dict = {
    "default": "KEYWORD2",
    "digit_re": "(0x[[:xdigit:]]+[lL]?|[[:digit:]]+(e[[:digit:]]*)?[lLdDfF]?)",
    "escape": "\\",
    "highlight_digits": "true",
    "ignore_case": "false",
    "no_word_sep": "",
}

# Dictionary of attributes dictionaries for c mode.
attributesDictDict = {
    "c_cpp": c_cpp_attributes_dict,
    "c_include": c_include_attributes_dict,
    "c_main": c_main_attributes_dict,
}
#@-<< c: attributes & dict >>
#@+<< c: keywords dict >>
#@ << c: keywords dict >>

# Keywords dict for c_main ruleset.
c_main_keywords_dict = {
    "NULL": "literal2",
    "asm": "keyword2",
    "asmlinkage": "keyword2",
    "auto": "keyword1",
    "break": "keyword1",
    "case": "keyword1",
    "char": "keyword3",
    "const": "keyword1",
    "continue": "keyword1",
    "default": "keyword1",
    "do": "keyword1",
    "double": "keyword3",
    "else": "keyword1",
    "enum": "keyword3",
    "extern": "keyword1",
    "false": "literal2",
    "far": "keyword2",
    "float": "keyword3",
    "for": "keyword1",
    "goto": "keyword1",
    "huge": "keyword2",
    "if": "keyword1",
    "inline": "keyword2",
    "int": "keyword3",
    "long": "keyword3",
    "near": "keyword2",
    "pascal": "keyword2",
    "register": "keyword1",
    "return": "keyword1",
    "short": "keyword3",
    "signed": "keyword3",
    "sizeof": "keyword1",
    "static": "keyword1",
    "struct": "keyword3",
    "switch": "keyword1",
    "true": "literal2",
    "typedef": "keyword3",
    "union": "keyword3",
    "unsigned": "keyword3",
    "void": "keyword3",
    "volatile": "keyword1",
    "while": "keyword1",
}

# Dictionary of keywords dictionaries for c mode.
keywordsDictDict = {
    ### "c_cpp": c_cpp_keywords_dict,
    ### "c_include": c_include_keywords_dict,
    "c_main": c_main_keywords_dict,
}
#@-<< c: keywords dict >>
#@+<< c: rules >>
#@ << c: rules >>
# Rules for c_main ruleset.


#@+others
#@> function: c_rule0 /**
def c_rule0(colorer, s, i):
    return colorer.match_span(
        s, i, kind="comment3", begin="/**", end="*/", delegate="doxygen::doxygen"
    )


#@ function: c_rule1 /*!
def c_rule1(colorer, s, i):
    return colorer.match_span(
        s, i, kind="comment3", begin="/*!", end="*/", delegate="doxygen::doxygen"
    )


#@ function: c_rule2 /*
def c_rule2(colorer, s, i):
    return colorer.match_span(s, i, kind="comment1", begin="/*", end="*/")


#@ function: c_rule3 "
def c_rule3(colorer, s, i):
    return colorer.match_span(s, i, kind="literal1", begin="\"", end="\"", no_line_break=True)


#@ function: c_rule4 '
def c_rule4(colorer, s, i):
    return colorer.match_span(s, i, kind="literal1", begin="'", end="'", no_line_break=True)


#@ function: c_rule5 ##
def c_rule5(colorer, s, i):
    return colorer.match_plain_seq(s, i, kind="keyword2", seq="##")


#@ function: c_rule6 #
def c_rule6(colorer, s, i):
    # #4283: Colorize the whole line.
    return colorer.match_eol_span(s, i, kind="keyword2")


#@ function: c_rule7 // comment
def c_rule7(colorer, s, i):
    return colorer.match_eol_span(s, i, kind="comment2", seq="//")


#@ rules: operators
def c_rule8(colorer, s, i):
    return colorer.match_plain_seq(s, i, kind="operator", seq="=")


def c_rule9(colorer, s, i):
    return colorer.match_plain_seq(s, i, kind="operator", seq="!")


def c_rule10(colorer, s, i):
    return colorer.match_plain_seq(s, i, kind="operator", seq=">=")


def c_rule11(colorer, s, i):
    return colorer.match_plain_seq(s, i, kind="operator", seq="<=")


def c_rule12(colorer, s, i):
    return colorer.match_plain_seq(s, i, kind="operator", seq="+")


def c_rule13(colorer, s, i):
    return colorer.match_plain_seq(s, i, kind="operator", seq="-")


def c_rule14(colorer, s, i):
    return colorer.match_plain_seq(s, i, kind="operator", seq="/")


def c_rule15(colorer, s, i):
    return colorer.match_plain_seq(s, i, kind="operator", seq="*")


def c_rule16(colorer, s, i):
    return colorer.match_plain_seq(s, i, kind="operator", seq=">")


def c_rule17(colorer, s, i):
    return colorer.match_plain_seq(s, i, kind="operator", seq="<")


def c_rule18(colorer, s, i):
    return colorer.match_plain_seq(s, i, kind="operator", seq="%")


def c_rule19(colorer, s, i):
    return colorer.match_plain_seq(s, i, kind="operator", seq="&")


def c_rule20(colorer, s, i):
    return colorer.match_plain_seq(s, i, kind="operator", seq="|")


def c_rule21(colorer, s, i):
    return colorer.match_plain_seq(s, i, kind="operator", seq="^")


def c_rule22(colorer, s, i):
    return colorer.match_plain_seq(s, i, kind="operator", seq="~")


def c_rule23(colorer, s, i):
    return colorer.match_plain_seq(s, i, kind="operator", seq="}")


def c_rule24(colorer, s, i):
    return colorer.match_plain_seq(s, i, kind="operator", seq="{")


def c_rule_at_sign(colorer, s, i):  # #4283.
    return colorer.match_plain_seq(s, i, kind="operator", seq="@")


def c_rule_semicolon(colorer, s, i):  # #4283.
    return colorer.match_plain_seq(s, i, kind="operator", seq=";")


#@ function: c_rule26 (
def c_rule26(colorer, s, i):
    return colorer.match_mark_previous(s, i, kind="function", pattern="(", exclude_match=True)


#@ function: c_keyword & label
def c_keyword(colorer, s, i):
    n = colorer.match_keywords(s, i)
    if n >= 0:
        return n
    i2 = i + abs(n)
    ch = s[i2] if i2 < len(s) else ''
    if ch != ':':
        return n

    # color the label.
    seq = s[i : i2 + 1]
    return colorer.match_seq(s, i, kind="label", seq=seq)


#@-others
#@-<< c: rules >>
#@+<< c: rules dict >>
#@< << c: rules dict >>
# Rules dict for c_main ruleset.
rulesDict1 = {
    ";": [c_rule_semicolon],  # #4283.
    "@": [c_rule_at_sign],  # #4283.
    "!": [c_rule9],
    '"': [c_rule3],
    "#": [c_rule5, c_rule6],
    "%": [c_rule18],
    "&": [c_rule19],
    "'": [c_rule4],
    "(": [c_rule26],
    "*": [c_rule15],
    "+": [c_rule12],
    "-": [c_rule13],
    "/": [c_rule0, c_rule1, c_rule2, c_rule7, c_rule14],
    "<": [c_rule11, c_rule17],
    "=": [c_rule8],
    ">": [c_rule10, c_rule16],
    "^": [c_rule21],
    "{": [c_rule24],
    "|": [c_rule20],
    "}": [c_rule23],
    "~": [c_rule22],
}

# Add *all* characters that could start a c identifier.
lead_ins = string.ascii_letters + '_'
for lead_in in lead_ins:
    aList = rulesDict1.get(lead_in, [])
    if c_keyword not in aList:
        aList.insert(0, c_keyword)
        rulesDict1[lead_in] = aList
#@-<< c: rules dict >>

# x.rulesDictDict for c mode.
rulesDictDict = {
    "c_main": rulesDict1,
}

# Import dict for c mode.
importDict = {}

#@@language python
#@@tabwidth -4
#@-leo
