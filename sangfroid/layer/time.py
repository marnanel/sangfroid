from sangfroid.layer import Layer
import sangfroid.value as v
import sangfroid.layer.field as f

@Layer.handles_type()
class Timeloop(Layer):
    SYMBOL = '🕰️'

    ### {{{
    SYNFIG_VERSION = "0.2"

    z_depth              = f.ParamTagField(v.Real, 0.0)
    link_time            = f.ParamTagField(v.Time, 0)
    local_time           = f.ParamTagField(v.Time, 0)
    duration             = f.ParamTagField(v.Time, '1s')
    only_for_positive_duration = f.ParamTagField(v.Bool, True)
    symmetrical          = f.ParamTagField(v.Bool, True)

    ### }}}@Layer.handles_type()
class Stroboscope(Layer):
    SYMBOL = '🔦'

    ### {{{
    SYNFIG_VERSION = "0.1"

    z_depth              = f.ParamTagField(v.Real, 0.0)
    frequency            = f.ParamTagField(v.Real, 2.0)

    ### }}}@Layer.handles_type()
class Freetime(Layer):
    SYMBOL = '🍦'
    
    ### {{{
    SYNFIG_VERSION = "0.1"

    z_depth              = f.ParamTagField(v.Real, 0.0)
    time                 = f.ParamTagField(v.Time, 0)

    ### }}}
