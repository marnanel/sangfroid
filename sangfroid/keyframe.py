from sangfroid.t import T

class Keyframe:
    def __init__(self, tag):
        self._tag = tag

    @property
    def time(self):
        return T(self._tag['time'],
                 reference_tag = self._tag,
                 )

    @property
    def name(self):
        return self._tag.text

    @property
    def active(self):
        if self._tag['active']=='true':
            return True
        else:
            return False

    def __str__(self):
        if self.active:
            active = ''
        else:
            active = ' (inactive)'
        return f'{self.time} {repr(self.name)}{active}'

    __repr__ = __str__

    @classmethod
    def all_in_animation(cls, animation):
        result = Keyframes.__new__(Keyframes)
        result.animation = animation

        return result

class Keyframes:
    def __init__(self):
        raise ValueError("Don't instantiate the Keyframes class directly.")

    def __len__(self):
        return len(self.animation.tag.find_all('keyframe'))

    def __iter__(self):
        for keyframe_tag in self.animation.tag.find_all('keyframe'):
            yield Keyframe(keyframe_tag)

    def __str__(self):
        result = f'Keyframes of {self.animation}:'
        if len(self)==0:
            result += '\n  (none)'
        else:
            for keyframe in self:
                result += f'\n  - {keyframe}'

        return result

    __repr__ = __str__
