from __init__ import *


def main(scr):
    initialize_curses_colors()
    fr = Frame(scr)
    anim = Anim(fr) >> h1(1, "Animations")
    anim &= h2(3, "Une librairie d'animations sur terminal")
    anim &= bullets(5, [
        "animations en mode texte",
        "très flexible",
        [
            "système de composition d'animations",
            "animations primitives diverses",
            "possibilité de créer des primitives",
            "modèle d'animations simple mais généraliste"
            ],
        "simple",
        ], pauses=True)


    present(fr, [anim, anim])



curses.wrapper(main)
