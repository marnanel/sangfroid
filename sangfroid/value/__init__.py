"""
Types of possible values of layer attributes.

For example, a circle has a radius, which is a real number.
So the radius will be a value of class `sangfroid.value.Real`.

(It isn't just a `float`, because that wouldn't do if
the value was animated.)
"""

from sangfroid.value.value import *

from sangfroid.value.blendmethod import *
from sangfroid.value.canvas import *
from sangfroid.value.color import *
from sangfroid.value.vector import *
from sangfroid.value.gradient import *
from sangfroid.value.simple import *
from sangfroid.value.string import *
from sangfroid.value.tbd import *
from sangfroid.value.transformation import *

__all__ = [
        cls.__name__.title()
        for cls in Value.handles_type.handlers.values()
        ]
