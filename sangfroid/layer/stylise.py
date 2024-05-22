from sangfroid.layer import Layer
import sangfroid.value as v

@Layer.handles_type()
class Shade(Layer):
    SYMBOL = '👓'

    ### {{{
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "color": v.Color,
        "origin": v.Vector,
        "size": v.Vector,
        "type": v.Integer,
        "invert": v.Bool,
    }
    ### }}}

@Layer.handles_type()
class Bevel(Layer):
    SYMBOL = '🫴'

    ### {{{
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "type": v.Integer,
        "color1": v.Color,
        "color2": v.Color,
        "angle": v.Angle,
        "depth": v.Real,
        "softness": v.Real,
        "use_luma": v.Bool,
        "solid": v.Bool,
        "fake_origin": v.Vector,
    }
    ### }}}
