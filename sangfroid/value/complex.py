import bs4
from sangfroid.value.value import Value

@Value.handles_type()
class Vector(Value):

    # it may happen that other types occur, though I don't
    # know of any at present, or how we could know if they
    # applied to us
    our_type = float

    def _set_value(self):
        self._value = dict(
                [(field.name,
                  field.string)
                 for field in self.tag.children
                 if isinstance(field, bs4.element.Tag)
                 ])

    @property
    def value(self):
        return self._value

    def __getitem__(self, *args, **kwargs):
        return self.our_type(self._value.__getitem__(*args, **kwargs))

    def get(self, value, default=None):
        result = self._value.get(value, None)
        if result is None:
            return default
        else:
            return self.our_type(result)

    def keys(self):
        return self._value.keys()

    def values(self):
        return [self.our_type(v) for v in self._value.values()]

    def items(self):
        return [(k, self.our_type(v)) for k,v in self._value.items()]

@Value.handles_type()
class Dynamic_List(Value):
    def _set_value(self):
        raise ValueError("do this later")

@Value.handles_type()
class Static_List(Value):
    def _set_value(self):
        raise ValueError("do this later")

@Value.handles_type()
class Wplist(Value):
    def _set_value(self):
        raise ValueError("do this later")

@Value.handles_type()
class Dilist(Value):
    def _set_value(self):
        raise ValueError("do this later")

@Value.handles_type()
class Composite(Value):
    def _set_value(self):

        def name_and_value(n):

            name = n.name

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
                 for field in self.tag.children
                 if isinstance(field, bs4.element.Tag)
                 ])

        for name in ['items', 'values', 'keys', 'get', '__getitem__']:
            setattr(self, name, getattr(self._value, name))

@Value.handles_type()
class Canvas(Value):
    def _set_value(self):
        from sangfroid.layer.layer import Layer
        layers = [field
                 for field in self.tag.children
                 if isinstance(field, bs4.element.Tag)
                 ]
        if len([n for n in layers if n.name!='layer'])!=0:
            raise ValueError(
                    f"Only layers can be the children of a canvas: {self.tag}"
                    )

        self._value = [Layer.from_tag(layer) for layer in layers]
