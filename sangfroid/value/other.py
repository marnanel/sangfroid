import bs4
from sangfroid.value.value import Value

@Value.handles_type()
class Color(Value):
    def __init__(self, tag):
        super().__init__(tag)

        for field in 'rgba':
            setattr(self, field,
                    float(tag(field)[0].string),
                    )

    @property
    def value(self):
        result = '%02x%02x%02x%02x' % (
                int(self.r*256),
                int(self.g*256),
                int(self.b*256),
                int(self.a*256),
                )
        return result

    @value.setter
    def value(self, v):

        def _raise_format_error():
            raise ValueError(
                    "Express a colour value as (r,g,b), or (r,g,b,a), or "
                    "as a string of six or eight hex digits."
                    )

        if isinstance(v, tuple):
            if len(v) not in (3,4):
                _raise_format_error()

            if len(v)==3:
                v = (v[0], v[1], v[2], 1.0)

            for i, field in enumerate('rgba'):
                setattr(self, field, float(v[i]))

        elif isinstance(v, str):
            if len(v) not in (6,8):
                _raise_format_error()

            if len(v)==6:
                v += 'FF'

            for i, field in enumerate('rgba'):
                setattr(self, field,
                        int(field[i*2:i*2+1], 16))
        else:
            _raise_format_error()

@Value.handles_type()
class Gradient(Value):
    def __init__(self, tag):
        super().__init__(tag)

        colours = tag.find_all('color')
        if len(colours)!=2:
            raise ValueError("there should be two colours in a gradient")

        self.first = Color(colours[0])
        self.second = Color(colours[1])
        for field in 'rgba':
            setattr(self, field,
                    float(tag(field).string),
                    )

    @property
    def value(self):
        return (self.first, self.second)

    @value.setter
    def value(self, v):
        if not isinstance(v, (Tuple, List)) or len(v)!=2:
            raise ValueError("A gradient should contain two colours")

        self.first = Color(colours[0])
        self.second = Color(colours[1])

@Value.handles_type()
class Bline(Value):
    def __init__(self, tag):
        raise ValueError("do this later")

@Value.handles_type()
class Canvas(Value):
    def __init__(self, tag):
        raise ValueError("do this later")

