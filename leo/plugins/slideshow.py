#@+leo-ver=cub-1-thin
#@0 [ekr.20060831165821] @f ../plugins/slideshow.py
#@+<< docstring >>
#@> << docstring >>
"""Supports slideshows in Leo outlines.

This plugin defines four new commands:

- next-slide-show:  move to the start of the next slide show,
  or the first slide show if no slide show has been seen yet.
- prev-slide-show:  move to the start of the previous slide show,
  or the first slide show if no slide show has been seen yet.
- next-slide: move to the next slide of a present slide show.
- prev-slide: move to the previous slide of the present slide show.

Slides shows consist of a root @slideshow node with descendant @slide nodes.
@slide nodes may be organized via non-@slide nodes that do not appear in the slideshow.

All these commands ignore @ignore trees.

"""

#@-<< docstring >>
#@+<< imports >>
#@ << imports >>
from leo.core import leoGlobals as g
#@-<< imports >>

# To do:
# - Add sound/script support for slides.
# - Save/restore changes to slides when entering/leaving a slide.


#@+others
#@ init
def init():
    """Return True if the plugin has loaded successfully."""
    g.registerHandler(('open2', 'new2'), onCreate)
    g.plugin_signon(__name__)
    return True


#@ onCreate
def onCreate(tag, keys):
    c = keys.get('c')
    if c:
        slideshowController(c)


#@ class slideshowController
class slideshowController:
    #@+others
    #@> __init__
    def __init__(self, c):
        self.c = c
        self.firstSlideShow = None
        self.slideShowRoot = None
        self.slide = None
        self.createCommands()

    #@ createCommands (slideshowController)
    def createCommands(self):
        c = self.c
        k = c.k
        for commandName, func in (
            ('next-slide-command', self.nextSlide),
            ('next-slide-show-command', self.nextSlideShow),
            ('prev-slide-command', self.prevSlide),
            ('prev-slide-show-command', self.prevSlideShow),
        ):
            k.registerCommand(commandName, func)

    #@ findFirstSlideShow
    def findFirstSlideShow(self):
        c = self.c
        for p in c.all_positions():
            h = p.h.strip()
            if h.startswith('@slideshow'):
                self.firstSlideShow = p.copy()
                return p
            if g.match_word(h, 0, '@ignore'):
                p = p.nodeAfterTree()
        self.firstSlideShow = None
        return None

    #@ ignored
    def ignored(self, p):
        for p2 in p.self_and_parents():
            if g.match_word(p2.h, 0, '@ignore') or g.match_word(p2.h, 0, '@noslide'):
                return True
        return False

    #@ nextSlide
    def nextSlide(self, event=None):
        c = self.c
        p = c.p
        if p == self.slide:
            p = self.slide.threadNext()
            oldSlide = self.slide
        else:
            oldSlide = None
        while p:
            h = p.h.strip()
            if self.ignored(p):
                p = p.threadNext()
            elif h.startswith('@slideshow'):
                self.select(p)
                return g.es('At %s of slide show' % 'end' if oldSlide else 'start')
            elif g.match_word(h, 0, '@ignore') or g.match_word(h, 0, '@noslide'):
                p = p.nodeAfterTree()
            else:
                return self.select(p)
            # elif h.startswith('@slide'):
            # return self.select(p)
            # else: p = p.threadNext()
        return g.es('At end of slide show' if self.slideShowRoot else 'Not in any slide show')

    #@ nextSlideShow
    def nextSlideShow(self, event=None):
        c = self.c
        self.findFirstSlideShow()
        if not self.firstSlideShow:
            g.es('No slide show found')
            return
        if not self.slideShowRoot:
            self.select(self.firstSlideShow)
            return
        p = c.p
        h = p.h.strip()
        if h.startswith('@slideshow'):
            p = p.threadNext()
        while p:
            h = p.h.strip()
            if self.ignored(p):
                p = p.threadNext()
            elif h.startswith('@slideshow'):
                self.select(p)
                return
            elif g.match_word(h, 0, '@ignore'):
                p = p.nodeAfterTree()
            else:
                p = p.threadNext()
        self.select(self.slideShowRoot)
        g.es('At start of last slide show')

    #@ prevSlide
    def prevSlide(self, event=None):
        c = self.c
        p = c.p
        if self.ignored(p):
            p = p.threadBack()
        else:
            if self.slide and self.slide == self.slideShowRoot:
                return g.es('At start of slide show')
            if p == self.slide:
                p = self.slide.threadBack()
        while p:
            h = p.h.strip()
            if self.ignored(p):
                p = p.threadBack()
            elif h.startswith('@slideshow'):
                self.select(p)
                return g.es('At start of slide show')
            else:
                return self.select(p)
            # elif h.startswith('@slide'):
            # return self.select(p)
            # else: p = p.threadBack()
        p = self.findFirstSlideShow()
        if p:
            self.select(p)
            return g.es('At start of first slide show')
        return g.es('No slide show found')

    #@ prevSlideShow
    def prevSlideShow(self, event=None):
        c = self.c
        self.findFirstSlideShow()
        if not self.firstSlideShow:
            g.es('No slide show found')
            return
        if not self.slideShowRoot:
            self.select(self.firstSlideShow)
            return
        p = c.p
        h = p.h.strip()
        if h.startswith('@slideshow'):
            p = p.threadBack()
        while p:
            h = p.h.strip()
            if self.ignored(p):
                p = p.threadBack()
            elif h.startswith('@slideshow'):
                self.select(p)
                return
            else:
                p = p.threadBack()
        self.select(self.firstSlideShow)
        g.es('At start of first slide show')

    #@ select
    def select(self, p):
        """Make p the present slide, and set self.slide and maybe self.slideShowRoot."""
        c = self.c
        h = p.h.strip()
        w = c.frame.body.wrapper
        g.es('%s' % h)
        c.redraw(p)
        w.see(0)
        if h.startswith('@slideshow'):
            self.slideShowRoot = p.copy()
        self.slide = p.copy()

    #@-others


#@-others
#@-leo
