import math

DEFAULT_FPS = 24

# XXX parse value

class Time:
    def __init__(
            *args,
            **kwargs,
            ):
        """Args can be:
            - a string consisting of a decimal int or float, followed
                by "s" for seconds or "f" for frames; if frames, it will
                be converted to int
             - an int, giving the number of frames

           Kwargs can be:
             - frames: the number of frames; it will be converted to int
             - seconds: the number of seconds; cannot be used with "frames"
             - fps: the number of frames per seconds, used for seconds/frames
                  conversion; defaults to 24
        """
 
        fps = kwargs.get('fps', DEFAULT_FPS)
        self._frames = None
        self._seconds = None

        if len(args)==1:
            if isinstance(args[0], str):
                self._frames, self._seconds = self.parse_time_spec(
                        fps = fps,
                        )
            else:
                try:
                    self._frames = int(args[0])
                except TypeError:
                    self._constructor_type_error()

        if 'frames' in kwargs:
            if 'seconds' in kwargs:
                self._raise_constructor_type_error()

            self._frames = math.floor(kwargs['frames'])
        else:
            self._seconds = kwargs['seconds']

        assert (self._frames is None) != (self._seconds is None)

        if self._frames is None:
            self._seconds = self._frames * fps
        else:
            self._frames = self._seconds // fps

    @property
    def frames(self):
        return self._frames

    @property
    def seconds(self):
        return self._seconds

    def _raise_constructor_type_error(self):
        raise ValueError(self.__init__.__doc__)

    def __str__(self):
        return "{self._frames}f"
