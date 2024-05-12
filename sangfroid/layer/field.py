import bs4
import sangfroid.value as v

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
        self.__doc__ += f"\n\nType: {type_.__name__}"
        if default is not None:
            # yes, this is the right way round; think about it
            self.__doc__ += ' or None'

    def read_from(self, obj):
        raise NotImplementedError()

    def write_to(self, obj, value):
        raise NotImplementedError()

    def __call__(self):
        pass

    def __str__(self):

        result = f'[{self.__class__.__name__} {self.name} '

        result += '%20s' % (self.type_,)

        result += ']'

        return result

    @classmethod
    def tag_for_obj(cls, obj):
        return object.__getattribute__(obj, '_tag')

    __repr__ = __str__

class TagAttributeField(Field):

    def read_from(self, obj):
        value = self.tag_for_obj(obj).get(self.name, None)

        if value is None:
            return None
        elif issubclass(self.type_, bool):
            return str(value).lower()=='true'
        else:
            return self.type_(value)

    def write_to(self, obj, value):
        if issubclass(self.type_, bool):
            if value:
                value = 'true'
            else:
                value = 'false'
        else:
            value = self.type_(value)

        self.tag_for_obj(obj)[self.name] = value

class ParamField(Field):
    def read_from(self, obj):
        holder = self.tag_for_obj(obj).find('param',
                                            attrs={
                                                'name': self.name,
                                                },
                                            )
        contents = [t for t in holder.children
                    if isinstance(t, bs4.Tag)]
        assert len(contents)==1
        
        result = self.type_(contents[0])
        return result

    def write_to(self, obj, value):
        raise NotImplementedError(
                "9000"
                )

class TagField(Field):
    def __init__(self):
        super().__init__(
                name = 'tag',
                type_ = bs4.Tag,
                default = None,
                doc = """The BeautifulSoup tag behind this item.""",
                )
 
    def read_from(self, obj):
        return self.tag_for_obj(obj)

    def write_to(self, obj, value):
        raise KeyError("You can't put a different tag into an object.")

class NamedChildField(Field):
    def __init__(self, name, type_, default, doc=None):
        super().__init__(
                name = name,
                type_ = type_,
                default = default,
                doc = doc,
                )

    def get_subtag_for_obj(self, obj):
        return self.tag_for_obj(obj).find(self.name)
 
    def read_from(self, obj):

        subtag = self.get_subtag_for_obj(obj)

        if subtag is None:
            return ''
        else:
            return subtag.string

        raise ValueError()

    def write_to(self, obj, value):

        subtag = self.get_subtag_for_obj(obj)

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
    """9000
    def __new__(cls, name, bases, dct):
        result = super().__new__(cls, name, bases, dct)
        return result
        """

    def __dir__(self):
        result = super().__dir__()
        return result

class HasFields(metaclass=_MetaclassWithFields):
    pass

def field(*args, **kwargs):

    def _inner(layer_class):

        name = kwargs.get('name', None)
        if name is not None:
            del kwargs['name']

        if (
                len(args)==1 and
                isinstance(args[0], Field)
                ):
            new_field = args[0]
        else:
            type_arg = args[1]
            assert isinstance(type_arg, type)

            if issubclass(type_arg, v.Value):
                new_field = ParamField(*args, **kwargs)
            else:
                new_field = TagAttributeField(*args, **kwargs)

        name = name or new_field.name

        setattr(layer_class, name, new_field)

        return layer_class

    return _inner
