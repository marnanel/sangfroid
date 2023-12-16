import sangfroid
from test import *

def test_load_sif():
    sif = get_animation('circles.sif')

    assert sif.name == 'circles'
    assert sif.description == 'I like circles. They are round.'
    assert sif.size == (480, 270)
    assert sif.resolution==(2834.645669, 2835)
    assert sif.gamma==(0.98, 0.99, 1.0)
    assert sif.background==sangfroid.value.Color('#7f7f7f')

def test_load_sifz():
    sif = get_animation('wombats.sifz')

    assert sif.name == 'wombats'
    assert sif.description == 'I like wombats. They live in Australia.'
