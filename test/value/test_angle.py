import pytest
import sangfroid
from sangfroid.value import *
from test import *

def test_angle_simple():
    sif = get_animation('circles.sif')
    layer = sif.find(desc="Well, it's round")
    transformation = layer.transformation

    assert transformation.angle == 45.0
    assert transformation.skew_angle == 50.5

    assert str(transformation.angle) == '45°'
    assert str(transformation.skew_angle) == '50.5°'

    angle = Angle(45)
    assert angle==45
    assert str(angle) == '45°'
