import pytest
import sangfroid
from sangfroid.value import *
from test import *

def test_value_real():
    sif = get_animation('circles.sif')
    orange_circle = sif.find(desc='Orange circle')
    amount = orange_circle['amount']

    assert str(amount)=='1.0'
    assert repr(amount)=='[Real 1.0]'

    assert amount==1.0
    assert not amount==1.1
    assert amount==1
    assert not amount==2
    assert not amount=='bananas'

def test_value_composite():
    sif = get_animation('circles.sif')
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

def test_value_str_animated():
    sif = get_animation('bouncing.sif')

    background = sif.find(desc='Background')
    assert str(background['transformation']['scale'])=='(1.0, 1.0)'

    shadow = sif.find(desc='Shadow')
    assert str(shadow['transformation']['scale'])=='(animated)'

def test_value_timeline_on_and_off():
    sif = get_animation('circles.sif')
    orange_circle = sif.find(desc='Orange circle')
    amount = orange_circle['amount']

    assert str(amount)=='1.0'
    assert amount.timeline is None
    assert amount.our_type==float

    amount.timeline = []
    assert amount.timeline==[]
    assert amount.our_type==float

    amount.timeline = None
    assert amount.timeline is None
    assert amount.our_type==float

def test_value_timeline_assign():
    r = Real(1.77)
    assert str(r)=='1.77'

    r.timeline = [
            Waypoint(time=T('0s', fps=24), value=Real(1.0)),
            Waypoint(time=T('1s', fps=24), value=Real(2.0)),
            ]

    s = Real(1.77)
    s.timeline = r.timeline

    for obj in [r, s]:
        assert [str(w.value) for w in obj.timeline] == ['1.0', '2.0']

    assert r.timeline[0] == s.timeline[0]
    assert r.timeline[0] is not s.timeline[0]

def test_value_timeline_assign_twice():
    r = Real(1.77)
    assert str(r)=='1.77'
    assert r.is_animated == False

    r.timeline = [
            Waypoint(time=T('0f', fps=24), value=Real(1.0)),
            ]
    assert r.is_animated == True
    assert len(r.timeline)==1
    assert r.timeline[0].time == T('0f')

    r.timeline = [
            Waypoint(time=T('1f', fps=24), value=Real(2.0)),
            ]
    assert r.is_animated == True
    assert len(r.timeline)==1
    assert r.timeline[0].time == T('1f')

def test_value_tag_name():
    r = Real(1.77)
    assert str(r.tag)=='<real value="1.77"></real>'
