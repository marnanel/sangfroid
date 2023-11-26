import bs4
from sangfroid.value.value import Value

@Value.handles_type()
class Vector(Value):
    def __init__(self, tag):
        super().__init__(tag)

        self._value = dict(
                [(field.name,
                  field.string)
                 for field in tag.children
                 if isinstance(field, bs4.element.Tag)
                 ])

@Value.handles_type()
class Dynamic_List(Value):
    def __init__(self, tag):
        raise ValueError("do this later")

@Value.handles_type()
class Static_List(Value):
    def __init__(self, tag):
        raise ValueError("do this later")

@Value.handles_type()
class Wplist(Value):
    def __init__(self, tag):
        raise ValueError("do this later")

@Value.handles_type()
class Dilist(Value):
    def __init__(self, tag):
        raise ValueError("do this later")

@Value.handles_type()
class Composite(Value):
    def __init__(self, tag):
        raise ValueError("do this later")


