import bs4
from sangfroid.value.value import Value

RGBA = 'rgba'

@Value.handles_type()
class Color(Value):

    @property
    def value(self):
        result = '#' + (''.join([
                '%02x' % (
                    int(round(float(self.tag(dimension)[0].string)*255.0)),)
            for dimension in RGBA
            ]))

        if result.endswith('ff'):
            result = result[:-2]
        return result

    def as_tuple(self):
        result = tuple([
            float(self.tag(dimension)[0].string)
            for dimension in RGBA
            ])
        return result

    def __eq__(self, other):

        if isinstance(other, Color):
            return self.value == other.value
        elif isinstance(other, str):
            other = other.lower()
            if not other.startswith('#'):
                other = f'#{other}'
            if len(other)==9 and other.endswith('ff'):
                other = other[:-2]
            return str(self) == other
        elif isinstance(other, tuple):
            if len(other)==3:
                other = other+(1.0,)
            return self.as_tuple() == other
        else:
            return False

    @value.setter
    def value(self, v):

        def _raise_format_error():
            raise ValueError(
                    "Express a colour value as (r,g,b), or (r,g,b,a), or "
                    f"as a string of six or eight hex digits: {v}"
                    )

        if isinstance(v, tuple):

            if len(v)==0:
                result = (1.0, 1.0, 1.0, 1.0)
            elif len(v)==3:
                result = v + (1.0,)
            elif len(v)==4:
                result = v
            else:
                _raise_format_error()

        elif isinstance(v, str):
            if v.startswith('#'):
                v = v[1:]

            if len(v)==6:
                v += 'FF'
            elif len(v)==8:
                pass
            else:
                _raise_format_error()

            result = tuple(
                round(int(v[i*2:i*2+2], 16)/255, 6)
                for i in range(4))
        else:
            _raise_format_error()

        assert isinstance(result, tuple), result
        assert [type(n) for n in result]==[float]*4, result

        self.tag.name = __class__.__name__.lower()
        self.tag.attrs = {}
        self.tag.clear()

        for i, dimension in enumerate(RGBA):
            dimension_tag = bs4.element.Tag(name=dimension)
            dimension_tag.string = '%.06f' % (result[i],)
            self.tag.append(dimension_tag)
