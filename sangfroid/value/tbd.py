from sangfroid.value.value import Value

class Tbd(Value):
    """
    All types which are not yet implemented.
    """
    @property
    def value(self):
        raise NotImplementedError(
                f"{self.__class__.__name__} is not yet implemented.")

@Value.handles_type()
class Dynamic_List(Tbd):
    pass

@Value.handles_type()
class Static_List(Tbd):
    pass

@Value.handles_type()
class Wplist(Tbd):
    pass

@Value.handles_type()
class Dilist(Tbd):
    pass
