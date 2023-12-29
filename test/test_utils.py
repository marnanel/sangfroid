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

def test_utils_boolean():

    for thing, expected in [
            ("Boolean()",           False),
            ("Boolean(False)",      False),
            ("Boolean(0)",          False),
            ("Boolean(Boolean(0))", False),
            ("Boolean(True)",       True),
            ("Boolean(1)",          True),
            ("Boolean(Boolean(1))", True),
            ]:

        b = eval(thing)

        if expected:
            assert b, thing
            assert b==True, thing
            assert bool(b)==True, thing
            assert int(b)==1, thing
            assert str(b)=='true', thing
        else:
            assert not b, thing
            assert b==False, thing
            assert bool(b)==False, thing
            assert int(b)==0, thing
            assert str(b)=='false', thing
