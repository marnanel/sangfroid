class Layer:

    SYMBOL = '?' # fallback

    ########################

    def __init__(self, tag):
        self.tag = tag

    @property
    def description(self):
        return self.tag.get('desc', None)

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
        result += repr(self.description)
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
        if tag['type'] not in cls.type_handlers:
            raise ValueError(
                    f"This tag is a <{tag['type']}>, which I don't know how "
                    "to handle."
                    )
        result = cls.type_handlers[tag['type']]._from_tag_inner(tag)

        return result

    @classmethod
    def _from_tag_inner(cls, tag):
        if cls==Layer:
            raise NotImplementedError()

        return cls(tag)
