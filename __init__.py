import curses
from frame import Frame
from animations import Anim, AnimIterator
from primitives import *
from anim_player import play, present

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


    anim = Anim(fr) >> fadein(3, 2, "coucou")
    anim &= fadein(6, 7, "truc")
    anim >>= bounce_left(2, "test")
    anim >>= repeat(5, appear_top(10, 10, "super !!!!!!!", 73))
    anim >>= repeat(5, appear_left(5, 20, "génial", 172))
    anim >>= Anim(fr) & wait(5) & bounce_left(1, "super chose")



    play(fr, slow(anim, 2))


if __name__ == "__main__":
    curses.wrapper(main)

