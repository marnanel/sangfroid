import bs4
import sangfroid.value as v

FIELDS_NAME = 'FIELDS'

class Field:
    def __init__(self,
                 name,
                 type_,
                 default,
                 doc = None,
                 ):
        self.type_ = type_
        self.default = default
        self.name = name
        self.default = default

        self.__doc__ = doc or ''
        self.__doc__ += f"\n\nType: {type_}"
        if default is not None:
            # yes, this is the right way round; think about it
            self.__doc__ += ' or None'

    def read_from(self, obj):
        raise NotImplementedError()

    def write_to(self, obj, value):
        raise NotImplementedError()

    def __str__(self):

        result = f'[{self.__class__.__name__} {self.name} '

        result += '%20s' % (self.type_,)

        result += ']'

        return result

    __repr__ = __str__

class TagAttributeField(Field):

    def read_from(self, obj):
        value = obj._tag.get(self.name, None)

        if value is None:
            return None
        elif issubclass(self.type_, bool):
            return str(bool(value)).lower()
        else:
            return str(value)

    def write_to(self, obj, value):
        obj._tag[self.name] = value

class ParamField(Field):
    def read_from(self, obj):
        holder = obj._tag.find('param', name=self.name)
        contents = [t for t in holder.children
                    if isinstance(t, bs4.Tag)]
        assert len(contents)==1
        
        result = self._type(contents[0])
        return result

    def write_to(self, obj, value):
        raise ValueError("9900")

class TagField(Field):
    def __init__(self):
        super().__init__(
                name = 'tag',
                type_ = bs4.Tag,
                default = None,
                doc = """The BeautifulSoup tag behind this item.""",
                )
 
    def read_from(self, obj):
        return obj._tag

    def write_to(self, obj, value):
        raise KeyError("You can't put a different tag into an object.")

class NamedChildField(Field):
    def __init__(self, name, _type, default, doc=None):
        super().__init__(
                name = name,
                type_ = _type,
                default = default,
                doc = doc,
                )

    def get_subtag(self, tag):
        return tag.find(self.name)
 
    def read_from(self, obj):

        subtag = self.get_subtag(obj._tag)

        if subtag is None:
            return ''
        else:
            return subtag.string

        raise ValueError()

    def write_to(self, obj, value):

        subtag = self.get_subtag(obj._tag)

        subtag.string = value

class _FieldsDict(dict):
    def getter(fn):
        _install_getter_or_setter('read_from', fn)

    def setter(fn):
        _install_getter_or_setter('write_to', fn)

    def _install_getter_or_setter(method_name, fn):
        fieldname = fn.__name__

        if fieldname not in self:
            raise KeyError(
                    f"{fieldname} is not a field in "
                    f"{self.__objclass__.__name__}.")

        setattr(self[fieldname], method_name, fn)

class _MetaclassWithFields(type):
    def __new__(cls, name, bases, dct):
        result = super().__new__(cls, name, bases, dct)
        result.FIELDS = _FieldsDict()
        return result

    def __dir__(self):
        raise ValueError()

class HasFields(metaclass=_MetaclassWithFields):
    pass

def field(*args, **kwargs):

    def _inner(layer_class):

        if not hasattr(layer_class, FIELDS_NAME):
            setattr(layer_class, FIELDS_NAME, _FieldsDict())
            """
            raise AttributeError(
                    f"The class {layer_class.__name__} doesn't have a "
                    f"FIELDS attribute, which means there's "
                    f"nowhere to put the field. Try subclassing "
                    f"sangfroid.layer.field.HasField."
                    )
                    """

        if (
                len(args)==1 and
                isinstance(args[0], Field)
                ):
            new_field = args[0]
        else:
            _type_arg = args[1]
            assert isinstance(_type_arg, type)

            if issubclass(_type_arg, v.Value):
                new_field = ParamField(*args, **kwargs)
            else:
                new_field = TagAttributeField(*args, **kwargs)

        layer_class.FIELDS[new_field.name] = new_field

        return layer_class

    return _inner
