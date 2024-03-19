import bs4
from sangfroid.value.value import Value
from sangfroid.t import T

@Value.handles_type()
class String(Value):
    our_type = str

    @property
    def value(self):
        result = str(self.tag.string)
        return result

    @value.setter
    def value(self, v):
        self.tag.string = str(v)
