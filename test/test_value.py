import sangfroid
from test import *

def test_value_real():
    sif = get_sif('circles.sif')
    orange_circle = sif.find(desc='Orange circle')
    amount = orange_circle['amount']

    assert str(amount)=='1.0'
    assert repr(amount)=='[Real 1.0]'

    assert amount==1.0
    assert not amount==1.1
    assert amount==1
    assert not amount==2
    assert not amount=='bananas'

def test_value_vector():
    sif = get_sif('circles.sif')
    green_circle = sif.find(desc='Green circle')

    origin = green_circle['origin']
    assert origin['x'] == -2.7426433563
    assert origin['y'] == -1.7542968988

    assert origin == (-2.7426433563, -1.7542968988)
    assert origin.as_tuple() == (-2.7426433563, -1.7542968988)

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

def test_value_composite():
    sif = get_sif('circles.sif')
    layer = sif.find(desc="Well, it's round")
    transformation = layer['transformation']

    assert transformation['offset'] == (3.3333332539, -0.8333333135)
    assert transformation['angle'] == 45.0
    assert transformation['skew_angle'] == 50.0
    assert transformation['scale'] == (2, 0.5)

    try:
        transformation['wombat']
        ok = False
    except KeyError:
        ok = True

    assert ok, "subscript with unreal string raises KeyError"

    assert transformation.get('offset') == (3.3333332539, -0.8333333135)
    assert transformation.get('angle') == 45.0
    assert transformation.get('skew_angle') == 50.0
    assert transformation.get('scale') == (2, 0.5)
    assert transformation.get('wombat') == None

    assert transformation.get('offset', 'no') == (3.3333332539, -0.8333333135)
    assert transformation.get('angle', 'no') == 45.0
    assert transformation.get('skew_angle', 'no') == 50.0
    assert transformation.get('scale', 'no') == (2, 0.5)
    assert transformation.get('wombat', 'no') == 'no'

    assert sorted(transformation.items()) == [
        ('x', -2.7426433563),
        ('y', -1.7542968988),
        ]
    assert sorted(transformation.keys()) == ['x', 'y']
    assert sorted(transformation.values()) == [
        -2.7426433563,
        -1.7542968988,
        ]

