from time import time, sleep
from animations import Anim
from primitives import slide_number, clear

FRAME_DELAY = 0.02



def run(frame, animation):
    # ensure that animation is an *Anim* object
    if isinstance(animation, Anim):
        anim = animation
    else:
        anim = Anim(frame, animation)
    # the animation loop
    for modif_list in anim:
        time_before_modifs = time()
        for modif in modif_list:
            modif(frame)
        # refresh only after all the modifications
        frame.refresh()
        # wait as long as needed so the frame lasts *FRAME_DELAY*
        while time() < time_before_modifs + FRAME_DELAY:
            pass

def play(frame, animation):
    run(frame, animation)
    frame.pause()

def present(frame, anim_list: list):
    """Show a list of animations as a presentation."""
    len_anim_list = len(anim_list)
    idx_anim = 0
    while idx_anim < len_anim_list:
        run(frame, Anim(frame, clear()))
        frame.getkey()
        run(frame, anim_list[idx_anim] >> slide_number(idx_anim, len_anim_list))
        key = frame.getkey()
        if key == "k":
            idx_anim -= 1
        else:
            idx_anim += 1





