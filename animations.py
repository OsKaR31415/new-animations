

class AnimIterator:
    def __init__(self, anim):
        """Initialize the object.
        Args:
            anim (Anim): The anim object to make the iterator of.
        """
        self.anim = anim
        self.index = -1  # start at -1 because the increment is done before the return

    def __next__(self):
        self.index += 1
        try:
            return self.anim[self.index]
        except IndexError:
            raise StopIteration


class Anim:
    def __init__(self, frame, animation=[], after: int =0) -> None:
        # the number of frames to wait before the beginning of the animation
        self.after = int(after)
        # the frame to play the animation in
        self.frame = frame
        # the animation representation : list of lists of frame modifications
        self.anim = self.__init_animation__(animation)

    def __init_animation__(self, anim):
        if self.after > 0:
            return ([()] * self.after) + list(anim)
        return list(anim)

    def __iter__(self):
        return AnimIterator(self.anim)

    def __str__(self):
        return f"\n[in {self.frame}] : \n {self.anim}"

    def __compose_with__(self, other):
        """Compose with another animation.
        Args:
            other (Anim): The animation to add over the current one.
        Returns:
            list: The new animation formed with composing *self* and *other*.
        """
        # this is very similar to itertools zip_longest, but elements are
        # joined together instead of put side-by-side in a list
        composed_anim = []
        # go through the longest one
        length = max(len(self.anim), len(other.anim))
        for idx in range(length):
            current_step = []
            if idx < len(self.anim):
                # note the extend, not append : we need to have only one list
                # of frame modifications
                current_step.extend(self.anim[idx])
            if idx < len(other.anim):
                # extend, not append, for the same reason
                current_step.extend(other.anim[idx])
            # make a tuple of frame modifications
            composed_anim.append(tuple(current_step))
        return composed_anim


    def __rshift__(self, other):
        """The >> operator is used to compose two animations.
        That means playing them at the same time.
        *other* will be added atop of *self*.
        This operator is called "over".
        Args:
            other (Anim): The animation to add over the current one.
        Returns:
            Anim: The new animation formed with composing *self* and *other*.
        """
        if not isinstance(other, Anim):
            other = Anim(self.frame, other)
        return Anim(self.frame, self.__compose_with__(other))

    def __lshift__(self, other):
        """The << operator is used to compose two animations.
        That means playing them at the same time.
        *other* well be added behind of *self* (at the very behind if *self* is
        already a composed animation).
        This operator is called "under".
        Args:
            other (Anim): The animation to add behind the current one.
        Returns:
            Anim: The new animation formed with composing *self* and *other*.
        """
        if not isinstance(other, Anim):
            other = Anim(self.frame, other)
        # it's just like >> but swapped !
        return other >> self

    def __and__(self, other):
        """The & operator is used to concatenate two animations.
        That means playing them one at a time.
        This operator is called "and" or "then", because it plays the animation
        *self* then *other*.
        Args:
            other (Anim): The animation to add after the current one.
        Returns:
            Anim: The new animation that is *self* then *other*.
        """
        if not isinstance(other, Anim):
            other = Anim(self.frame, other)
        return Anim(self.frame, self.anim + other.anim)


if __name__ == "__main__":
    F = "the frame"
    A = Anim(F, [("A",), ("a",), ("Ah",), ("ah",)], after=2)
    B = Anim(F, [("b", "B"), ("beh", "Beh"), ("beh", "BEH")])
    print(A)
    print(B)
    print(A>>B)
    print(A<<B)
    print(A&B)

