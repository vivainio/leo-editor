#@+leo-ver=cub-1-thin
#@0 [tom.20240923194438.1] @f ../plugins/qt_layout.py
"""The basic machinery to support applying layouts of the main Leo panels."""

#@+<< qt_layout: imports & annotations >>
#@> << qt_layout: imports & annotations >>
from __future__ import annotations

import textwrap
from collections import OrderedDict
from collections.abc import Callable
from typing import Any, TYPE_CHECKING
from leo.core.leoQt import QtWidgets, Orientation
from leo.core import leoGlobals as g

QSplitter = QtWidgets.QSplitter
QWidget = QtWidgets.QWidget

if TYPE_CHECKING:  # pragma: no cover
    from leo.core.leoCommands import Commands as Cmdr
    from leo.core.leoGui import LeoKeyEvent
#@-<< qt_layout: imports & annotations >>
#@+<< qt_layout: declarations >>
#@ << qt_layout: declarations >>
VR3_OBJ_NAME = 'viewrendered3_pane'
VR_OBJ_NAME = 'viewrendered_pane'
VRX_PLACEHOLDER_NAME = 'viewrenderedx_pane'

VR_MODULE_NAME = 'viewrendered.py'
VR3_MODULE_NAME = 'viewrendered3.py'

LAYOUT_REGISTRY: dict[str, str] = {}  # {layout_name: layout_docstring}
#@-<< qt_layout: declarations >>


#@+others
#@ Top-level functions: qt_layout.py
#@> function: init (qt_layout.py)
def init() -> bool:
    """
    qt_layout is not a true plugin, but return True just in case.
    """
    return True


#@ function: show_vr3_pane (qt_layout.py)
def show_vr3_pane(c: Cmdr, w: QWidget) -> None:
    w.setUpdatesEnabled(True)
    c.doCommandByName('vr3-show')


#@ function: is_module_loaded (qt_layout.py)
def is_module_loaded(module_name: str) -> bool:
    """Return True if the plugins controller has loaded the module."""
    controller = g.app.pluginsController
    return controller.isLoaded(module_name)


#@ decorator:  register_layout (qt_layout.py)
def register_layout(name: str) -> Callable:

    def decorator(func: Callable) -> Callable:
        # Register the function's name and docstring in the dictionary
        LAYOUT_REGISTRY[name] = func.__doc__ or ''
        return func  # Ensure the original function is returned

    return decorator


#@< Layout commands
# Read Me or Suffer
#
# The help-for-layouts and show-layout commands use these docstrings,
# so the following constraints apply to the following docstrings:
#
# 1. All docstrings must start with a newline.
# 2. Use a *single* ':', followed by a blank line
#    to denote the start of a layout diagram or
#    any other verbatim text.
# 3. All verbatim text must end with a blank line unless
#    the verbatim text ends the docstring.
#@@c
#@> command: 'layout-big-tree'
@g.command('layout-big-tree')
@register_layout('layout-big-tree')
def big_tree(event: LeoKeyEvent | None = None) -> None:
    """
    Create Leo's big-tree layout:

        ┌──────────────────┐
        │  outline         │
        ├─────────┬────────┤ <-- Main splitter
        │  body   │  log   │
        ├─────────┼────────┤
        │    VR   │  VR3   │
        └─────────┴────────┘
    """
    c = event.get('c') if event else None
    if not c:
        return
    cache = c.frame.top.layout_cache
    cache.restoreFromLayout()
    cache.layout_dict = {'name': 'big-tree'}

    has_vr3 = is_module_loaded(VR3_MODULE_NAME)

    ms = cache.find_widget('main_splitter')
    ss = cache.find_widget('secondary_splitter')
    vs = cache.find_widget('vrx_splitter')
    if vs is None:
        vs = QSplitter(cache)
        vs.setObjectName('vrx_splitter')
    of = cache.find_widget('outlineFrame')
    lf = cache.find_widget('logFrame')
    bf = cache.find_widget('bodyFrame')

    if has_vr3:
        vr3 = cache.find_widget('viewrendered3_pane')
        if vr3 is None:
            import leo.plugins.viewrendered3 as vr3_mod

            h = c.hash()
            vr3_mod.controllers[h] = vr3_mod.ViewRenderedController3(c)
    else:
        vr3 = None
    vr = c.vr

    # Clear out splitters so we can add widgets back in the right order
    for widget in (ss, of, lf, bf, vr, vr3):  # Don't remove ms!
        if widget is not None:
            widget.setParent(cache)

    # Move widgets to target splitters
    ms.addWidget(of)
    ms.addWidget(ss)
    ms.addWidget(vs)
    vs.addWidget(vr)
    if vr3 is not None:
        vs.addWidget(vr3)
    ss.addWidget(bf)
    ss.addWidget(lf)

    ms.setOrientation(Orientation.Vertical)
    ss.setOrientation(Orientation.Horizontal)
    vs.setOrientation(Orientation.Horizontal)

    ms.setSizes([100_000] * len(ms.sizes()))
    ss.setSizes([100_000] * len(ss.sizes()))
    vs.setSizes([100_000] * len(vs.sizes()))


