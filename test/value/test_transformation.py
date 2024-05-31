import sangfroid
from test import *

def test_transformation_simple():
    sif = get_animation('circles.sif')

    circle = sif.find(desc="Well, it's round")
    transformation = circle.transformation

    assert transformation == {
            'offset': (3.3333332539, -0.8333333135),
            'angle': 45.0,
            'skew_angle': 50.5,
            'scale': (2.0, 0.5),
            }

def test_transformation_shortcuts():
    sif = get_animation('circles.sif')

    circle = sif.find(desc="Well, it's round")

    assert circle.offset == (3.3333332539, -0.8333333135)
    assert circle.angle == 45.0
    assert circle.skew_angle == 50.5
    assert circle.scale == (2.0, 0.5)
