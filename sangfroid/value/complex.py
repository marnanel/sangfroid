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

    def _make_tag_from_args(self, args):
        result = bs4.element.Tag(name=__class__.__name__.lower())

        if isinstance(args, (list, tuple)) and len(args)==2:
            args = dict(zip('xy', args))

        for k, v in args.items():
            addendum = bs4.element.Tag(name=k)
            addendum.string = str(v)
            result.append(addendum)

        return result

    @property
    def value(self):
        return self._value

    def __getitem__(self, item):
        if isinstance(item, int):
            item = self.keys()[item]

        return self.our_type(self._value[item])

    def get(self, value, default=None):
        try:
            result = self._value[value]
        except KeyError:
            return default

        return self.our_type(result)

    def keys(self):
        return sorted(self._value.keys())

    def values(self):
        return [self.our_type(v) for v in self._value.values()]

    def items(self):
        return [(k, self.our_type(v)) for k,v in self._value.items()]

    def __len__(self):
        return len(self._value)

    def as_tuple(self):
        return tuple(
                [self.our_type(self._value[k])
                 for k in sorted(self._value.keys())]
                )

    def _str_inner(self):
        return str(self.as_tuple())

    def __eq__(self, other):
        try:
            if len(other)!=len(self):
                return False
        except TypeError:
            return False

        return all([left==right for left,right in zip(self, other)])

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

    def __getitem__(self, *args, **kwargs):
        return self._value.__getitem__(*args, **kwargs)

    def get(self, value, default=None):
        result = self._value.get(value, None)
        if result is None:
            return default
        else:
            return result

    def keys(self):
        return self._value.keys()

    def values(self):
        return self._value.values()

    def items(self):
        return self._value.items()

    def __len__(self):
        return len(self._value)

    def __eq__(self, other):


        if len(other)!=len(self):
            return False

        for key, value in self.items():
            if other[key]!=value:
                return False

        return True

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
