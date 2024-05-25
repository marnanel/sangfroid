from sangfroid.layer import Layer
import sangfroid.value as v
import sangfroid.layer.field as f
import bs4

@Layer.handles_type()
class Group(Layer):
    SYMBOL = '📂'

    ### {{{
    SYNFIG_VERSION = "0.3"

    z_depth              = f.ParamTagField(v.Real, 0.0)
    amount               = f.ParamTagField(v.Real, 1.0)
    blend_method         = f.ParamTagField(v.BlendMethod, v.BlendMethod.COMPOSITE)
    origin               = f.ParamTagField(v.X_Y, (0.0, 0.0))
    transformation       = f.ParamTagField(v.Transformation, {
                                         'offset': (0.0, 0.0),
                                          'angle': 0.0,
                                     'skew_angle': 0.0,
                                          'scale': (1.0, 1.0),
                                        })
    canvas               = f.ParamTagField(v.Canvas, [])
    time_dilation        = f.ParamTagField(v.Real, 1.0)
    time_offset          = f.ParamTagField(v.Time, 0)
    children_lock        = f.ParamTagField(v.Bool, True)
    outline_grow         = f.ParamTagField(v.Real, 0.0)
    z_range              = f.ParamTagField(v.Bool, True)
    z_range_position     = f.ParamTagField(v.Real, 0.0)
    z_range_depth        = f.ParamTagField(v.Real, 0.0)
    z_range_blur         = f.ParamTagField(v.Real, 0.0)

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
