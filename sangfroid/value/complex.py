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

    @property
    def value(self):
        return self._value

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
        super().__init__(tag)

        def name_and_value(n):

            name = n.name
            print("9100", tag.name, name)

            assert name!='layer'

            value_tags = [v
                 for v in n.children
                 if isinstance(v, bs4.element.Tag)
                 ]

            if len(value_tags)!=1:
                raise ValueError("Fields in composite types should only "
                                 f"have a single value: {n}")

            value = Value.from_tag(value_tags[0])

            return name, value

        self._value = dict(
                [name_and_value(field)
                 for field in tag.children
                 if isinstance(field, bs4.element.Tag)
                 ])

@Value.handles_type()
class Canvas(Value):
    def __init__(self, tag):
        super().__init__(tag)
        self._value = [field
                 for field in tag.children
                 if isinstance(field, bs4.element.Tag)
                 ]
