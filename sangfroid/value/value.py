from sangfroid.registry import Registry

class Value:

    def __init__(self, tag):
        self.tag = tag

    def __str__(self):
        return str(self.value)

    ########################

    # Factories, and setup for factories

    handles_type = Registry()

    @classmethod
    def from_tag(cls, tag):
        return cls.handles_type.from_tag(name=tag.name)

    @property
    def value(self):
        return self._value
