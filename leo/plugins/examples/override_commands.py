#@+leo-ver=cub-1-thin
#@0 [edream.110203113231.919] @f ../plugins/examples/override_commands.py
"""Override the Equal Sized Pane command"""

from leo.core import leoGlobals as g


#@+others
#@> init
def init():
    """Return True if the plugin has loaded successfully."""
    ok = not g.unitTesting  # Not for unit testing: overrides core methods.
    if ok:
        # Register the handlers...
        g.registerHandler("command1", onCommand)
        g.plugin_signon(__name__)
    return ok


#@ onCommand
def onCommand(tag, keywords):
    if keywords.get("label") == "equalsizedpanes":
        g.es("over-riding Equal Sized Panes")
        return "override"  # Anything other than None overrides.
    return None


#@-others
#@@language python
#@@tabwidth -4
#@-leo
