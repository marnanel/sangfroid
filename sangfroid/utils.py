class Boolean:
    def __init__(self, value=0):
        if isinstance(value, Boolean):
            value = value.value
        elif isinstance(value, str):
            value = value.lower()

        if value=='true':
            self.value = True
        elif value=='false':
            self.value = False
        elif isinstance(value, bool):
            self.value = value
        elif isinstance(value, int):
            self.value = value!=0
        else:
            raise ValueError("{value} is not a valid description of a boolean")

        assert isinstance(self.value, bool)

    def __bool__(self):
        return self.value

    def __int__(self):
        if self.value:
            return 1
        else:
            return 0

    def __eq__(self, other):
        return self.value==bool(other)

    def __str__(self):
        if self.value:
            return 'true'
        else:
            return 'false'

    __repr__ = __str__

def tag_to_fps(tag):
    """
    Given any tag from a Synfig document, finds that document's film speed
    in frames per second (fps).

    Args:
        tag (Tag): any tag from a Synfig document

    Returns:
        float, the speed in frames per second.
    """
    parents = tag.find_parents()

    if len(parents)<2:
        raise ValueError(f"{tag} is not attached to a document, "
                         "so I can't determine the correct FPS."
                         )

    root = parents[-2] # -1 is "document", the anon root tag
    assert root.name=='canvas'
    result = float(root['fps'])
    return result
