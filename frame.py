import curses
from typing import TypeVar


class Frame:
    def __init__(self, scr) -> None:
        # scr is a curses stdscr
        self.scr = scr
        # Coordinates of the origin
        # Theses can be modified, so that everything added will be shifted
        self.X = 0
        self.Y = 0

    def put_text(self, y: int, x: int, text: str, col: int =None) -> None:
        Y = (int(y) + self.Y) % self.getheight()
        X = (int(x) + self.X) % self.getwidth()
        if col is None:
            self.scr.addstr(Y, X, str(text))
        else:
            self.scr.addstr(Y, X, str(text), curses.color_pair(col))

    def addstr(self, *args, **kwargs):
        """The original curses function."""
        y, x, *args = args
        Y, X = int(y) + self.Y, int(x) + self.X
        self.scr.addstr(Y, X, *args, **kwargs)

    def move_origin(self, y: int, x: int):
        """shift the origin of the frame, so that new things are shifted."""
        self.Y = int(y)
        self.X = int(x)

    def reset_origin(self):
        """Reset the origin so that everything is put on its real coordinate."""
        move_origin(0, 0)

    def refresh(self):
        self.scr.refresh()

    def clear(self):
        self.scr.clear()

    def getmaxyx(self):
        """Return a tuple (y, x) of the height and width of the frame."""
        return self.scr.getmaxyx()

    def getheight(self):
        return self.scr.getmaxyx()[0]

    def getwidth(self):
        return self.scr.getmaxyx()[1]

    def pause(self):
        # wait for keypress on getkey
        self.scr.nodelay(0)
        # ask for a key
        self.scr.getkey()
        # reset the nodelay
        self.scr.nodelay(1)

    def getkey(self):
        # wait for keypress on getkey
        self.scr.nodelay(0)
        # ask for a key
        key = self.scr.getkey()
        # reset the nodelay
        self.scr.nodelay(1)
        # return the pressed key
        return key

    def copy(self):
        return Frame(self.scr)


def main(stdscr):
    frame = Frame(stdscr)


if __name__ == '__main__':
    curses.wrapper(main)


