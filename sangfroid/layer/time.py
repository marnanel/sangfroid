from sangfroid.layer import Layer
import sangfroid.value as v

@Layer.handles_type()
class Timeloop(Layer):
    SYMBOL = '🕰️'
    PARAMS = {
        "z_depth": v.Real,
        "link_time": v.Time,
        "local_time": v.Time,
        "duration": v.Time,
        "only_for_positive_duration": v.Bool,
        "symmetrical": v.Bool,
    }

@Layer.handles_type()
class Stroboscope(Layer):
    SYMBOL = '🔦'
    PARAMS = {
        "z_depth": v.Real,
        "frequency": v.Real,
    }

@Layer.handles_type()
class Freetime(Layer):
    SYMBOL = '🍦'
    PARAMS = {
        "z_depth": v.Real,
        "time": v.Time,
    }
