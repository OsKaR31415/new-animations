from time import time, sleep
from animations import Anim

FRAME_DELAY = 0.02


def play(frame, animation):
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
    frame.pause()




