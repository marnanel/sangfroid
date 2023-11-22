class Value:
    type_handlers = {}

    def __init__(self, tag):
        self.tag = tag

    # Decorator
    @classmethod
    def handles_type(cls, name):
        def _inner(cls):
            cls.type_handlers[name] = cls
            return cls
        return _inner

    @classmethod
    def from_tag(cls, tag):
        result = cls.type_handlers[tag.name]._from_tag_inner(tag)
        return result

    @property
    def __str__(self):
        return str(self.value)@Value.handles_type('real')

class Real:
    def __init__(self, tag):
        super().__init__(tag)
        self._value = float(self._value)

    @property
    def value(self):
        result = self.tag.get('value', None)
        if result is None:
            raise ValueError(f"value tag had no value: {self.tag}")
        return float(result)

