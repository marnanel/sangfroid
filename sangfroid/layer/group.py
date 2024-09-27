from sangfroid.layer import Layer
import sangfroid.value as v
import sangfroid.field as f
import bs4

@f.ShortcutField.include_from("transformation")
@Layer.handles_type()
class Group(Layer):
    """
    A collection of Layers, which are rendered together.
    """
    SYMBOL = '📂'

    ### {{{
    SYNFIG_VERSION = "0.3"

    z_depth              = f.ParamTagField(v.Real, 0.0,
                                  doc='How deep in the group this layer appears.',
                        )
    amount               = f.ParamTagField(v.Real, 1.0,
                                  doc='1.0 for opaque, 0.0 for transparent.',
                        )
    blend_method         = f.ParamTagField(v.BlendMethod, v.BlendMethod.COMPOSITE,
                                  doc='How this layer will affect the layers beneath it.',
                        )
    origin               = f.ParamTagField(v.X_Y, (0.0, 0.0),
                                  doc='Where the transformation coordinates are measured from.\n\n            You can move this around to move the layer.',
                        )
    transformation       = f.ParamTagField(v.Transformation, {
                                         'offset': (0.0, 0.0),
                                          'angle': 0.0,
                                     'skew_angle': 0.0,
                                          'scale': (1.0, 1.0),
                                        },
                        )
    canvas               = f.ParamTagField(v.Canvas, [],
                                  doc='Any layers which are inside this one.',
                        )
    time_dilation        = f.ParamTagField(v.Real, 1.0,
                        )
    time_offset          = f.ParamTagField(v.Time, 0,
                        )
    children_lock        = f.ParamTagField(v.Bool, False,
                        )
    outline_grow         = f.ParamTagField(v.Real, 0.0,
                        )
    z_range              = f.ParamTagField(v.Bool, False,
                        )
    z_range_position     = f.ParamTagField(v.Real, 0.0,
                        )
    z_range_depth        = f.ParamTagField(v.Real, 0.0,
                        )
    z_range_blur         = f.ParamTagField(v.Real, 0.0,
                        )

    ### }}}

    @property
    def canvas_tag(self):
        param = self._tag.find('param',
                              attrs={
                                  'name': 'canvas',
                                  },
                              )

        if param is None:
            raise ValueError(
                    "Group layer has no canvas parameter!"
                    "\n\n"
                    f"{self._tag}"
                    )

        return param.find('canvas')

    def _get_children(self,
                 include_descendants = False,
                 ):

        canvas = self.canvas_tag

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

    def append(self, layer):
        if not isinstance(layer, Layer):
            raise TypeError(type(layer))

        after = None
        # "after" from our perspective; *before* in the XML

        canvas = self.canvas_tag
        for child in canvas.contents:
            if not isinstance(child, bs4.element.Tag):
                continue
            if child.name=='layer':
                after = child
                break

        if after is None:
            canvas.append(layer._tag)
        else:
            after.insert_before(layer._tag)

    def insert(self, index, layer):
        if not isinstance(layer, Layer):
            raise TypeError(type(layer))

        before = self[index]
        # "before" from our perspective; *after* in the XML

        before._tag.insert_after("\n")
        before._tag.insert_after(layer._tag)
        before._tag.insert_after("\n")

    def __getitem__(self, f):
        if isinstance(f, int):
            return list(self.children)[f]
        else:
            return super().__getitem__(f)
