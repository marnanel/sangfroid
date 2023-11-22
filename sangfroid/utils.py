class Boolean:
    def __init__(self, value):
        if value=='true' or value==1:
            self.value = True
        elif value=='false' or value==0:
            self.value = False
        else:
            raise ValueError("{value} is not a valid description of a boolean")

    def __bool__(self):
        return self.value

    def __str__(self):
        if self.value:
            return 'true'
        else:
            return 'false'

    __repr__ = __str__
