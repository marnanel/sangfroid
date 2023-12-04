import sangfroid
from test import *
import pytest

def test_waypoint_simple():
    sif = get_sif('bouncing.sif')

    ball = sif.find(desc='ball')
    scale = ball['scale']

    assert scale.is_animated
    assert False
