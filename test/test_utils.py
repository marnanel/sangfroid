import pytest
import bs4
import sangfroid
from sangfroid.utils import *
from test import *

def test_utils_fps():
    sif = get_animation('circles.sif')

    orange_circle = sif.find(desc='Orange circle')
    assert tag_to_fps(orange_circle.tag)==24

    wombat = bs4.Tag(name='wombat')
    with pytest.raises(ValueError):
        tag_to_fps(wombat)
