import sangfroid
from test import *

def test_sif_fields():
    sif = get_animation('circles.sif')

    assert sif.name == 'circles'
    assert sif.description == 'I like circles. They are round.'
    assert sif.width == 480
    assert sif.height == 270
    assert sif.xres==2834.645669
    assert sif.yres==2834.645669
    assert sif.gamma==(1.0, 1.0, 1.0)
