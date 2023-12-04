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
