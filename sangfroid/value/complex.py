import bs4
from sangfroid.value.value import Value

RGBA = 'rgba'

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

    @value.setter
    def value(self, v):

        def _raise_type_error():
            raise TypeError(
                    "Vectors may be constructed as Vector(x,y), or "
                    "Vector(dict_of_members).")

        if len(v)==0:
            members = {}
        elif len(v)==1:
            members = v[0]
            if not hasattr(members, 'items'):
                self._raise_type_error()
        elif len(v)==2:
            members = dict(zip('xy', v))

            if not (
                    isinstance(members['x'], (float, int)) and
                    isinstance(members['y'], (float, int))
                    ):
                self._raise_type_error()

        else:
            self._raise_type_error()

        self.tag.name = self.__class__.__name__.lower()
        self.tag.attrs = {}

        for k, v in members.items():
            addendum = bs4.element.Tag(name=k)
            addendum.string = str(v)
            self.tag.append(addendum)

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

    # FIXME: All these methods are written in terms of self.value,
    # which is inefficient because all the values must be created
    # every time. They should be fixed to read self.tag themselves.

    def keys(self):
        return sorted(self.value.keys())

    def values(self):
        return [self.our_type(v) for v in self.value.values()]

    def items(self):
        return [(k, self.our_type(v)) for k,v in self_value.items()]

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

@Value.handles_type()
class Color(Value):

    @property
    def value(self):
        result = '#' + (''.join([
                '%02x' % (int(float(self.tag(dimension)[0].string)*255),)
            for dimension in RGBA
            ]))

        if result.endswith('ff'):
            result = result[:-2]
        return result

    def as_tuple(self):
        result = tuple([
            float(self.tag(dimension)[0].string)
            for dimension in RGBA
            ])
        return result

    def __eq__(self, other):

        if isinstance(other, Color):
            return self.value == other.value
        elif isinstance(other, str):
            other = other.lower()
            if not other.startswith('#'):
                other = f'#{other}'
            if len(other)==9 and other.endswith('ff'):
                other = other[:-2]
            return str(self) == other
        elif isinstance(other, tuple):
            if len(other)==3:
                other = other+(1.0,)
            return self.as_tuple() == other
        else:
            return False

    @value.setter
    def value(self, v):

        def _raise_format_error():
            raise ValueError(
                    "Express a colour value as (r,g,b), or (r,g,b,a), or "
                    f"as a string of six or eight hex digits: {v}"
                    )

        if isinstance(v, tuple):

            if len(v)==0:
                result = (1.0, 1.0, 1.0, 1.0)
            elif len(v)==3:
                result = v + (1.0,)
            elif len(v)==4:
                result = v
            else:
                _raise_format_error()

        elif isinstance(v, str):
            if v.startswith('#'):
                v = v[1:]

            if len(v)==6:
                v += 'FF'
            elif len(v)==8:
                pass
            else:
                _raise_format_error()

            result = tuple(
                int(v[i*2:i*2+2], 16)/255
                for i in range(4))
        else:
            _raise_format_error()

        assert isinstance(result, tuple), result
        assert [type(n) for n in result]==[float]*4, result

        self.tag.name = __class__.__name__.lower()
        self.tag.attrs = {}
        self.tag.clear()

        for i, dimension in enumerate(RGBA):
            dimension_tag = bs4.element.Tag(name=dimension)
            dimension_tag.string = '%.06f' % (result[i],)
            self.tag.append(dimension_tag)
