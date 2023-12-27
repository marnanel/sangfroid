import bs4
from sangfroid.value.value import Value

@Value.handles_type()
class Gradient(Value):
    def _set_value(self):
        colours = self.tag.find_all('color')
        if len(colours)!=2:
            raise ValueError("there should be two colours in a gradient")

        self._value = (
                Color(colours[0]),
                Color(colours[1]),
                )

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if not isinstance(v, (Tuple, List)) or len(v)!=2:
            raise ValueError("A gradient should contain two colours")

        self._value = (v[0], v[1])
