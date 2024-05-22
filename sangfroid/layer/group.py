from sangfroid.layer import Layer
import sangfroid.value as v
import bs4

@Layer.handles_type()
class Group(Layer):
    SYMBOL = '📂'

    ### {{{
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "origin": v.Vector,
        "transformation": v.Composite,
        "canvas": v.Canvas,
        "time_dilation": v.Real,
        "time_offset": v.Time,
        "children_lock": v.Bool,
        "outline_grow": v.Real,
        "z_range": v.Bool,
        "z_range_position": v.Real,
        "z_range_depth": v.Real,
        "z_range_blur": v.Real,
    }
    ### }}}

    def _get_children(self,
                 include_descendants = False,
                 ):

        if self._tag.name=='layer':
            canvas = self._tag.find('canvas')
        else:
            canvas = self._tag

        for child in reversed(canvas.contents):
            if not isinstance(child, bs4.element.Tag):
                continue
            if child.name!='layer':
                continue

            result = Layer.from_tag(child)
            yield result

            if include_descendants:
                yield from result.children

    @property
    def children(self):
        yield from self._get_children(
                include_descendants = False,
                )
    @property
    def descendants(self):
        yield from self._get_children(
                include_descendants = True,
                )
