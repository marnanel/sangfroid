import pytest
import sangfroid
from sangfroid.value import *
from test import *

def test_vector_simple():
    sif = get_animation('circles.sif')
    green_circle = sif.find(desc='Green circle')
    origin = green_circle['origin']

    assert origin['x'] == -2.7426433563
    assert origin['y'] == -1.7542968988

    assert list(zip(origin, origin))==[
        (-2.7426433563, -2.7426433563),
        (-1.7542968988, -1.7542968988),
        ]

    assert origin == (-2.7426433563, -1.7542968988)
    assert origin.as_tuple() == (-2.7426433563, -1.7542968988)
    assert len(origin) == 2

def test_vector_as_dict():
    sif = get_animation('circles.sif')
    green_circle = sif.find(desc='Green circle')
    origin = green_circle['origin']

    try:
        origin['wombat']
        ok = False
    except KeyError:
        ok = True

    assert ok, "subscript with unreal string raises KeyError"

    assert origin.get('x') == -2.7426433563
    assert origin.get('y') == -1.7542968988
    assert origin.get('wombat') == None

    assert origin.get('x', 'no') == -2.7426433563
    assert origin.get('y', 'no') == -1.7542968988
    assert origin.get('wombat', 'no') == 'no'

    assert sorted(origin.items()) == [
        ('x', -2.7426433563),
        ('y', -1.7542968988),
        ]
    assert sorted(origin.keys()) == ['x', 'y']
    assert sorted(origin.values()) == [
        -2.7426433563,
        -1.7542968988,
        ]

def test_vector_constructor():
    assert str(Vector(1.0, 2.0))=='(1.0, 2.0)'
    assert str(Vector({'x': 1.0, 'y': 2.0}))=='(1.0, 2.0)'
    assert str(Vector({'a': 1.0, 'b': 2.0}))==(
            "{'a': '1.0000000000', 'b': '2.0000000000'}"
            )

    with pytest.raises(TypeError):
        Vector(1.0, 'banana')

    with pytest.raises(TypeError):
        Vector(1,2,3)
