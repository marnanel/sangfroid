from sangfroid.layer import Layer
import bs4

@Layer.handles_type("group")
class Group(Layer):
    SYMBOL = '📂'

    def _get_children(self,
                 include_descendants = False,
                 ):

        if self.tag.name=='layer':
            canvas = self.tag.find('canvas')
        else:
            canvas = self.tag

        for child in reversed(canvas.contents):
            if not isinstance(child, bs4.element.Tag):
                continue
            if child.name!='layer':
                continue

            result = Layer.from_tag(child)
            yield result

            if include_descendants and hasattr(result, 'children'):
                yield from result.children

    @property
    def children(self):
        yield from self._get_children(
                include_descendants = False,
                )
    @property
    def descendants(self):
        yield from self._get_children(
                include_descendants = True,
                )
