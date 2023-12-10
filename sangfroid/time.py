import math
import functools

DEFAULT_FPS = 24

@functools.total_ordering
class Time:
    def __init__(
            self,
            *args,
            **kwargs,
            ):
        """Args can be:
            - a string consisting of a decimal int or float, followed
                by "s" for seconds or "f" for frames; if frames, it will
                be converted to int
             - an int, giving the number of frames

           Kwargs can be:
             - fps: the number of frames per seconds, used for seconds/frames
                  conversion; defaults to 24
        """
 
        fps = kwargs.get('fps', DEFAULT_FPS)
        self._frames = None
        self._seconds = None

        if len(args)==1:
            if isinstance(args[0], str):
                self._frames, self._seconds = self._parse_time_spec(args[0])
            else:
                try:
                    self._frames = int(args[0])
                except TypeError:
                    self._constructor_type_error()

        assert (self._frames is None) != (self._seconds is None)

        if self._frames is None:
            self._frames = int(self._seconds * fps)
        else:
            self._seconds = float(self._frames / fps)

        assert isinstance(self._frames, int)
        assert isinstance(self._seconds, float)

    def _parse_time_spec(self, s):
        assert isinstance(s, str)

        s = s.strip()
        try:
            if s.endswith('f'):
                return int(s[:-1]), None
            elif s.endswith('s'):
                return None, float(s[:-1])
            else:
                return int(s), None
        except ValueError:
            raise ValueError(
                    f"bad time specification: {s}")

    @property
    def frames(self):
        return self._frames

    def __int__(self):
        return self._frames

    @property
    def seconds(self):
        return self._seconds

    def __float__(self):
        return self._seconds

    def _compare(self, other, operator):
        result1 = operator(self._frames, other._frames)
        result2 = operator(self._seconds, other._seconds)

        if result1!=result2:
            raise ValueError(
                    "Comparison between two Times with different FPS")

        return result1

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(
                    "No comparison is possible between "
                    f"Time and {type(other)}")

        return self._compare(other, lambda a,b:a<b)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        return self._compare(other, lambda a,b:a==b)

    def __str__(self):
        return f"{self._frames}f"

    __repr__ = __str__