#@ command: 'layout-legacy'
@g.command('layout-legacy')
@register_layout('layout-legacy')
def quadrants(event: LeoKeyEvent | None = None) -> None:
    """
    Create Leo's legacy layout:

        ┌───────────────┬───────────┐
        │   outline     │   log     │
        ├───────────────┼────┬──────┤ <-- Main splitter
        │   body        │ VR │ VR3  │
        └───────────────┴────┴──────┘
    """
    c = event.get('c') if event else None
    if not c:
        return
    dw = c.frame.top
    cache = dw.layout_cache
    cache.restoreFromLayout(LEGACY_LAYOUT)


#@ command: 'layout-horizontal-thirds'
@g.command('layout-horizontal-thirds')
@register_layout('layout-horizontal-thirds')
def horizontal_thirds(event: LeoKeyEvent | None = None) -> None:
    """
    Create Leo's horizontal-thirds layout:

        ┌───────────┬───────┐
        │  outline  │  log  │
        ├───────────┴───────┤ <-- Main splitter
        │  body             │
        ├─────────┬─────────┤
        │   VR    │   VR3   │
        └─────────┴─────────┘
    """
    c = event.get('c') if event else None
    if not c:
        return
    dw = c.frame.top
    cache = dw.layout_cache
    cache.restoreFromLayout(HORIZONTAL_THIRDS_LAYOUT)


#@ command: 'layout-render-focused'
@g.command('layout-render-focused')
@register_layout('layout-render-focused')
def render_focused(event: LeoKeyEvent | None = None) -> None:
    """
    Create Leo's render-focused layout:

        ┌───────────┬─────┬─────┐
        │ outline   │     │     │
        ├───────────┤     │     │
        │ body      │ VR  │ VR3 │
        ├───────────┤     │     │
        │ log       │     │     │
        └───────────┴─────┴─────┘

    Note: The expand/contract-main-splitter commands have no effect when using this layout.
    """
    c = event.get('c') if event else None
    if not c:
        return
    dw = c.frame.top
    cache = dw.layout_cache
    cache.restoreFromLayout(RENDERED_FOCUSED_LAYOUT)


#@ command: 'layout-restore-to-setting'
@g.command('layout-restore-to-setting')
@register_layout('layout-restore-to-setting')
def restoreDefaultLayout(event: LeoKeyEvent | None = None) -> None:
    """
    Select the layout specified by the `@string qt-layout-name` setting in effect
    for this outline. Use the **legacy** layout if the user's setting is erroneous.
    """
    c = event.get('c') if event else None
    if not c:
        return
    event = g.app.gui.create_key_event(c)
    layout = c.config.getString('qt-layout-name') or 'legacy'
    if not layout.startswith('layout-'):
        layout = 'layout-' + layout.strip()
    if layout not in c.commandsDict:
        g.es_print(f"Unknown layout: {layout}; Using 'legacy' layout", color='red')
        layout = 'layout-legacy'
    c.commandsDict[layout](event)


