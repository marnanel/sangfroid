class Registry:
    def __init__(self):
        self.handlers = {}

    # Decorator.
    def __call__(self, name=None):
        def _inner(c):
            n = name or c.__name__.lower()

            self.handlers[n] = c
            return c
        return _inner

    def from_tag(self, name):

        if name not in self.handlers:
            raise ValueError(
                    f"This tag is a {name}, which I don't know how "
                    "to handle."
                    )
        result = self.handlers[name]

        return result
