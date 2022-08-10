import curses
from animations import Anim


# ╺┳╸╻┏┳┓╻┏┓╻┏━╸
#  ┃ ┃┃┃┃┃┃┗┫┃╺┓
#  ╹ ╹╹ ╹╹╹ ╹┗━┛

def pause():
    """pause and wait for a keypress."""
    return [[lambda fr: fr.pause()]]


def wait(delay: int =100):
    """Wait for *delay* units."""
    return [[]] * delay



# ┏┓ ┏━┓┏━┓╻┏━╸   ╺┳╸┏━╸╻ ╻╺┳╸
# ┣┻┓┣━┫┗━┓┃┃      ┃ ┣╸ ┏╋┛ ┃
# ┗━┛╹ ╹┗━┛╹┗━╸    ╹ ┗━╸╹ ╹ ╹
# animations that simply show text, with some style


def clear():
    """Clear the frame."""
    return [[lambda frame: frame.clear()]]

def text(x: int, y: int, string: str, col: int =None):
    """Add the given *string* text at the given x, y coordinates, with the
    given *col* color.
    Args:
        y (int): The line to add the text at.
        x (int): The column to add the text at.
        string (str): The text to add.
        col (int): The color of the text.
    Returns:
        list: The corresponding animation
    """
    if col is None:
        col = 0
    return [[lambda frame: frame.put_text(int(x), int(y),
                                          str(string), int(col))]]


def addstr(*args, **kwargs):
    """Copy of the curses window.addstr function.
    It accepts more parameters than the *text* primitive, so you can have more
    advanced styles, like bold, italics, underline, etc.
    """
    return [[lambda frame: frame.addstr(*args, **kwargs)]]


# ⢎⡑ ⡇ ⡷⢾ ⣏⡱ ⡇  ⣏⡉   ⢹⠁ ⣏⡉ ⢇⡸ ⢹⠁   ⢎⡑ ⢹⠁ ⢇⢸ ⡇  ⣏⡉ ⢎⡑
# ⠢⠜ ⠇ ⠇⠸ ⠇  ⠧⠤ ⠧⠤   ⠸  ⠧⠤ ⠇⠸ ⠸    ⠢⠜ ⠸   ⠇ ⠧⠤ ⠧⠤ ⠢⠜

# TODO: bold and other styles don't work :(
# def bold(y: int, x: int, string: str, col: int =None):
#     if col is None:
#         col = 0
#     return [(lambda frame: addstr(y, x, string,
#                                   curses.color_pair(col)),)]

# def italic(y: int, x: int, string: str, col: int =None):
#     if col is None:
#         col = 1
#     return addstr(y, x, string, curses.A_ITALIC + curses.color_pair(col))




# ⣏⡉ ⣎⣱ ⡏⢱ ⣏⡉   ⣏⡉ ⣏⡉ ⣏⡉ ⣏⡉ ⡎⠑ ⢹⠁ ⢎⡑
# ⠇  ⠇⠸ ⠧⠜ ⠧⠤   ⠧⠤ ⠇  ⠇  ⠧⠤ ⠣⠔ ⠸  ⠢⠜
# effects that only change the color of the same text

def fadein(y: int, x: int, string: str):
    # make the text invisible at the beginning
    anim = addstr(y, x, string, curses.A_INVIS)
    for col in range(233, 256):
        anim.extend(text(y, x, string, col))
    return anim


def fadeout(y: int, x: int, string: str):
    anim = []
    for col in reversed(range(233, 256)):
        anim.extend(text(y, x, string, col))
    # make the text invisible at the end because 233 is not exactly black
    anim.extend(addstr(y, x, string, curses.A_INVIS))
    return anim


def fadeinout(y: int, x: int, string: str):
    anim = fadein(y, x, string)
    anim += fadeout(y, x, string)
    return anim


def color_ramp(y: int, x: int, string: str, col_ramp: list[int]):
    """Show a string with its colors following the given *col_ramp*.
    Can be used to make color effects like random colors, fade int..."""
    anim = []
    for col in list(col_ramp):
        anim.extend(text(y, x, string, int(col)))
    return anim


# ╻ ╻╻┏━╸╻ ╻┏━╸┏━┓   ┏━┓┏━┓╺┳┓┏━╸┏━┓
# ┣━┫┃┃╺┓┣━┫┣╸ ┣┳┛   ┃ ┃┣┳┛ ┃┃┣╸ ┣┳┛
# ╹ ╹╹┗━┛╹ ╹┗━╸╹┗╸   ┗━┛╹┗╸╺┻┛┗━╸╹┗╸
# functions to modify animations

def repeat(anim, times: int):
    """Repeat *times* times the animation *anim*.
    Args:
        anim: The animation to repeat
        times (int): The number of repetitions."""
    if isinstance(anim, Anim):
        return Anim(anim.frame, anim.anim * times)
    else:
        return anim * times


# FIXME
# def slow(anim, factor: int):
#     """Slow the animation by of factor of *factor* times."""
#     if isinstance(anim, Anim):
#         animation = anim.anim
#         frame = anim.frame
#     else:
#         animation = anim
#     slowed_anim = []
#     for step in animation:
#         slowed_anim.extend([[step]] * factor)
#     if isinstance(anim, Anim):
#         return Anim(frame, animation)
#     else:
#         return animation




