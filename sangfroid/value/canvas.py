import bs4
from sangfroid.value.value import Value

@Value.handles_type()
class Canvas(Value):
    @property
    def value(self):

        from sangfroid.layer.layer import Layer

        layers = [field
                 for field in self.tag.children
                 if isinstance(field, bs4.element.Tag)
                 ]
        if len([n for n in layers if n.name!='layer'])!=0:
            raise ValueError(
                    f"Only layers can be the children of a canvas: {self.tag}"
                    )

        result = [Layer.from_tag(layer) for layer in layers]

        return result
