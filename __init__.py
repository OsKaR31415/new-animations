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


    anim = Anim(fr) >> bounce("coucou")

    play(fr, slow(anim, 1))


if __name__ == "__main__":
    curses.wrapper(main)

