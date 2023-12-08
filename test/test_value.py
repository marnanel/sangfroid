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
    assert green_circle['radius'] == 0.5055338531

    try:
        green_circle['wombat']
        ok = False
    except KeyError:
        ok = True

    assert ok, 'subscript of unreal string should raise KeyError'

    origin = green_circle['origin']
    assert origin['x'] == -2.7426433563
    assert origin['y'] == -1.7542968988

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
