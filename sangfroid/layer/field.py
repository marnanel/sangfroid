import sangfroid.value as v

class Field:
    def __init__(self,
                 name,
                 type_,
                 default,
                 in_params = None,
                 ):
        self.type_ = type_
        self.default = default
        self.name = name

        if in_params is None:
            self.in_params = issubclass(type_, v.Value)
        else:
            self.in_params = in_params

    def __str__(self):

        result = f'[{self.name} '

        if self.in_params:
            result += 'param '
        else:
            result += 'attr  '

        result += '%20s' % (self.type_,)

        result += ']'

        return result

    __repr__ = __str__

    @classmethod
    def dict_of(self, *fields):
        assert all([isinstance(f, Field) for f in fields])

        result = dict([
            (f.name, f)
            for f in fields
            ])

        return result
