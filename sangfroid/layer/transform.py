from sangfroid.layer import Layer
import sangfroid.value as v
import sangfroid.layer.field as f

@Layer.handles_type()
class Scale(Layer):
    SYMBOL = '⚖️' # yeah, a bit contrived

    ### {{{
    PARAMS = {
        "amount": v.Real,
        "center": v.Vector,
    }












    ### }}}

@Layer.handles_type()
class Zoom(Scale):
    ### {{{
    SYNFIG_VERSION = "0.1"

    amount               = f.ParamTagField(v.Real, 0.0)
    center               = f.ParamTagField(v.X_Y, (0.0, 0.0))

    ### }}}
    pass # XXX do they differ?

@Layer.handles_type()
class Translate(Layer):
    SYMBOL = '⇄'

    ### {{{
    SYNFIG_VERSION = "0.1"

    origin               = f.ParamTagField(v.X_Y, (0.0, 0.0))

    ### }}}

@Layer.handles_type()
class Rotate(Layer):
    SYMBOL = '🗘'

    ### {{{
    SYNFIG_VERSION = "0.1"

    origin               = f.ParamTagField(v.X_Y, (0.0, 0.0))
    amount               = f.ParamTagField(v.Angle, 0.0)

    ### }}}