#@ command: 'layout-swap-log-panel'
@g.command('layout-swap-log-panel')
@register_layout('layout-swap-log-panel')
def swapLogPanel(event: LeoKeyEvent | None = None) -> None:
    """
    Move the Log frame between main and secondary splitters.

    **Do not use this layout as the initial layout.**
    """
    c = event.get('c') if event else None
    if not c:
        return
    gui = g.app.gui

    ms = gui.find_widget_by_name(c, 'main_splitter')
    ss = gui.find_widget_by_name(c, 'secondary_splitter')
    lf = gui.find_widget_by_name(c, 'logFrame')

    lf_parent = lf.parent()
    lf_parent_container = lf_parent.parent()
    widget = None

    if lf_parent in (ss, ms):
        # Move just the lf
        target = ms if lf_parent is ss else ss
        widget = lf
    elif lf_parent_container in (ms, ss):
        # Move lf's entire container
        target = ms if lf_parent_container is ss else ss
        widget = lf_parent
    else:
        g.es("Don't know what widget or container to swap")

    if widget is not None:
        target.addWidget(widget)
        gui.equalize_splitter(target)


#@ command: 'layout-vertical-thirds'
@g.command('layout-vertical-thirds')
@register_layout('layout-vertical-thirds')
def vertical_thirds(event: LeoKeyEvent | None = None) -> None:
    """
    Create Leo's vertical-thirds layout:

        ┌───────────┬────────┬────┬─────┐
        │  outline  │        │    │     │
        ├───────────┤  body  │ VR │ VR3 │
        │  log      │        │    │     │
        └───────────┴────────┴────┴─────┘
                    |
                    └─ Main splitter
    """
    c = event.get('c') if event else None
    if not c:
        return
    dw = c.frame.top
    cache = dw.layout_cache
    cache.restoreFromLayout(VERTICAL_THIRDS_LAYOUT)


#@ command: 'layout-vertical-thirds2'
@g.command('layout-vertical-thirds2')
@register_layout('layout-vertical-thirds2')
def vertical_thirds2(event: LeoKeyEvent | None = None) -> None:
    """
    Create Leo's vertical-thirds2 layout:

        ┌───────────┬───────┬────┬─────┐
        │           │  log  │    │     │
        │  outline  ├───────┤ VR │ VR3 │
        │           │  body │    │     │
        └───────────┴───────┴────┴─────┘
                    |
                    └─ Main splitter
    """
    c = event.get('c') if event else None
    if not c:
        return
    dw = c.frame.top
    cache = dw.layout_cache
    cache.restoreFromLayout(VERTICAL_THIRDS2_LAYOUT)


#@ command: 'show-layouts'
@g.command('layout-show-layouts')
@g.command('show-layouts')
def showLayouts(event: LeoKeyEvent | None) -> None:
    """Show all layout diagrams in the Log Frame's `layouts` tab."""
    if not event:
        return
    c = event.get('c')
    if not c:
        return

    dw = c.frame.top
    cache = dw.layout_cache
    layouts = cache.layout_registry
    listing = []
    for name, docstr in layouts.items():
        # This trick is *not* a bug in Leo!
        doc_s = textwrap.dedent(docstr.rstrip()).strip()
        listing.append(f'{name}\n' + '=' * len(name) + f'\n\n{doc_s}\n\n')
    listing_s = ''.join(listing)
    g.es(listing_s, tabName='layouts')


#@ command: show_layout_name
@g.command('show-current-layout')
def show_layout_name(event: LeoKeyEvent | None = None) -> None:
    c = event.get('c') if event else None
    if not c:
        return
    cache = c.frame.top.layout_cache
    if cache.layout_dict:
        name = cache.layout_dict.get('name', 'unnamed layout')
    else:
        name = 'unnamed layout'
    g.es(name)


