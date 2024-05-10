import bs4
import sangfroid.value as v

class Field:
    def __init__(self,
                 name,
                 type_,
                 default,
                 in_params = None,
                 doc = None,
                 ):
        self.type_ = type_
        self.default = default
        self.name = name

        if in_params is None:
            self.in_params = issubclass(type_, v.Value)
        else:
            self.in_params = in_params

        self.__doc__ = doc or ''
        self.__doc__ += f"\n\nType: {type_}"
        if default is not None:
            # yes, this is the right way round; think about it
            self.__doc__ += ' or None'

    def read_from(self, tag):
        if self.in_params:
            return self._get_param(self.name)
        else:
            value = tag.get(self.name, None)

            if value is None:
                return None
            elif issubclass(self.type_, bool):
                return str(bool(value)).lower()
            else:
                return str(value)

    def __str__(self):

        result = f'[{self.name} '

        if self.in_params:
            result += 'param '
        else:
            result += 'attr  '

        result += '%20s' % (self.type_,)

        result += ']'

        return result

    __repr__ = __str__

    @classmethod
    def put_in_layer(cls, *fields):

        def _inner(layer_class):

            assert all([isinstance(f, cls) for f in fields]), (
                    [type(f) for f in fields if not isinstance(f, cls)])

            result = dict([
                (field.name, field)
                for field in fields
                ])

            layer_class.FIELDS = result

            return layer_class

        return _inner

class TagField(Field):
    def __init__(self):
        super().__init__(
                name = 'tag',
                type_ = bs4.Tag,
                default = None,
                doc = """The BeautifulSoup tag behind this item.""",
                )
 
    def read_from(self, tag):
        return tag

    def write_to(self, tag, value):
        raise KeyError("You can't change a layer's tag.")

class NamedChildField(Field):
    def __init__(self, name, doc=None):
        super().__init__(
                name = name,
                type_ = str,
                default = None,
                doc = doc,
                )

    def get_subtag(self, tag):
        return tag.find(self.name)
 
    def read_from(self, tag):

        subtag = self.get_subtag(tag)

        if subtag is None:
            return ''
        else:
            return subtag.string

        raise ValueError()

    def write_to(self, tag, value):

        subtag = self.get_subtag(tag)

        subtag.string = value

def ClassWithFields(type):
    def __dir__(self):
        raise ValueError()
