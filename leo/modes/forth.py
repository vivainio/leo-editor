#@+leo-ver=cub-1-thin
#@0 [ekr.20150326145530.1] @f ../modes/forth.py
# Hand-written Leo colorizer control file for forth mode.
# This file is in the public domain.
#@@killbeautify
from leo.core import leoGlobals as g
#@+<< define mode rules >>
#@-<< define mode rules >>
#@+<< define mode data >>
#@-<< define mode data >>
#@+<< define extendForth class >>
#@-<< define extendForth class >>
e = extendForth()


def pre_init_mode(c):
    e.c = c
    e.init()
    e.createKeywords()
    e.createBracketRules()
    e.createDefiningWordRules()


#@-leo
