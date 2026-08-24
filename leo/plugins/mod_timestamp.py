#@+leo-ver=cub-1-thin
#@0 [edream.110203113231.727] @f ../plugins/mod_timestamp.py
"""Timestamps all save operations to show when they occur."""

#@@language python
#@@tabwidth -4

# By Paul Paterson.
import time
from leo.core import leoGlobals as g


#@+others
#@> init
def init():
    """Return True if the plugin has loaded successfully."""
    g.registerHandler("command1", timestamp)
    g.plugin_signon(__name__)
    return True  # OK for unit testing.


#@ timestamp
def timestamp(tag=None, keywords=None):
    cmd = keywords.get('label', 'save')

    if cmd.startswith(("save", "tangle")):
        g.es("%s: %s" % (cmd, time.ctime()))


#@-others
#@-leo
