from enum import Enum
from sangfroid.value.simple import Integer

class BlendMethod(Enum):
    ### {{{

    COMPOSITE = 0
    STRAIGHT = 1
    BRIGHTEN = 2
    DARKEN = 3
    ADD = 4
    SUBTRACT = 5
    MULTIPLY = 6
    DIVIDE = 7
    COLOR = 8
    HUE = 9
    SATURATION = 10
    LUMINANCE = 11
    BEHIND = 12
    ONTO = 13
    ALPHA_BRIGHTEN = 14
    ALPHA_DARKEN = 15
    SCREEN = 16
    HARD_LIGHT = 17
    DIFFERENCE = 18
    ALPHA_OVER = 19
    OVERLAY = 20
    STRAIGHT_ONTO = 21
    ADD_COMPOSITE = 22
    ALPHA = 23
    
    ### }}}

    @classmethod
    def from_tag(cls, t):
        v = Integer.from_tag(t)
        return cls(v.value)

    def as_python_expression(self):
        return 'v.'+str(self)
