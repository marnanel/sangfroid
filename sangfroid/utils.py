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

def _canvas_root(tag):
    parents = tag.find_parents()

    if len(parents)==0:
        raise ValueError(f"{tag} is not attached to a document, "
                         "so I can't determine the correct FPS."
                         )

    elif len(parents)==1:
        root = tag
    else:
        root = parents[-2] # -1 is "document", the anon root tag
    assert root.name=='canvas'
    return root

def _root_tag_to_fps(root_tag):
    assert root_tag.name=='canvas'
    result = float(root_tag['fps'])
    return result

def tag_to_fps(tag):
    """
    Given any tag from a Synfig document, finds that document's film speed
    in frames per second (fps).

    Args:
        tag (Tag): any tag from a Synfig document

    Returns:
        float, the speed in frames per second.
    """
    result = _root_tag_to_fps(_canvas_root(tag))
    return result

def tag_to_canvas_duration(tag):

    from sangfroid.t import T
    root_tag = _canvas_root(tag)
    fps = _root_tag_to_fps(root_tag)

    begin_time = T(tag.attrs['begin-time'],
                 fps=fps,
                 )
    end_time = T(tag.attrs['end-time'],
                 fps=fps,
                 )
    result = int(end_time) - int(begin_time)
    return result

__all__ = [
        'tag_to_canvas_duration',
        'tag_to_fps',
        'Boolean',
        ]
