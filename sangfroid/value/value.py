class Value:

    def __init__(self, tag):
        self.tag = tag

    @classmethod
    def from_tag(cls, tag):
        return None
        result = cls.type_handlers[tag.name]._from_tag_inner(tag)
        return result

    @property
    def __str__(self):
        return str(self.value)

    ########################

    # Factories, and setup for factories

    type_handlers = {}

    # Decorator
    @classmethod
    def handles_type(cls):
        def _inner(c, name=None):
            if name is None:
                name = c.__name__.lower()

            c.type_handlers[name] = c
            return c
        return _inner