#@< Layouts
#@> FALLBACK_LAYOUT
FALLBACK_LAYOUT: dict[str, Any] = {
    'SPLITTERS': OrderedDict(
        (
            ('outlineFrame', 'secondary_splitter'),
            ('logFrame', 'secondary_splitter'),
            ('secondary_splitter', 'main_splitter'),
            ('bodyFrame', 'main_splitter'),
        )
    ),
    'ORIENTATIONS': {
        'main_splitter': Orientation.Horizontal,
        'secondary_splitter': Orientation.Vertical,
    },
}
#@ LEGACY_LAYOUT
LEGACY_LAYOUT = {
    'SPLITTERS': OrderedDict(
        (
            ('bodyFrame', 'secondary_splitter'),
            (VR_OBJ_NAME, 'secondary_splitter'),
            (VR3_OBJ_NAME, 'secondary_splitter'),
            ('outlineFrame', 'outline-log-splitter'),
            ('logFrame', 'outline-log-splitter'),
            ('outline-log-splitter', 'main_splitter'),
            ('secondary_splitter', 'main_splitter'),
        )
    ),
    'ORIENTATIONS': {
        'outline-log-splitter': Orientation.Horizontal,
        'secondary_splitter': Orientation.Horizontal,
        'main_splitter': Orientation.Vertical,
    },
    'name': 'legacy',
}
#@ HORIZONTAL_THIRDS_LAYOUT
HORIZONTAL_THIRDS_LAYOUT = {
    'SPLITTERS': OrderedDict(
        (
            ('outlineFrame', 'secondary_splitter'),
            ('logFrame', 'secondary_splitter'),
            (VR_OBJ_NAME, 'vr_splitter'),
            (VR3_OBJ_NAME, 'vr_splitter'),
            ('secondary_splitter', 'main_splitter'),
            ('bodyFrame', 'main_splitter'),
            ('vr_splitter', 'main_splitter'),
        )
    ),
    'ORIENTATIONS': {
        'secondary_splitter': Orientation.Horizontal,
        'main_splitter': Orientation.Vertical,
        'vr_splitter': Orientation.Horizontal,
    },
    'name': 'horizontal-thirds',
}
#@ RENDERED_FOCUSED_LAYOUT
RENDERED_FOCUSED_LAYOUT = {
    'SPLITTERS': OrderedDict(
        (
            ('outlineFrame', 'secondary_splitter'),
            ('bodyFrame', 'secondary_splitter'),
            ('logFrame', 'secondary_splitter'),
            (VR_OBJ_NAME, 'vr_splitter'),
            (VR3_OBJ_NAME, 'vr_splitter'),
            ('vr_splitter', 'body-vr-splitter'),
            ('secondary_splitter', 'main_splitter'),
            ('body-vr-splitter', 'main_splitter'),
        )
    ),
    'ORIENTATIONS': {
        'body-vr-splitter': Orientation.Horizontal,
        'secondary_splitter': Orientation.Vertical,
        'main_splitter': Orientation.Horizontal,
        'vr_splitter': Orientation.Horizontal,
    },
    'name': 'render-focused',
}

#@ VERTICAL_THIRDS2_LAYOUT
VERTICAL_THIRDS2_LAYOUT = {
    'SPLITTERS': OrderedDict(
        (
            ('logFrame', 'secondary_splitter'),
            ('bodyFrame', 'secondary_splitter'),
            ('outlineFrame', 'main_splitter'),
            (VR_OBJ_NAME, 'vr-splitter'),
            (VR3_OBJ_NAME, 'vr-splitter'),
            ('secondary_splitter', 'main_splitter'),
            ('vr-splitter', 'main_splitter'),
        )
    ),
    'ORIENTATIONS': {
        'vr-splitter': Orientation.Horizontal,
        'secondary_splitter': Orientation.Vertical,
        'main_splitter': Orientation.Horizontal,
    },
    'name': 'vertical-thirds2',
}
#@ VERTICAL_THIRDS_LAYOUT
VERTICAL_THIRDS_LAYOUT = {
    'SPLITTERS': OrderedDict(
        (
            ('outlineFrame', 'secondary_splitter'),
            ('logFrame', 'secondary_splitter'),
            ('secondary_splitter', 'main_splitter'),
            ('bodyFrame', 'main_splitter'),
            (VR_OBJ_NAME, 'main_splitter'),
            (VR3_OBJ_NAME, 'main_splitter'),
        )
    ),
    'ORIENTATIONS': {
        'secondary_splitter': Orientation.Vertical,
        'main_splitter': Orientation.Horizontal,
    },
    'name': 'vertical-thirds',
}


