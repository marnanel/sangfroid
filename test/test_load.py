import sangfroid
from test import *

def test_load_sif():
    sif = get_animation('circles.sif')

    assert sif.name == 'circles'
    assert sif.description == 'I like circles. They are round.'
    assert sif.width == 480
    assert sif.height == 270
    assert sif.xres==2834.645669
    assert sif.yres==2834.645669
    assert sif.gamma==(1.0, 1.0, 1.0)

def test_load_sifz():
    sif = get_animation('wombats.sifz')

    assert sif.name == 'wombats'
    assert sif.description == 'I like wombats. They live in Australia.'
