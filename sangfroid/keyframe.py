from sangfroid.t import T

class Keyframe:
    def __init__(self, time, name,
                 active = True,
                 ):
        self.time = time
        self.name = name
        self.active = active
        self.tag = None

    @classmethod
    def from_tag(cls, tag):
        result = cls(
                time = T(tag['time']),
                name = tag.get('name', None),
                active = tag['active'],
                )
        result.tag = tag

        return result
