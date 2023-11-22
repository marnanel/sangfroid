from sangfroid.value import Value

class Layer:

    SYMBOL = '?' # fallback

    ########################

    def __init__(self, tag):
        self.tag = tag

        # 'group' field?
        self.active = tag.get('active', True)
        self.synfig_version = tag.get('version', None)
        self.exclude_from_rendering = tag.get(
                'exclude_from_rendering', False)

        def name_and_value_of(tag):
            name = tag.get('name', None)

            if name is None:
                raise ValueError(f"param has no name: {tag}")

            use = tag.get("use", None)

            first_tag_child = None
            for c in tag.children:
                if hasattr(c, 'contents'):
                    first_tag_child = c
                    break

            if first_tag_child is None:
                if use is None:
                    raise ValueError(f"param has no value: {tag}")
                else:
                    print("(warning: 'use' is not yet implemented)")
                    value = 0

            else:
                if use is not None:
                    raise ValueError("param has both use and value: {tag}")
                value = Value(tag=first_tag_child)

            return name, value

        self.params = dict([
            name_and_value_of(param)
            for param in tag.find_all('param')
            ])

    @property
    def desc(self):
        result = self.tag.get('desc', None)
        if result is not None:
            return result

        node = self.tag.find('desc')
        if node is not None:
            return node.string

        return None

    @property
    def parent(self):
        cursor = self.tag.parent
        while cursor is not None:
            print("???", cursor.name)
            if cursor.name=='layer':
                return Layer.from_tag(cursor)
                return cursor
            cursor = cursor.parent

    def __repr__(self):
        result = '['
        result += ('-'*self.depth)
        result += self.SYMBOL
        result += self.__class__.__name__.lower()
        result += ' '
        result += repr(self.desc)
        result += ']'
        return result

    @property
    def depth(self):
        cursor = self.tag.parent
        result = 0
        while cursor is not None:
            if cursor.name=='layer':
                result += 1
            cursor = cursor.parent
        return result

    ########################

    # Factories, and setup for factories

    type_handlers = {}

    # Decorator
    @classmethod
    def handles_type(cls, name):
        def _inner(cls):
            cls.type_handlers[name] = cls
            return cls
        return _inner

    @classmethod
    def from_tag(cls, tag):
        tag_type = tag.get('type', None)
        if tag_type is None:
            raise ValueError(
                    "layer has no 'type' field.")

        if tag_type not in cls.type_handlers:
            raise ValueError(
                    f"This layer is a {tag_type}, which I don't know how "
                    "to handle."
                    )
        result = cls.type_handlers[tag_type]._from_tag_inner(tag)

        return result

    @classmethod
    def _from_tag_inner(cls, tag):
        if cls==Layer:
            raise NotImplementedError()

        return cls(tag)
