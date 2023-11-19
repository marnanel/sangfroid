from sangfroid.layer import Layer

@Layer.handles_type("circle")
class Circle(Layer):
    SYMBOL = '🔵'
