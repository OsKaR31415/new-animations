import curses
from frame import Frame
from animations import Anim, AnimIterator
from primitives import *
from anim_player import play

from random import randint, choice


def initialize_curses_colors():
    """Initialize the color support of curses (256 colors)."""
    curses.curs_set(0)  # hide the cursor
    curses.start_color()
    curses.use_default_colors()
    # set color_pair for each color
    for i in range(curses.COLORS):
        curses.init_pair(i, i, -1)
        # curses.init_pair(i + 256, i,)


def main(scr):
    initialize_curses_colors()
    fr = Frame(scr)

    coucou = Anim(fr,     fadein(8,  23, "coucou "))
    ca_va = Anim(fr, appear_left(10, 23, "ca va ?"))
    salut = Anim(fr,  appear_top(12, 23, "salut  "))

    anim = coucou << salut >> ca_va & salut & ca_va & coucou

    play(fr, slow(anim, 2))


if __name__ == "__main__":
    curses.wrapper(main)

