import logging
import bs4
import sangfroid.value as v

logger = logging.getLogger('sangfroid')

class Field:
    def __init__(self,
                 type_,
                 default,
                 name = None,
                 doc = None,
                 ):
        self.type_ = type_
        self.default = default
        self.name = name
        self.owner = None
        self.default = default

        self.__doc__ = doc or ''
        self.__doc__ += f"\n\nType: {type_.__name__}"
        if default is not None:
            # yes, this is the right way round; think about it
            self.__doc__ += ' or None'

    def __set_name__(self, owner, name):
        self.owner = owner
        if self.name is None:
            self.name = name.replace('_', '-')

    def __get__(self, obj, obj_type=None):
        raise NotImplementedError()

    def __set__(self, obj, value):
        raise NotImplementedError()

    def __str__(self):

        result = f'[{self.__class__.__name__}'

        result += '%20s of %20s (%20s)' % (
                self.name,
                self.owner.__name__,
                self.type_,)

        result += ']'

        return result

    __repr__ = __str__

class TagAttrField(Field):

    def __init__(self,
                 *args,
                 type_override = None,
                 **kwargs):

        super().__init__(*args, **kwargs)

        self.type_override = type_override or self.type_
        assert self.type_override.__module__=='builtins', self.type_override

    def __get__(self, obj, obj_type=None):

        if self.name not in obj._tag.attrs:
            logger.debug("no %s field; returning default: %s",
                         self.name,
                         self.default,
                         )
            return self.default

        value = obj._tag.get(self.name)
        logger.debug("%s field is %s",
                     self.name,
                     value,
                     )

        if value is None:
            return None
        elif issubclass(self.type_override, bool):
            return str(value).lower()=='true'
        else:
            return self.type_override(value)

    def __set__(self, obj, value):
        if issubclass(self.type_override, bool):
            if value:
                value = 'true'
            else:
                value = 'false'
        else:
            value = self.type_override(value)

        obj._tag[self.name] = value

class ParamTagField(Field):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert self.type_.__module__!='builtins', self.type_

    def __get__(self, obj, obj_type=None):
        print("9100", self.name, obj)
        holder = obj._tag.find('param',
                               attrs={
                                   'name': self.name,
                                   },
                               )
        contents = [t for t in holder.children
                    if isinstance(t, bs4.Tag)]
        assert len(contents)==1
        
        result = self.type_(contents[0])
        return result

    def __set__(self, obj, value):
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
 
    def __get__(self, obj, obj_type=None):
        return obj._tag

    def __set__(self, obj, value):
        raise KeyError("You can't put a different tag into an object.")

class NamedChildField(Field):
    def __init__(self, type_, default, name=None, doc=None):
        super().__init__(
                type_ = type_,
                default = default,
                name = name,
                doc = doc,
                )

    def get_subtag_for_obj(self, obj):
        return obj._tag.find(self.name)
 
    def __get__(self, obj, obj_type=None):

        subtag = self.get_subtag_for_obj(obj)

        if subtag is None:
            return ''
        else:
            return subtag.string

        raise ValueError()

    def __set__(self, obj, value):

        subtag = self.get_subtag_for_obj(obj)

        subtag.string = value
"""

class _FieldsDict(dict):
    pass

class _MetaclassWithFields(type):

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
        name = name.replace('-', '_')

        setattr(layer_class, name, new_field)

        return layer_class

    return _inner
    """
