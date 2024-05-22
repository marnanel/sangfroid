from sangfroid.layer import Layer
import sangfroid.value as v

@Layer.handles_type()
class Blur(Layer):
    SYMBOL = '🟠'

    ### {{{
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "size": v.Vector,
        "type": v.Integer,
    }
    ### }}}

@Layer.handles_type()
class Radial_Blur(Layer):
    SYMBOL = '🟠'

    ### {{{
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "origin": v.Vector,
        "size": v.Real,
        "fade_out": v.Bool,
    }
    ### }}}

@Layer.handles_type()
class Motion_Blur(Layer):
    SYMBOL = '🟠'

    ### {{{
    PARAMS = {
        "aperture": v.Time,
        "subsamples_factor": v.Real,
        "subsampling_type": v.Integer,
        "subsample_start": v.Real,
        "subsample_end": v.Real,
    }
    ### }}}
