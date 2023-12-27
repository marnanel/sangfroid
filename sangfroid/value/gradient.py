import bs4
from sangfroid.value.value import Value
from sangfroid.value.color import Color

@Value.handles_type()
class Gradient(Value):
    @property
    def value(self):
        colours = self.tag.find_all('color')
        if len(colours)<2:
            self._raise_colour_count_error()

        self._value = [
                Color(c) for c in colours
                ]

        return self._value

    @value.setter
    def value(self, v):
        if not isinstance(v, (tuple, list)) or len(v)<2:
            self._raise_colour_count_error()

        def normalise(c):
            if isinstance(c, Color):
                return c
            return Color(c)

        v = [Color(c) for c in v]

        self.tag.clear()

        for i, colour in enumerate(v):
            colour_tag = colour.tag
            colour_tag['pos'] = '%.06f' % (i,) # yes, 6dp for an integer
            self.tag.append(colour_tag)

    def _raise_colour_count_error(self):
        raise ValueError("there should be at least two colours in a gradient")

    def __len__(self):
        return len(self.value)

    def __getitem__(self, n):
        return self.value[n]

    def __setitem__(self, n, v):
        previous = self.value
        previous[n] = v
        self.value = previous

    def __str__(self):
        return (
                '[' +
                ','.join([str(c) for c in self.value]) +
                ']')
