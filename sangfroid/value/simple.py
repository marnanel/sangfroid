from sangfroid.value.value import Value
from sangfroid.t import T

NEAR_AS_DAMMIT = 0.0001

class Simple(Value):

    our_type = None

    @property
    def value(self):
        if self.our_type is None:
            raise NotImplementedError()

        result = self._tag.get('value', None)
        if result is None:
            raise ValueError(f"value tag had no value: {self._tag}")

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

        self._tag.name = self.__class__.__name__.lower()
        self._tag.attrs = {
                'value': result,
                }
        self._tag.clear()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            v = other.value
        else:
            try:
                v = self.our_type(other)
            except ValueError:
                v = other

        try:
            return abs(self.value-v)<=NEAR_AS_DAMMIT
        except TypeError:
            return False

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
                reference_tag = self._tag,
                )
