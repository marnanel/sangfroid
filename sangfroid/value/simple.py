from sangfroid.value.value import Value
from sangfroid.time import Time as TimeType

class Simple(Value):

    our_type = None

    def _set_value(self):
        if self.our_type is None:
            raise NotImplementedError()

        self._value = self.our_type(self.value)

    @property
    def value(self):
        result = self.tag.get('value', None)
        if result is None:
            raise ValueError(f"value tag had no value: {self.tag}")
        return self.our_type(result)

@Value.handles_type()
class Real(Simple):
    our_type = float

@Value.handles_type()
class Integer(Simple):
    our_type = int

@Value.handles_type()
class Bool(Simple):
    our_type = bool

@Value.handles_type()
class Angle(Simple):
    our_type = float

@Value.handles_type()
class String(Simple):
    our_type = str

@Value.handles_type()
class Time(Simple):
    our_type = TimeType
