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

def test_value_vector_simple():
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

def test_value_vector_as_dict():
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

def test_value_vector_constructor():
    assert str(Vector(1.0, 2.0))=='(1.0, 2.0)'
    assert str(Vector({'x': 1.0, 'y': 2.0}))=='(1.0, 2.0)'
    assert str(Vector({'a': 1.0, 'b': 2.0}))=="{'a': '1.0', 'b': '2.0'}"

    with pytest.raises(TypeError):
        Vector(1.0, 'banana')

    with pytest.raises(TypeError):
        Vector(1,2,3)

def test_value_angle():
    sif = get_animation('circles.sif')
    layer = sif.find(desc="Well, it's round")
    transformation = layer['transformation']

    assert transformation['angle'] == 45.0
    assert transformation['skew_angle'] == 50.5

    assert str(transformation['angle']) == '45°'
    assert str(transformation['skew_angle']) == '50.5°'

    angle = Angle(45)
    assert angle==45
    assert str(angle) == '45°'

def test_value_str_animated():
    sif = get_animation('bouncing.sif')

    background = sif.find(desc='Background')
    assert str(background['transformation']['scale'])=='(1.0, 1.0)'

    shadow = sif.find(desc='Shadow')
    assert str(shadow['transformation']['scale'])=='(animated)'

def test_value_color_compare():
    sif = get_animation('circles.sif')

    blue_circle = sif.find(desc='Blue circle')
    found = blue_circle['color']

    LITERALS = [
            ('tuple, with alpha',    (0.0, 0.2, 1.0, 1.0)),
            ('tuple, no alpha',      (0.0, 0.2, 1.0)),
            ('string, with alpha',   '#0033FFFF'),
            ('string, no alpha',     '#0033FF'),
            ]

    OBJECTS = [('retrieved from sif', found)]
    OBJECTS.extend([
        (f'colour from {name}', Color(o))
        for name, o in LITERALS])

    for first_name, first in OBJECTS:
        for literal_name, literal in LITERALS:
            assert first==literal, f"{first_name} vs {literal_name}"

        for second_name, second in OBJECTS:
            assert first==second, f"{first_name} vs {second_name}"

def test_value_color_assign():
    c = Color()
    xml_compare(c.tag, """
<color>
  <r>1.000000</r>
  <g>1.000000</g>
  <b>1.000000</b>
  <a>1.000000</a>
</color>""", asserting='with no parameters')

    c = Color(0.1, 0.2, 0.3)
    xml_compare(c.tag, """
<color>
  <r>0.100000</r>
  <g>0.200000</g>
  <b>0.300000</b>
  <a>1.000000</a>
</color>""", asserting='with 3 floats')

    c = Color(0.1, 0.2, 0.3, 0.4)
    xml_compare(c.tag, """
<color>
  <r>0.100000</r>
  <g>0.200000</g>
  <b>0.300000</b>
  <a>0.400000</a>
</color>""", asserting='with 4 floats')

    c = Color("#102030")
    xml_compare(c.tag, """
<color>
  <r>0.062745</r>
  <g>0.125490</g>
  <b>0.188235</b>
  <a>1.000000</a>
</color>""", asserting='with 6 hex digits with hash')

    c = Color("102030")
    xml_compare(c.tag, """
<color>
  <r>0.062745</r>
  <g>0.125490</g>
  <b>0.188235</b>
  <a>1.000000</a>
</color>""", asserting='with 6 hex digits with no hash')

    c = Color("#10203040")
    xml_compare(c.tag, """
<color>
  <r>0.062745</r>
  <g>0.125490</g>
  <b>0.188235</b>
  <a>0.250980</a>
</color>""", asserting='with 8 hex digits with hash')

    c = Color("10203040")
    xml_compare(c.tag, """
<color>
  <r>0.062745</r>
  <g>0.125490</g>
  <b>0.188235</b>
  <a>0.250980</a>
</color>""", asserting='with 8 hex digits with no hash')
