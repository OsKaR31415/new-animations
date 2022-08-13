import curses
from animations import Anim
from flib import flatten
from time import sleep
from random import randint
from math import cos



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



# ⢹⠁ ⣏⡉ ⢇⡸ ⢹⠁   ⡇⢸ ⡇ ⢹⠁ ⣇⣸   ⢎⡑ ⢹⠁ ⢇⢸ ⡇  ⣏⡉
# ⠸  ⠧⠤ ⠇⠸ ⠸    ⠟⠻ ⠇ ⠸  ⠇⠸   ⠢⠜ ⠸   ⠇ ⠧⠤ ⠧⠤


#### Simple styles ####
def invisible(y: int, x: int, string: str):
    return addstr(int(y), int(x), str(string), curses.A_INVIS)


def center(y: int, string: str, col: int =0):
    y = int(y)
    col = int(col)
    string = str(string)
    return [[lambda fr: fr.put_text(
        y, (fr.getwidth() - len(string)) // 2, string, col)]]

def center_addstr(y: int, string: str, style: int =0):
    y = int(y)
    string = str(string)
    style = int(style)
    return [[lambda fr: fr.addstr(
        y, (fr.getwidth() - len(string)) // 2, string, style)]]

def bold(y: int, x: int, string: str, col: int =None):
    """Show text in bold style."""
    if col is None:
        col = 0
    return addstr(int(y), int(x), str(string), curses.color_pair(col) | curses.A_BOLD)

def italic(y: int, x: int, string: str, col: int =None):
    if col is None:
        col = 0
    return addstr(int(y), int(x), str(string), curses.color_pair(col) | curses.A_ITALIC)

def underline(y: int, x: int, string: str, col: int =None):
    if col is None:
        col = 0
    return addstr(int(y), int(x), str(string), curses.color_pair(col) | curses.A_UNDERLINE)

def standout(y: int, x: int, string: str, col: int =None):
    if col is None:
        col = 0
    return addstr(int(y), int(x), str(string), curses.color_pair(col) | curses.A_STANDOUT)

def blink(y: int, x: int, string: str, col: int =None):
    if col is None:
        col = 0
    return addstr(int(y), int(x), str(string), curses.color_pair(col) | curses.A_BLINK)



#### Titles ####
def h1(y: int, string: str):
    """First-level title."""
    return center_addstr(
            y, string,
            curses.color_pair(208) | curses.A_BOLD | curses.A_UNDERLINE)

def h2(y: int, string: str):
    """Second-level title (subtitle)."""
    return addstr(
            y, 1, string,
            curses.color_pair(33) | curses.A_BOLD | curses.A_UNDERLINE)

def h3(y: int, string: str):
    """Third-level title (sub-subtitle)."""
    return addstr(
            y, 1, string,
            curses.color_pair(28) | curses.A_BOLD
            )

def h4(y: int, string: str):
    """Fourth-level title (sub-sub-subtitle)."""
    return addstr(
            y, 1, string,
            curses.color_pair(38) | curses.A_BOLD
            )

def h5(y: int, string: str):
    """Fith-level title (sub-sub-sub-subtitle)"""
    return addstr(
            y, 1, string,
            curses.color_pair(25) | curses.A_BOLD)



#### Lists ####

def item(y: int, string: str, symbol: str ="━", depth: int =0, pauses: bool =False):
    """Position an list item.
    Args:
        y (int): The line to put the item at.
        string (str): The text to put in the item.
        symbol (str): The symbol to use as a bullet icon. (defaults to ━)
        depth (int): The indentation to put the item list at. (defaults to 0)
        pauses (bool): Wether to put a pause before the item appears.
                   (defaults to False)
    """
    indent = int(depth) * 2 + 5
    symbol = str(symbol)
    anim = []
    if pauses:
        anim.extend(pause())
    anim.extend(text(y, indent, symbol + ' ' + string))
    return anim

def bullet(y: int, string: str, depth: int =0, pauses: bool =False):
    depth = min(5, max(0, int(depth)))  # make depth an int between 0 and 3
    symbol = "●○◆▶━•"[depth]
    anim = item(y, string, symbol, depth, pauses)
    return anim

def bullets(y: int, strings: list[str], pauses: bool =False):
    def aux(y, strings, depth, pauses):
        result = []
        line = 0  # the line where to put the bullet isnt equal to *idx*
        for idx, item in enumerate(strings):
            if isinstance(item, str):
                result.extend(bullet(y + line, item, depth, pauses))
                line += 1
            else:
                result.extend(aux(y + line, item, depth + 1, pauses))
                # we need to add as much lines as the recustion call has added.
                # That is preciesly the number of items of the flatened sublist
                line += len(flatten(item))
        return result
    return aux(int(y), list(strings), 0, pauses)


# ⡎⠑ ⡎⢱ ⡷⢾ ⣏⡱ ⡇  ⣏⡉ ⢇⡸   ⣏⡉ ⣏⡉ ⣏⡉ ⣏⡉ ⡎⠑ ⢹⠁ ⢎⡑
# ⠣⠔ ⠣⠜ ⠇⠸ ⠇  ⠧⠤ ⠧⠤ ⠇⠸   ⠧⠤ ⠇  ⠇  ⠧⠤ ⠣⠔ ⠸  ⠢⠜

def typing(y: int, x: int, string: str):
    letters_timing = {
            " ": 1,
            "qsdfjklm": 0,
            "gh": 1,
            "azeruiop": 1,
            "wxcvn": 2,
            "tyvb": 3,
            }
    string = str(string)
    anim = []
    for idx, letter in enumerate(string):
        for letters, timing in letters_timing.items():
            if letter in letters:
                anim.extend(wait(timing))
                break
            elif letter.lower() in letters:
                # upper case letters are longer to type
                anim.extend(wait(timing + 1))
                break
        else:  # if the letter is nowhere in *letters_timing*
            anim.extend(wait(randint(1, 3)))
        anim.extend(wait(randint(0, 1)))
        # retyping everything every time, so the text is not erased until the
        # animation is finished.
        # also helps for line wrapping
        anim.extend(text(int(y), int(x), string[:idx + 1]))
    return anim


######################
#### Fade effects ####
######################

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


########################
#### Motion effects ####
########################

def appear_top(y: int, x: int, string: str, col: int =None, delay: int =1):
    """Make the text apprear from the top of the screen.
    Args:
        y (int): The line to put the text at.
        x (int): The column to put the text at.
        string (str): The text to animate.
        col (int): The color of the text.
        delay (int): The number of frames to wait between each motion step.
    """
    anim = []
    for line in range(0, int(y) + 1):
        anim.extend(over(
            invisible(max(0, line-1), x, string),
            text(line, x, string, col)))
        anim.extend(wait(delay))
    return anim


def appear_left(y: int, x: int, string: str, col: int =None, delay: int =0):
    """Make the text apprear from the left of the screen.
    Args:
        y (int): The line to put the text at.
        x (int): The column to put the text at.
        string (str): The text to animate.
        col (int): The color of the text.
        delay (int): The number of frames to wait between each motion step.
    """
    anim = []
    for column in range(0, int(x) + 1):
        anim.extend(over(
            invisible(y, max(0, column - 1), string),
            text(y, column, string, col)
            ))
        anim.extend(wait(delay))
    return anim



def bounce(string: str):
    anim = []
    for x in reversed(range(0, 10)):
        anim.extend(text(1, int(10*cos(x)), string))
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


def over(*animations):
    """join animations to be played at the same time.
    acts like (and using) the >> operator."""
    first, *animations = animations
    result = Anim("foo", first)
    for anim in animations:
        result = result >> Anim("foo", anim)
    return result.anim


def under(*animations):
    """join animations to be played at the same time.
    acts like (and using) the << (under) operator."""
    first, *animations = animations
    result = Anim("foo", first)
    for anim in animations:
        result = result << Anim("foo", anim)
    return result.anim


def slow(anim, factor: int):
    """Slow the animation by of factor of *factor* times."""
    if isinstance(anim, Anim):
        animation = anim.anim
        frame = anim.frame
    else:
        animation = anim
    slowed_anim = []
    for step in animation:
        slowed_anim.append(step)
        slowed_anim.extend(wait(int(factor) - 1))
    if isinstance(anim, Anim):
        return Anim(frame, slowed_anim)
    else:
        return slowed_anim


def reverse(anim):
    """Reverse an animation."""
    if isinstance(anim, Anim):
        return Anim(anim.frame, list(reversed(anim.anim)))
    return list(reversed(anim))


