class Boolean:
    def __init__(self, value):
        if value=='true' or value==1:
            self.value = True
        elif value=='false' or value==0:
            self.value = False
        else:
            raise ValueError("{value} is not a valid description of a boolean")

    def __bool__(self):
        return self.value

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
    root = tag.find_parents()[-2] # -1 is "document", the anon root tag
    assert root.name=='canvas'
    result = float(root['fps'])
    return result
