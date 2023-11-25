class Registry:
    def __init__(self):
        self.handlers = {}

    def __call__(self, name=None):
        def _inner(c):
            n = name or c.__name__.lower()

            self.handlers[n] = c
            return c
        return _inner
