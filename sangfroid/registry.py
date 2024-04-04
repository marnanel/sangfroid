from sangfroid.util import normalise_synfig_layer_type_name

class Registry:
    """
    Decorator, mapping names of things onto classes that handle those things.

    Names are case-insensitive, and underscores are not significant.

    Args to the decorator:
        name (str, optional): the name to associate this class with.
            If None or omitted, the name of the class is used.
    """
    def __init__(self):
        self.handlers = {}

    # Decorator.
    def __call__(self, name=None):
        def _inner(c):
            n = name or c.__name__
            n = normalise_synfig_layer_type_name(n)

            self.handlers[n] = c
            return c
        return _inner

    def from_name(self, name):
        """
        Returns whatever is associated with "name".

        Returns:
            any type

        Raises:
            KeyError, if the name doesn't refer to anything.
        """
        name = normalise_synfig_layer_type_name(name)

        if name not in self.handlers:
            raise KeyError(
                    f"This tag is a {name}, which I don't know how "
                    "to handle."
                    )
        result = self.handlers[name]

        return result
