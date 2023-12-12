import bs4
from sangfroid.value.value import Value
from sangfroid.time import Time as TimeType
from sangfroid.utils import tag_to_fps

class Simple(Value):

    our_type = None

    def _set_value(self):
        if self.our_type is None:
            raise NotImplementedError()

        result = self.tag.get('value', None)
        if result is None:
            raise ValueError(f"value tag had no value: {self.tag}")

        self._value = self._construct_value(result)

    def _construct_value(self, v):
        return self.our_type(v)

    def _make_tag_from_args(self, args):
        if len(args)!=1:
            raise ValueError(
                    f"{self.__class__.__name__} takes a single argument")

        result = bs4.element.Tag(name=self.__class__.__name__.lower())
        result['value'] = str(args[0])

        return result

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
        return '%g°' % (self._value,)

@Value.handles_type()
class String(Simple):
    our_type = str

@Value.handles_type()
class Time(Simple):
    our_type = TimeType

    def _construct_value(self, v):
        return self.our_type(
                v,
                fps = tag_to_fps(self.tag),
                )
