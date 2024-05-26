import bs4
from sangfroid.value.value import Value

@Value.handles_type()
class Composite(Value):

    REQUIRED_KEYS = None

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

        result = dict(
                [name_and_value(field)
                 for field in self._tag.children
                 if isinstance(field, bs4.element.Tag)
                 ])

        if self.REQUIRED_KEYS is not None:
            assert keys(result)==self.REQUIRED_KEYS

        return result

    @value.setter
    def value(self, new_value):

        for k,v in new_value.items():
            if self.REQUIRED_KEYS is not None:
                if k not in self.REQUIRED_KEYS:
                    raise KeyError(
                    f"{k} is not one of the keys we can accept. "
                    f"We can accept: {' '.join(sorted(self.REQUIRED_KEYS))}")

                # XXX TO HERE

        raise ValueError(new_value)

    def __getattr__(self, key):
        result = self.get(key, default=None)

        if result is None:
            raise AttributeError(key)

        return result

    def __getitem__(self, key):
        result = self.get(key=key, default=None)
        if result is None:
            raise KeyError(key)
        return result

    def get(self, key, default=None):
        found = [v
                 for v in self._tag.children
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
                 for v in self._tag.children
                 if isinstance(v, bs4.element.Tag)
                 ]

    def values(self):
        return self.value.values()

    def items(self):
        return self.value.items()

    def __len__(self):
        return len([v
                 for v in self._tag.children
                 if isinstance(v, bs4.element.Tag)
                 ])

    def __eq__(self, other):

        if len(other)!=len(self):
            return False

        for key, value in self.items():
            if other[key]!=value:
                return False

        return True

    def as_python_expression(self):
        value = self.value

        result = '{\n'
        for f,v in value.items():
            result += '     %40s: %s,\n' % (
                    repr(f),
                    v.as_python_expression(),
                    )
        result += (' '*36) + '}'

        return result

class Transformation(Composite):
    REQUIRED_KEYS = {
            'offset',
            'angle',
            'skew_angle',
            'scale',
            }
