import bs4
from sangfroid.value.complex import Composite

class Transformation(Composite):
    REQUIRED_KEYS = {
            'offset',
            'angle',
            'skew_angle',
            'scale',
            }
