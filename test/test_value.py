import sangfroid
from sangfroid.value import Vector, Angle
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

    assert list(zip(origin, origin))==[
        (-2.7426433563, -2.7426433563),
        (-1.7542968988, -1.7542968988),
        ]

    assert origin == (-2.7426433563, -1.7542968988)
    assert origin.as_tuple() == (-2.7426433563, -1.7542968988)
    assert len(origin) == 2

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

    assert transformation['angle'] == 45.0
    assert transformation['skew_angle'] == 50.5

    assert str(transformation['angle']) == '45°'
    assert str(transformation['skew_angle']) == '50.5°'

    try:
        transformation['wombat']
        ok = False
    except KeyError:
        ok = True

    assert ok, "subscript with unreal string raises KeyError"

    assert len(transformation)==4

    assert transformation.get('offset') == (3.3333332539, -0.8333333135)
    assert transformation.get('angle') == 45.0
    assert transformation.get('skew_angle') == 50.5
    assert transformation.get('scale') == (2, 0.5)
    assert transformation.get('wombat') == None

    assert transformation.get('offset', 'no') == (3.3333332539, -0.8333333135)
    assert transformation.get('angle', 'no') == 45.0
    assert transformation.get('skew_angle', 'no') == 50.5
    assert transformation.get('scale', 'no') == (2, 0.5)
    assert transformation.get('wombat', 'no') == 'no'

    assert transformation == {
            'offset': (3.3333332539, -0.8333333135),
            'angle': 45.0,
            'skew_angle': 50.5,
            'scale': (2, 0.5),
            }

    assert sorted(transformation.items()) == [
            ('angle', Angle(45.0)),
            ('offset', Vector(3.3333332539, -0.8333333135)),
            ('scale', Vector(2, 0.5)),
            ('skew_angle', Angle(50.5)),
            ]

    assert sorted(transformation.keys()) == [
            'angle',
            'offset',
            'scale',
            'skew_angle',
            ]
    assert set([str(x) for x in transformation.values()]) == {
            '(3.3333332539, -0.8333333135)',
            '45°',
            '50.5°',
            '(2.0, 0.5)',
            }

def test_value_angle():
    sif = get_sif('circles.sif')
    layer = sif.find(desc="Well, it's round")
    transformation = layer['transformation']

    assert transformation['angle'] == 45.0
    assert transformation['skew_angle'] == 50.5

    assert str(transformation['angle']) == '45°'
    assert str(transformation['skew_angle']) == '50.5°'

def test_value_str_animated():
    sif = get_sif('bouncing.sif')

    background = sif.find(desc='Background')
    assert str(background['transformation']['scale'])=='(1.0, 1.0)'

    shadow = sif.find(desc='Shadow')
    assert str(shadow['transformation']['scale'])=='(animated)'