#@< class LayoutCacheWidget
class LayoutCacheWidget(QWidget):
    """
    Manage layouts, which may be defined by methods or by
    a layout data structure such as the following::

        FALLBACK_LAYOUT = {
            'SPLITTERS':OrderedDict(
                (('outlineFrame', 'secondary_splitter'),
                ('logFrame', 'secondary_splitter'),
                ('secondary_splitter', 'main_splitter'),
                ('bodyFrame', 'main_splitter'))
            ),
            'ORIENTATIONS':{
            'main_splitter':Orientation.Horizontal,
            'secondary_splitter':Orientation.Vertical}
        }
    """

    def __init__(self, c: Cmdr, parent: QWidget | None) -> None:
        super().__init__(parent)
        self.c = c
        self.setObjectName('leo-layout-cache')
        self.layout_dict: dict | None = None

        # maps splitter objectNames to their splitter object.
        self.created_splitter_dict: dict[str, QWidget] = {}
        self.layout_registry = LAYOUT_REGISTRY

    #@+others
    #@> LayoutCasheWidget: contract_*
    #@> LCW.contract_body
    def contract_body(self) -> None:
        """Contract the body pane"""
        self.contract_pane(self.c.frame.body.widget)

    #@ LCW.contract_log
    def contract_log(self) -> None:
        """Contract the log pane"""
        self.contract_pane(self.c.frame.log.logWidget)

    #@ LCW.contract_outline
    def contract_outline(self) -> None:
        """Contract the outline pane"""
        self.contract_pane(self.c.frame.tree.treeWidget)

    #@ LCW.contract_vr
    def contract_vr(self) -> None:
        """Contract the VR pane if VR is running"""
        c = self.c
        if is_module_loaded(VR_MODULE_NAME):
            if vr := getattr(c, 'vr', None):
                self.expand_pane(vr)
                return
        g.es_print('VR is not running', color='blue')

    #@ LCW.contract_vr3
    def contract_vr3(self) -> None:
        """Contract the VR3 pane if VR3 is running"""
        c = self.c
        if is_module_loaded(VR3_MODULE_NAME):
            from leo.plugins.viewrendered3 import controllers

            vr3 = controllers.get(c.hash())
            if vr3:
                self.contract_pane(vr3)
        else:
            g.es_print('VR3 is not running', color='blue')

    #@< LayoutCacheWidget: expand_*
    #@> LCW.expand_body
    def expand_body(self) -> None:
        """Expand the body pane"""
        self.expand_pane(self.c.frame.body.widget)

    #@ LCW.expand_log
    def expand_log(self) -> None:
        """Expand the log pane"""
        self.expand_pane(self.c.frame.log.logWidget)

    #@ LCW.expand_outline
    def expand_outline(self) -> None:
        """Expand the outline pane."""
        self.expand_pane(self.c.frame.tree.treeWidget)

    #@ LCW.expand_vr
    def expand_vr(self) -> None:
        """Expand the VR pane if VR is running"""
        c = self.c
        if is_module_loaded(VR_MODULE_NAME):
            if vr := getattr(c, 'vr', None):
                self.expand_pane(vr)
                return
        g.es_print('VR is not running', color='blue')

    #@ LCW.expand_vr3
    def expand_vr3(self) -> None:
        """Expand the VR3 pane if VR3 is running"""
        c = self.c
        if is_module_loaded(VR3_MODULE_NAME):
            from leo.plugins.viewrendered3 import controllers

            if vr3 := controllers.get(c.hash()):
                self.expand_pane(vr3)
                return
        g.es_print('VR3 is not running', color='blue')

    #@< LayoutCacheWidget: utils
    #@> LCW.contract_pane
    def contract_pane(self, widget: QWidget) -> None:
        """Contract the pane containing the given widget."""
        self.resize_pane(widget, delta=-40)

    #@ LCW.expand_pane
    def expand_pane(self, widget: QWidget) -> None:
        """Expand the pane containing the given widget."""
        self.resize_pane(widget, delta=40)

    #@ LCW.find_splitter_by_name
    def find_splitter_by_name(self, name: str) -> QSplitter | None:
        """Return the splitter with the given objectName."""

        def is_splitter(obj: object) -> bool:
            return obj is not None and isinstance(obj, QSplitter)

        splitter: Any
        splitter = self.find_widget(name)
        if is_splitter(splitter):
            return splitter  # type:ignore  # We've just checked the type.
        splitter = self.created_splitter_dict.get(name, None)
        if is_splitter(splitter):
            return splitter  # type:ignore  # We've just checked the type.
        for child in self.children():
            if child.objectName() == name and is_splitter(child):
                return child  # type:ignore  # We've just checked the type.
        return None

    #@ LCW.find_widget
    def find_widget(self, name: str) -> QWidget:
        """Return a widget given it objectName."""
        return g.app.gui.find_widget_by_name(self.c, name)

    #@ LCW.find_widget_in_children
    def find_widget_in_children(self, name: str) -> QWidget | None:
        """Return a child widget with the given objectName."""
        w: QWidget | None = None
        for kid in self.children():
            if kid.objectName() == name:
                w = kid  # type:ignore
        return w

    #@ LCW.resize_pane
    def resize_pane(self, widget: QWidget, delta: int) -> None:
        """Resize the pane containing the given widget."""
        splitter, direct_child = g.app.gui.find_parent_splitter(widget)
        if not splitter:
            g.trace(f"Oops! no splitter for name: {widget.objectName()!r}")
            return

        index = splitter.indexOf(direct_child)
        if index == -1:
            g.trace(f"Oops! direct child: {direct_child!r} not in {splitter}")
            return

        # Look for another *visible* widget.
        sizes = splitter.sizes()
        widget_size = sizes[index]
        if widget_size > 0:
            for other_index, size in enumerate(sizes):
                if other_index != index and size > 0:
                    sizes[index] += delta
                    sizes[other_index] -= delta
                    splitter.setSizes(sizes)
                    return

        # #4325. Try resizing a parent frame.
        parent_splitter, _junk = g.app.gui.find_parent_splitter(splitter)
        if not parent_splitter:
            g.trace('No parent splitter')
            return

        index = parent_splitter.indexOf(splitter)
        if index == -1:
            g.trace(f"Oops! {splitter} not in {parent_splitter}")
            return

        # It's valid for the splitter's size to be zero!
        for other_index, size in enumerate(sizes):
            if other_index != index and size > 0:
                sizes = parent_splitter.sizes()
                sizes[index] += delta
                sizes[other_index] -= delta
                parent_splitter.setSizes(sizes)
                return

    #@ LCW.restoreFromLayout
    def restoreFromLayout(self, layout: dict | None = None) -> None:
        self.layout_dict = layout
        if layout is None:
            layout = FALLBACK_LAYOUT
        #@+<< initialize data structures >>
        #@-<< initialize data structures >>
        #@+<< rehome body editor >>
        #@-<< rehome body editor >>
        #@+<< clean up splitters >>
        #@-<< clean up splitters >>
        #@+<< set default orientations >>
        #@-<< set default orientations >>
        #@+<< move widgets to targets >>
        #@-<< move widgets to targets >>
        #@+<< resize splitters >>
        #@-<< resize splitters >>
        editor.show()

    #@-others


#@-others

#@-leo
