import sangfroid
from test import *

def test_value_int():
    sif = get_animation('pick-and-mix.sif')
    value = sif.find('plant').seed

    assert isinstance(value, sangfroid.value.Integer)
    assert isinstance(float(value), float)
    assert isinstance(int(value), int)

    assert float(value)==1700432811.0
    assert int(value)==1700432811

def test_value_float():
    sif = get_animation('bouncing.sif')
    value = sif.find(desc='wall').amount

    assert isinstance(value, sangfroid.value.Real)
    assert isinstance(float(value), float)
    assert isinstance(int(value), int)

    assert float(value)==1.0
    assert int(value)==1

def test_value_bool_get():
    sif = get_animation('pick-and-mix.sif')
    timeloop = sif.find('timeloop')

    value = timeloop.symmetrical
    assert isinstance(value, sangfroid.value.Bool)
    assert isinstance(bool(value), bool)
    assert bool(value)==True

    assert value._tag.name=='bool'
    assert value._tag['value']=='true'

    value = timeloop.only_for_positive_duration
    assert isinstance(value, sangfroid.value.Bool)
    assert isinstance(bool(value), bool)
    assert bool(value)==False

def test_value_bool_put():
    sif = get_animation('pick-and-mix.sif')
    timeloop = sif.find('timeloop')

    assert timeloop.symmetrical==True
    assert timeloop.symmetrical._tag.name=='bool'
    assert timeloop.symmetrical._tag['value']=='true'

    timeloop.symmetrical = False

    assert timeloop.symmetrical==False
    assert timeloop.symmetrical._tag.name=='bool'
    assert timeloop.symmetrical._tag['value']=='false'

    timeloop.symmetrical = True

    assert timeloop.symmetrical==True
    assert timeloop.symmetrical._tag.name=='bool'
    assert timeloop.symmetrical._tag['value']=='true'
