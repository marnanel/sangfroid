from sangfroid.layer.layer import Layer
import sangfroid.value as v

@Layer.handles_type()
class Text(Layer):
    SYMBOL = '𝕋'
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "text": v.String,
        "color": v.Color,
        "family": v.String,
        "style": v.Integer,
        "weight": v.Integer,
        "direction": v.Integer,
        "compress": v.Real,
        "vcompress": v.Real,
        "size": v.Vector,
        "orient": v.Vector,
        "origin": v.Vector,
        "use_kerning": v.Bool,
        "grid_fit": v.Bool,
        "invert": v.Bool,
    }

    @property
    def text(self):
        return self['text'].value

    @text.setter
    def text(self, v):
        self['text'].value = v
