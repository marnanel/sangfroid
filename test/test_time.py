import sangfroid
from sangfroid.time import Time
from test import *

def test_time_seconds():
    t = Time('0s')
    assert int(t)==0
    assert t.frames==0
    assert t.seconds==0.0
    assert str(t)=='0f'

    t = Time('2s')
    assert int(t)==48
    assert t.frames==48
    assert t.seconds==2.0
    assert str(t)=='48f'

    t = Time('2s', fps=40)
    assert int(t)==80
    assert t.frames==80
    assert t.seconds==2.0
    assert str(t)=='80f'

def test_time_frames():
    t = Time('0f')
    assert int(t)==0
    assert t.frames==0
    assert t.seconds==0.0
    assert str(t)=='0f'

    t = Time('48f')
    assert int(t)==48
    assert t.frames==48
    assert t.seconds==2.0
    assert str(t)=='48f'

    t = Time('80f', fps=40)
    assert int(t)==80
    assert t.frames==80
    assert t.seconds==2.0
    assert str(t)=='80f'

def test_time_frames_as_int():
    t = Time(0)
    assert int(t)==0
    assert t.frames==0
    assert t.seconds==0.0
    assert str(t)=='0f'

    t = Time(48)
    assert int(t)==48
    assert t.frames==48
    assert t.seconds==2.0
    assert str(t)=='48f'

    t = Time(80, fps=40)
    assert int(t)==80
    assert t.frames==80
    assert t.seconds==2.0
    assert str(t)=='80f'

def test_time_ordering():
    assert Time('0f') < Time('1f')
    assert Time('1f') > Time('0f')
    assert Time('1f') == Time('1f')

    assert Time('23f') < Time('1s')
    assert Time('24f') == Time('1s')
    assert Time('25f') > Time('1s')

    assert Time('23f') <= Time('1s')
    assert Time('24f') <= Time('1s')
    assert Time('24f') >= Time('1s')
    assert Time('25f') >= Time('1s')

    slow = Time('1s', fps=10)
    normal = Time('1s')
    try:
        slow==normal
        assert False, "comparison should fail"
    except ValueError:
        pass

    try:
        slow<normal
        assert False, "comparison should fail"
    except ValueError:
        pass

def test_time_compare_silly():
    assert Time(1) != 'bananas'
