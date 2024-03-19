from sangfroid.value.value import Value
from sangfroid.t import T

class Simple(Value):

    our_type = None

    @property
    def value(self):
        if self.our_type is None:
            raise NotImplementedError()

        result = self.tag.get('value', None)
        if result is None:
            raise ValueError(f"value tag had no value: {self.tag}")

        result = self._construct_value(result)

        return result

    def _construct_value(self, v):
        return self.our_type(v)

    @value.setter
    def value(self, v):
        if self.our_type is None:
            raise NotImplementedError()

        if v==() or v is None:
            result = self.our_type()

        else:
            try:
                result = self.our_type(v)
            except TypeError:
                raise TypeError("I need a value of type "
                                f"{self.our_type.__name__}, "
                                "not "
                                f"{v.__class__.__name__}."
                                )

        self.tag.name = self.__class__.__name__.lower()
        self.tag.attrs = {
                'value': result,
                }
        self.tag.clear()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value
        else:
            return self.value == other

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

    def _str_inner(self):
        return '%g°' % (self.value,)

@Value.handles_type()
class Time(Simple):
    our_type = T

    def _construct_value(self, v):
        return self.our_type(
                v,
                reference_tag = self.tag,
                )
