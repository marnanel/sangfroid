from sangfroid.layer import Layer
import sangfroid.value as v

# XXX Do these differ?
@Layer.handles_type('scale')
@Layer.handles_type('zoom')
class Scale(Layer):
    SYMBOL = '⚖️' # yeah, a bit contrived

    ### {{{
    PARAMS = {
        "amount": v.Real,
        "center": v.Vector,
    }
    ### }}}

@Layer.handles_type()
class Translate(Layer):
    SYMBOL = '⇄'

    ### {{{
    PARAMS = {
        "origin": v.Vector,
    }
    ### }}}

@Layer.handles_type()
class Rotate(Layer):
    SYMBOL = '🗘'

    ### {{{
    PARAMS = {
        "origin": v.Vector,
        "amount": v.Angle,
    }
    ### }}}
