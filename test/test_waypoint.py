import sangfroid
from test import *
import pytest

def test_waypoint_simple():
    sif = get_sif('bouncing.sif')

    ball = sif.find(desc='Ball')
    scale = ball['transformation']['scale']

    assert scale.is_animated

    for found, expected in zip(scale.timeline, [
        sangfroid.value.Waypoint( '0f', 'constant', 'constant'),
        sangfroid.value.Waypoint('24f', 'linear',   'linear'),
        sangfroid.value.Waypoint('48f', 'constant', 'constant'),
        ]):
        assert found==expected
