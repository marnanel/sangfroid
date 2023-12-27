import bs4
from sangfroid.value.value import Value

@Value.handles_type()
class Vector(Value):

    # it may happen that other types occur, though I don't
    # know of any at present, or how we could know if they
    # applied to us
    our_type = float

    @property
    def value(self):
        return dict(
                [(field.name,
                  field.string)
                 for field in self.tag.children
                 if isinstance(field, bs4.element.Tag)
                 ])

    def _raise_type_error(self):
        raise TypeError(
                "Vectors may be constructed as Vector(x,y), or "
                "Vector(dict_of_members).")

    @value.setter
    def value(self, v):

        if isinstance(v, tuple):
            if len(v)==0:
                members = {}
            elif len(v)==2:
                members = dict(zip('xy', v))

                if not (
                        isinstance(members['x'], (float, int)) and
                        isinstance(members['y'], (float, int))
                        ):
                    self._raise_type_error()

            else:
                self._raise_type_error()
        elif hasattr(v, 'items'):
            members = v
        else:
            self._raise_type_error()

        self.tag.name = self.__class__.__name__.lower()
        self.tag.attrs = {}

        for k, v in members.items():
            addendum = bs4.element.Tag(name=k)
            addendum.string = str(v)
            self.tag.append(addendum)

    def __getitem__(self, key):
        result = self.get(key, default=None)

        if result is None:
            raise KeyError(key)

        return result

    def get(self, key, default=None):
        if isinstance(key, int):
            key = self.keys()[key]

        v = [field.string
             for field in self.tag.children
             if isinstance(field, bs4.element.Tag)
             and field.name==key
             ]

        if len(v)==0:
            return default

        return self.our_type(v[0])

    # FIXME: All these methods are written in terms of self.value,
    # which is inefficient because all the values must be created
    # every time. They should be fixed to read self.tag themselves.

    def keys(self):
        return sorted(self.value.keys())

    def values(self):
        return [self.our_type(v) for v in self.value.values()]

    def items(self):
        return [(k, self.our_type(v)) for k,v in self.value.items()]

    def __len__(self):
        return len(self.value)

    def as_tuple(self):
        return tuple(
                [self.our_type(self.value[k])
                 for k in sorted(self.value.keys())]
                )

    def _str_inner(self):
        if sorted(self.value.keys())==['x', 'y']:
            return str(self.as_tuple())
        else:
            return str(self.value)

    def __eq__(self, other):
        try:
            if len(other)!=len(self):
                return False
        except TypeError:
            return False

        return all([left==right for left,right in zip(self, other)])

    def __iter__(self):
        for v in self.values():
            yield v

@Value.handles_type()
class Composite(Value):
    @property
    def value(self):
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

        return dict(
                [name_and_value(field)
                 for field in self.tag.children
                 if isinstance(field, bs4.element.Tag)
                 ])

    def __getitem__(self, key):
        result = self.get(key=key, default=None)
        if result is None:
            raise KeyError(key)
        return result

    def get(self, key, default=None):
        found = [v
                 for v in self.tag.children
                 if isinstance(v, bs4.element.Tag)
                 and v.name==key
                 ]

        if len(found)==0:
            return default
        elif len(found)>1:
            raise ValueError(f"multiple values for {key}!")

        values = [v
                 for v in found[0].children
                 if isinstance(v, bs4.element.Tag)
                 ]

        if len(values)==0:
            return default
        elif len(values)>1:
            raise ValueError(f"multiple values for {key}!")
        elif values[0]==None:
            return default
        else:
            return Value.from_tag(values[0])

    def keys(self):
        # No point constructing all the values
        return [v.name
                 for v in self.tag.children
                 if isinstance(v, bs4.element.Tag)
                 ]

    def values(self):
        return self.value.values()

    def items(self):
        return self.value.items()

    def __len__(self):
        return len([v
                 for v in self.tag.children
                 if isinstance(v, bs4.element.Tag)
                 ])

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
