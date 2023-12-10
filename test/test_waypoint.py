import sangfroid
from sangfroid.value.value import Waypoint
from sangfroid.time import Time
from test import *
import pytest

def test_waypoint_simple():
    sif = get_sif('bouncing.sif')

    ball = sif.find(desc='Ball')
    scale = ball['transformation']['scale']

    assert scale.is_animated

    for found, expected in zip(scale.timeline, [
        ( '0f', 'ease', 'ease'),
        ('24f', 'linear', 'linear'),
        ('48f', 'ease', 'ease'),
        ]):

        assert found.time==Time(expected[0])
        assert found.before==expected[1]
        assert found.after==expected[2]

def test_waypoint_silly():

    value = sangfroid.value.Bool(True)

    with pytest.raises(ValueError):
        # silly interpolation type
        Waypoint('0f', 'wombat', 'ease', value)

    with pytest.raises(TypeError):
        # values must be sangfroid.value.Values
        Waypoint('0f', 'ease', 'ease', True)
