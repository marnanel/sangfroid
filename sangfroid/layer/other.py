from sangfroid.layer import Layer
import sangfroid.value as v

@Layer.handles_type()
class Import(Layer):
    SYMBOL = 'I'
    ### {{{
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "size": v.Vector,
        "transformation": v.Composite,
    }
    ### }}}
