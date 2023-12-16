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

    The time may be specified in one of four ways, where "F" represents
    any decimal integer or float:
        - a float, the number of frames
        - "Ff"
        - "Fs"
        - "Fs Ff", in which case the values are added together.

    For types involving seconds, the FPS must be supplied to the constructor.
    You can find this using the "fps" property of the Animation.
    It's almost always 24. The reason we don't default to 24 is that
    it risks introducing subtle bugs which are only discovered when
    the actual frame rate isn't 24.

    However, if the time is zero (that is, the start of the film), you may
    write it as "0s" or "0s 0f" even if you don't supply the FPS.
    This doesn't allow you to write "0s 2f" without supplying the FPS,
    even though the FPS wouldn't make a difference, because edge cases
    give rise to bugs.

    Ts compare numerically to other Ts, but unless the frame
    count is zero, they must have the same FPS.

    Ts may be negative. However, in time specifications giving
    both the seconds and the frames, the frame count may not be negative.

    In time specifications giving both seconds and frames, the number
    of frames may be equal to or higher than the FPS. (So, for example,
    "2s 48f" is a valid time even if fps=24, when it's equivalent to "4s".)

    This type is immutable and hashable.
    """
    def __init__(
            self,
            value=0.0,
            fps = None,
            ):
        """
        Constructor.

        Args:
            value (str, or float): the time. See the type docstring.
            fps (int, or None): the number of frames per second.
                If "value" contains a number of seconds, and this
                is None, it raises ValueError.
        """
 
        self._fps = fps

        try:
            if isinstance(value, str):
                self._frames = self._parse_time_spec(value)
            else:
                self._frames = float(value)
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
            if self._fps is not None:
                result += seconds * self._fps
            elif seconds!=0:
                raise ValueError(
                        "If you specify a number of seconds, you "
                        f"must also specify the FPS: {s}")

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
        Speed of the film, in frames per seconds. Always a positive integer,
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
