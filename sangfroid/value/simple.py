from sangfroid.value.value import Value
from sangfroid.t import T
import warnings

NEAR_AS_DAMMIT = 0.0001

class Simple(Value):

    our_type = None

    @property
    def value(self):
        if self.our_type is None:
            raise NotImplementedError()

        print("9111", str(self._tag))
        result = self._tag.get('value', None)
        if result is None:
            raise ValueError(
                    f"This tag should have had a 'value' attribute, "
                    f"but it didn't:\n\n"
                    f"{self._tag}")
        assert isinstance(result, str), f"{result} {type(result)} {self._tag} {type(self._tag)}"

        print("9111", self._tag, result, type(result))
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
                'value': str(result),
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

        return self._compare_with(v)

    def _compare_with(self, v):
        return self.value==v

class Numeric(Simple):
    def __float__(self):
        return float(self.value)

    def __int__(self):
        return int(self.value)

@Value.handles_type()
class Real(Numeric):
    our_type = float

    def _compare_with(self, v):
        try:
            return abs(self.value-v)<=NEAR_AS_DAMMIT
        except TypeError:
            return False

@Value.handles_type()
class Integer(Numeric):
    our_type = int

@Value.handles_type()
class Bool(Simple):
    our_type = bool

    def __bool__(self):
        return self.value

    def _construct_value(self, v):
        assert isinstance(v, str)
        if v.lower()=='true':
            return True
        elif v.lower()=='false':
            return False
        else:
            warnings.warn(
                    "boolean string should have been 'true' or 'false', "
                    f"but it was {repr(v)}; treating as False.")
            return False

@Value.handles_type()
class Angle(Simple):
    our_type = float

    def _str_inner(self):
        return '%g°' % (self.value,)

    def as_python_expression(self):
        v = self.value
        return str(v)

    def __float__(self):
        return float(self.value)

@Value.handles_type()
class Time(Simple):
    our_type = T

    # We don't provide __float__ and __int__ here because
    # they'd be ambiguous between frames and seconds.

    def _construct_value(self, v):
        return self.our_type(
                v,
                reference_tag = self._tag,
                )

    def as_python_expression(self):
        v = self.value

        if v==0:
            return 0
        else:
            return repr(str(v))
