import copy
import logging
import bs4
import sangfroid.value as v
from sangfroid.registry import Registry
from sangfroid.layer.field import (
        Field,
        TagAttrField,
        ParamTagField,
        TagField,
        )
from sangfroid.util import (
        normalise_synfig_layer_type_name,
        type_and_str_to_value,
        type_and_value_to_str,
        )

logger = logging.getLogger('sangfroid')

class Layer:

    SYMBOL = '?' # fallback

    type_            = TagAttrField(str,         None, name='type')
    active           = TagAttrField(bool,        True)
    exclude_from_rendering = TagAttrField(bool,  False)
    version          = TagAttrField(float,       None)

    """
    A description of this layer.
    """
    desc             = TagAttrField(str,         '')

    tag              = TagField()

    ########################

    def __init__(self, tag):
        self._tag = tag

    @property
    def parent(self):
        cursor = self._tag.parent
        while cursor is not None:
            if cursor.name=='layer':
                return Layer.from_tag(cursor)
                return cursor
            cursor = cursor.parent

    def __repr__(self):
        result = '['
        result += ('-'*self.tag_depth)
        result += self.SYMBOL
        result += self.__class__.__name__.lower()
        try:
            # Look desc up directly, rather than going through the field
            # resolution process. If any errors occur there, it'll
            # inevitably try to print the name of layers, which would
            # cause infinite recursion.
            result += ' ' + repr(self.tag['desc'])
        except KeyError:
            pass

        result += ']'
        return result

    def __getitem__(self, f):
        found = self._tag.find('param', attrs={'name': f})
        if found is None:
            raise KeyError(f)
        return _name_and_value_of(found)[1]

    def __setitem__(self, f, val):
        found = self._tag.find('param', attrs={'name': f})
        if found is None:
            raise KeyError(f)
        old_value = _name_and_value_of(found)[1]

        if isinstance(val, v.Value):
            if not isinstance(val, old_value.__class__):
                raise TypeError(val.__class__)

            new_value = val
        else:
            new_value = old_value.__class__(val)

        old_value.tag.replace_with(new_value.tag)

    def __contains__(self, f):
        found = self._tag.find(
                'param',
                attrs={'name': f},
                )
        return found is not None
    
    @property
    def tag_depth(self):
        cursor = self._tag.parent
        result = 0
        while cursor is not None:
            if cursor.name=='layer':
                result += 1
            cursor = cursor.parent
        return result

    def find_all(self,
                 *args,
                 recursive=True,
                 **kwargs,
                 ):

        matching_special = None

        if len(args)>1:
            raise v.ValueError(
                    "You can only give one positional argument.")
        elif len(args)==1:

            if (
                    isinstance(args[0], str) or
                    (isinstance(args[0], type) and
                     issubclass(args[0], Layer))
                    ):
                if 'type' in kwargs:
                    raise v.ValueError(
                            "You can't give a type in both the positional "
                            "and keyword arguments.")

                kwargs['type'] = args[0]

            elif isinstance(args[0], bool):
                matching_special = args[0]

            elif hasattr(args[0], '__call__'):
                matching_special = args[0]

            else:
                raise TypeError(args[0])

        if 'attrs' in kwargs:
            for k,v in kwargs['attrs'].items():
                if k in kwargs:
                    raise v.ValueError("{k} specified both as a kwarg and in attrs")
                kwargs[k] = v

            del kwargs['attrs']

        for k,v in kwargs.items():
            if k=='type':
                if not isinstance(v, str):
                    v = v.__name__

                kwargs[k] = v.lower().replace('_', '')

        logger.debug("begin find_all")

        def matcher(found_tag):
            if found_tag.name!='layer':
                return False

            logger.debug("considering tag: %s %s",
                         found_tag.name, found_tag.attrs)

            found_layer = Layer.from_tag(found_tag)

            if matching_special is None:

                def munge(k,v):
                    if k=='type':
                        k = 'type_'
                        v = v.lower()

                    return (k,v)

                targets = [
                    munge(k,v)
                    for k,v in kwargs.items()
                    ]

                logger.debug("want: %s", targets)

                for k, want_value in targets:
                    try:
                        found_value = getattr(found_layer, k)
                        logger.debug("  -- %s field is %s; want %s", k,
                                     repr(found_value),
                                     repr(want_value),
                                     )
                    except AttributeError:
                        logger.debug("  -- it does not have a %s", k)
                        continue

                    logger.debug("  want: %s  found: %s",
                                 want_value, found_value)

                    if found_value==want_value:
                        logger.debug("    -- a match!")
                        return True

                logger.debug("  -- no matches.")
                return False

            elif isinstance(matching_special, bool):
                return matching_special

            else:
                result = matching_special(found_tag)
                logger.debug("  -- callback says: %s", result)
                return result

            raise v.ValueError(found_tag)

        result = [
                self.from_tag(x) for x in
                self._tag.find_all(matcher,
                                  recursive=recursive,
                                  )
                ]
        logger.debug("find_all found: %s",
                     result,
                     )

        return result

    @property
    def children(self):
        return
        yield

    def find(self, *args, **kwargs):
        items = self.find_all(*args, **kwargs)
        if items:
            return items[0]
        else:
            return None

    __call__ = find

    ########################

    handles_type = Registry()

    @classmethod
    def from_tag(cls, tag):
        tag_type = tag.get('type', None)
        if tag_type is None:
            raise v.ValueError(
                    f"tag has no 'type' field: {tag}")
        return cls.handles_type.from_name(name=tag_type)(tag)

    def _as_dict(self):
        return dict([
            _name_and_value_of(param)
            for param in self._tag.find_all('param')
            ])

    def items(self):
        return self._as_dict().items()

    def keys(self):
        return self._as_dict().keys()

    def values(self):
        return self._as_dict().values()

    def __iter__(self):
        return self._as_dict().__iter__()

    def _get_param(self, k):
        tag = self._tag.find('param',
                            attribs={
                                'name': k,
                                })
        if tag is None:
            return None

        raise ValueError(f"{k}, {tag}")

def _name_and_value_of(tag):
    if tag.name!='param':
        raise v.ValueError(f"param is not a <param>: {tag}")

    name = tag.get('name', None)
    if name is None:
        raise v.ValueError(f"param has no 'name' field: {tag}")

    value_tags = [tag for tag in tag.children
                  if isinstance(tag, bs4.element.Tag)
                  ]

    if len(value_tags)!=1:
        raise v.ValueError(f"param should have one value: {tag}")

    value_tag = value_tags[0]

    value = v.Value.from_tag(value_tag)
    return name, value
