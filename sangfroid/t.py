import math
import functools
import re

@functools.total_ordering
class T:
    """
    An instant during an animation.

    This can be expressed either as a number of frames or as a number
    of seconds, both measured from the start of the animation.
    In both cases, it's a float, usually but not always integral.

    The time may be specified in one of four ways, where `F` represents
    any decimal integer or float:

        - an `int` or `float`, giving the number of frames counting forwards
          from the start of the animation. But if the number is negative,
          it counts backwards from the end, in the usual Python indexing style.

        - `"Ff"`

        - `"Fs"`

        - `"Fs Ff"`, in which case the values are added together.

    For the reference_tag parameter, you may supply the root Beautiful Soup
    tag of an animation, or any of that tag's descendants. If this parameter
    is unspecified, or `None`, but we need to calculate something from it,
    we throw `ValueError`.

    There are two reasons you might need to specify a reference_tag:

        - If the specification is `int` or `float`, and it's negative;
          this is because we will need to look up the animation length.

        - If the specification is given as `"Fs"` or `"Fs Ff"`;
          this is because we need to look up the speed in frames per second.
          It's almost always 24. The reason we don't default to 24 is that
          it risks introducing subtle bugs which are only discovered when
          the actual frame rate isn't 24.

    However, if the time is zero (that is, at the start of the animation),
    you may write it as `"0s"` or `"0s 0f"` even if you don't supply
    the reference_tag.  This doesn't allow you to write `"0s 2f"` without
    supplying the reference_tag, even though the FPS wouldn't make
    a difference, because edge cases give rise to bugs.

    Ts compare numerically to other Ts, but unless the frame
    count is zero, they must have the same FPS.

    The number of seconds in a `"Fs"` or `"Fs Ff"` may be negative,
    which allows you to set times before the start of the animation.
    However, the number of *frames* in a `"Fs Ff"` specification
    may not be negative.

    In time specifications giving both seconds and frames, the number
    of frames may be equal to or higher than the FPS. (So, for example,
    `"2s 48f"` is a valid time even if `fps=24`, when it's equivalent
    to `"4s`"`.)

    This type is immutable and hashable.

    Attrs:
        _frames (float): distance in frames from the start of the animation
        _fps (float or None): speed in frames per second, if known
    """
    def __init__(
            self,
            value=0.0,
            reference_tag = None,
            ):
 
        if reference_tag is None:
            self._fps = None
        else:
            root_tag = _canvas_root(reference_tag)
            if root_tag is None:
                self._fps = None
            else:
                self._fps = float(root_tag['fps'])
            
                if self._fps<=0.0:
                    raise ValueError(f"FPS must be positive: {self._fps}")

        try:
            if isinstance(value, str):
                self._frames = self._parse_time_spec(value)
            else:
                self._frames = float(value)

                if self._frames < 0:
                    if root_tag is None:
                        raise ValueError("Negative frame counts require "
                                         "an anchored reference_tag.")

                    animation_duration = 1+(
                            self._parse_time_spec(
                                root_tag.attrs['end-time'],
                                )
                            - 
                            self._parse_time_spec(
                                root_tag.attrs['begin-time'],
                                )
                            )

                    self._frames = animation_duration + self._frames

        except TypeError:
            raise ValueError(f"Invalid time specification: {value}")

        assert isinstance(self._frames, float)

    def _parse_time_spec(self, s):
        assert isinstance(s, str)

        def complain():
            raise ValueError(
                    f"bad time specification: {s}")

        s = s.strip()

        seconds = None
        frames = 0.0

        found = TIMESPEC_RE.fullmatch(s)
        if found is None:
            complain()

        result = 0.0

        if found.group(2) is None and found.group(3) is None:
            complain()

        if found.group(2) is not None:
            seconds = float(found.group(2))

            if seconds!=0.0:
                if self._fps is None:
                    raise ValueError("Time specifications in seconds require "
                                     "an anchored reference_tag.")
                result += seconds * self._fps

        if found.group(3) is not None:
            result += float(found.group(3))

        if found.group(1)=='-':
            result = -result

        return result

    @property
    def frames(self):
        """
        Time in frames.
        """
        return self._frames

    @property
    def fps(self):
        """
        Speed of the film, in frames per second. Always a positive float,
        or None if we don't know the speed.
        """
        return self._fps

    def __int__(self):
        return int(self._frames)

    def __float__(self):
        return self._frames

    @property
    def seconds(self):
        """
        Time in seconds.

        Raises:
            ValueError: if we don't know the FPS.
        """
        if self.fps is None:
            if self._frames==0.0:
                return 0.0
            else:
                raise ValueError(
                        "If you want to measure time in seconds, "
                        "you will need to specify the FPS.")
        return self._frames / self.fps

    def _compare(self, other, operator):

        if isinstance(other, self.__class__):
            if (
                    other.fps is not None and
                    self.fps is not None and
                    other.fps!=self.fps):
                raise ValueError(
                        "Comparison between two Ts with different FPS: "
                        f"{self}, {other}"
                        )

            other_f = other.frames
        elif isinstance(other, (float, int)):
            other_f = other
        else:
            return False

        return operator(self._frames, other_f)

    def __lt__(self, other):
        return self._compare(other, lambda a,b:a<b)

    def __eq__(self, other):
        return self._compare(other, lambda a,b:a==b)

    def __str__(self):
        if self._fps is None or abs(self._frames) < self._fps:
            return '%gf' % (self._frames, )


        result = '%gs' % (
            (abs(self._frames) // self._fps) * (
                math.copysign(1, self._frames))
            )
        if (self._frames % self._fps)!=0:
            result += ' %gf' % (
                    abs(self._frames % math.copysign(self._fps, self._frames)),
                    )

        return result

    __repr__ = __str__

    def __hash__(self):
        if self._frames == 0:
            return 0

        s = f'{self._frames} {self._fps}'
        return hash(s)

# It doesn't matter that you can produce invalid decimals with this regex:
# that will be discovered when we do the float conversion.
TIMESPEC_RE = re.compile(
        r'(-?)'
        r'(?:([0-9.]+)s)?'
        r' ?'
        r'(?:([0-9.]+)f)?'
        )

def _canvas_root(tag):
    parents = tag.find_parents()

    if len(parents)==0:
        return None
    elif len(parents)==1:
        root = tag
    else:
        root = parents[-2] # -1 is "document", the anon root tag

    if root.name=='canvas':
        return root
    else:
        return None

__all__ = [
        'T',
        ]
