from sangfroid.layer import Layer

@Layer.handles_type("blur")
class Blur(Layer):
    SYMBOL = '🟠'

